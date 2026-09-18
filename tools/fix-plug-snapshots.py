#!/usr/bin/env python3
"""Inject the KAS 1.x modules into old SEP_plug snapshots.

Plugs that existed before SEP-KAS1-Patch was installed (in KIS inventories,
inside .craft files or as vessel parts in .sfs saves) keep a part snapshot
without the KAS modules. When such a plug is used, KSP Community Fixes creates
empty module instances, KAS's OnLoad never runs and "Link" fails with a
NullReferenceException in KASRendererPipe.UpdateMaterialOverrides.

Usage: fix-plug-snapshots.py [-n] [--cache PATH] <file.craft|file.sfs> ...
  -n            report only, do not write
  --cache PATH  GameData/ModuleManager.ConfigCache to take the modules from
                (default: found by walking up from the first file's directory)

Run with the game closed. The modules are copied from the patched SEP_plug
prefab in the ModuleManager cache, so start KSP once with the patch installed
before using this. Every changed file gets a backup <file>.bak-YYYYmmdd-HHMMSS.
"""
import os, re, sys, shutil, datetime

PART = "SEP.plug"
KAS_MODULES = ("KASLinkSourceInteractive", "KASLinkTargetBase", "KASRendererPipe", "KASJointRigid")


def node_end(s, start):
    """Index of the '}' closing the node whose '{' is the first after start."""
    depth = 0
    i = s.index("{", start)
    for j in range(i, len(s)):
        c = s[j]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return j
    raise ValueError("unterminated node")


def find_cache(path):
    d = os.path.dirname(os.path.abspath(path))
    while True:
        c = os.path.join(d, "GameData", "ModuleManager.ConfigCache")
        if os.path.isfile(c):
            return c
        parent = os.path.dirname(d)
        if parent == d:
            sys.exit("GameData/ModuleManager.ConfigCache not found above %s; pass --cache" % path)
        d = parent


def kas_modules_from_cache(cache):
    s = open(cache, errors="replace").read()
    m = re.search(r"\n\s*PART\s*\{\s*name = SEP_plug\b", s)
    if not m:
        sys.exit("PART SEP_plug is not in the ConfigCache; start KSP once with the patch installed")
    part = s[m.start():node_end(s, m.start()) + 1]
    blocks = []
    for mm in re.finditer(r"\n(\s*)MODULE\s*\{\s*name = (\w+)", part):
        if mm.group(2) in KAS_MODULES:
            blk = part[mm.start() + 1:node_end(part, mm.start()) + 1]
            ind = mm.group(1)  # strip the cache's indentation
            blocks.append("\n".join(l[len(ind):] if l.startswith(ind) else l for l in blk.split("\n")))
    if len(blocks) != len(KAS_MODULES):
        sys.exit("expected %d KAS modules in the prefab, found %d" % (len(KAS_MODULES), len(blocks)))
    return blocks


def fix_file(path, blocks, dry):
    s = open(path, errors="replace").read()
    out, pos, fixed, total = [], 0, 0, 0
    for m in re.finditer(r"PART\s*\{\s*name = " + re.escape(PART) + r"\b", s):
        if m.start() < pos:
            continue
        end = node_end(s, m.start())
        node = s[m.start():end]
        total += 1
        if KAS_MODULES[0] in node:
            continue
        ls = s.rfind("\n", 0, m.start()) + 1
        ind = s[ls:m.start()]  # indentation of the PART line
        inner = ind + "\t"
        inj = "".join("\n".join(inner + l for l in b.split("\n")) + "\n" for b in blocks)
        out.append(s[pos:end - len(ind)])  # up to the closing '}' (which follows \n + ind)
        out.append(inj)
        pos = end - len(ind)
        fixed += 1
    out.append(s[pos:])
    print("%s: %d %s snapshot(s), %d without KAS modules%s" % (
        os.path.basename(path), total, PART, fixed, " (fixed)" if fixed and not dry else ""))
    if fixed and not dry:
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copy2(path, "%s.bak-%s" % (path, stamp))
        open(path, "w").write("".join(out))


if __name__ == "__main__":
    args = sys.argv[1:]
    dry = "-n" in args
    cache = None
    if "--cache" in args:
        i = args.index("--cache")
        cache = args[i + 1]
        del args[i:i + 2]
    files = [a for a in args if a != "-n"]
    if not files:
        sys.exit(__doc__)
    blocks = kas_modules_from_cache(cache or find_cache(files[0]))
    for f in files:
        fix_file(f, blocks, dry)
