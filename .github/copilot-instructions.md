## Quick orientation

This repository is the Omniverse Kit App Template. It contains reusable templates for Kit-based Applications and Extensions and tooling to create, build, launch, test and package them.

Keep these quick facts top-of-mind when editing code here:

- Primary app/extension sources live under `source/apps/` and `source/extensions/`.
- Application descriptors are TOML `.kit` files (see `source/apps/my_company.my_usd_explorer.kit`). Those files declare `[package]`, `[dependencies]` and `[settings.app]` and are the canonical place for app metadata and runtime settings.
- The repository tooling is driven by `repo.bat` (Windows) and `repo.sh` (Linux) which call the Python repoman. Common commands used by developers are: template new, build, launch, test, and package.

## Key commands (Windows PowerShell examples)

- Create a new app from a template: `.
epo.bat template new`
- Build all configured apps/extensions: `.
epo.bat build`
- Launch an app: `.
epo.bat launch`
- Run unit tests: `.
epo.bat test`
- Package for distribution: `.
epo.bat package`

Note: `repo.bat` delegates to `tools/repoman/repoman.py` via the repository packman/python bootstrap (see top of `repo.bat`).

## Project-specific conventions you must follow

- .kit filenames and package names are namespaced and lowercase (example: `my_company.my_usd_explorer.kit`). Keep them alphanumeric and namespaced to avoid collisions with Kit bundles.
- When adding an app, add its `.kit` file under `source/apps/` and add a `define_app("<your_app>.kit")` entry in `premake5.lua` so the repo build system generates the wrappers (see `premake5.lua`).
- Runtime flags and behavior come from `settings.app` in the `.kit` file. Prefer changing behavior there instead of scattering hard-coded values across Python/C++ code.
- Extensions referenced by apps are typically named `my_company.<extension_name>` and live under `source/extensions/<name>/` with an obvious `docs/` folder for README-like guidance.

## Build / artifacts / where to look

- Generated build artifacts and per-platform wrappers appear under `_build/` and `_build/windows-x86_64/` (also see `windows-x86_64/debug` and `windows-x86_64/release` produced by the build).
- Premake-based generation (see `premake5.lua`) creates platform-specific launch wrappers and VS project files when appropriate.

## Language / platform notes

- Templates support Python and C++. For Windows C++ you must use MSVC; see the root README for the Visual Studio/Windows SDK requirements.
- Some C++ templates require repo-level flags (for example: `platform:windows-x86_64` and `link_host_toolchain`) — these are controlled in `repo.toml` and template metadata. If you change C++ build behavior, update `premake5.lua` and verify generated projects.

## Templates & examples to inspect

- `templates/apps/kit_base_editor/` — minimal editor app.
- `templates/extensions/basic_python/` and `templates/extensions/basic_cpp/` — how extensions are structured.
- `source/apps/my_company.my_usd_explorer.kit` — practical example of dependencies and `settings.app.*` usage (lots of real settings and extension ordering). Use it as the primary example when you need to modify app settings.

## When an AI agent edits this repo

- Prefer small, atomic changes: modify a `.kit` file, run the build, and verify the generated wrapper files under `_build/` before making further edits.
- If you add or remove an app, update `premake5.lua`'s `define_app("...")` list — builds rely on that list to generate artifacts.
- When changing dependency ordering in a `.kit` file, maintain any explicit `order = <num>` properties seen in `my_company.my_usd_explorer.kit` — ordering matters for extension startup sequence.
- If you touch C++ or platform-specific code, include a short note in the change describing how to regenerate platform project files and any additional toolchain settings required.

## Files to reference for common operations

- `README.md` (repo root) — overall quick-start and tooling guide.
- `repo.bat`, `repo.sh` — entry points for repo tooling.
- `premake5.lua` — app registration via `define_app` and generation of build wrappers.
- `templates/` — canonical starter code for apps and extensions.
- `readme-assets/additional-docs/` — contains docs like streaming configuration, troubleshooting, and Windows developer notes.

## If anything is unclear

Leave a short comment in a Pull Request referencing this file and include: which app/extension you intended to change, the `.kit` file path, and the simple goal (e.g., "increase default viewport width" or "add extension X to app Y"). That context helps reviewers and automated tooling.

---
If you'd like, I can open a draft PR with this file added and iterate based on which sections you want expanded or trimmed.
