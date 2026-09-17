# SEP-KAS1-Patch

Makes the **AKI Power Transfer Conduit** from [Surface Experiment Pack](https://github.com/CobaltWolf/Surface-Experiment-Pack) 2.7.x work with **KAS 1.x** on KSP 1.8–1.12.

SEP still ships the legacy `KASModulePort`/`KASModuleStrut` modules, which were removed in KAS 1.0, so the plug has no *Link* action and experiments can't be connected to the Central Station ([CobaltWolf/Surface-Experiment-Pack#41](https://github.com/CobaltWolf/Surface-Experiment-Pack/issues/41)). This ModuleManager patch replaces them with `KASLinkSourceInteractive` + `KASLinkTargetBase` + `KASRendererPipe` + `KASJointRigid`, following KAS's own legacy-pipe template. Joint limits match the original strut (30 m, 100°, break force 600).

## Usage

Unchanged from the original mod: KIS-attach one plug to the Central Station and one to the experiment, then on EVA right-click a plug → **Link** and click the other plug. The experiment becomes part of the station's vessel and shows up in the station.

## Upgrade note

Plugs that already existed in KIS inventories or on vessels **before** installing this patch keep their old part snapshot (without the KAS modules) and will throw an error when linking. Re-create them in the VAB.

## Install

Copy `GameData/SEP-KAS1-Patch` into your `GameData`. Requires Surface Experiment Pack, KAS ≥ 1.0, KIS and ModuleManager. Available on CKAN as `SEP-KAS1-Patch`.

The same change was submitted upstream as a pull request; this patch exists because the upstream repository has been unmaintained since 2019.

## License

BSD 2-Clause (same as SEP).
