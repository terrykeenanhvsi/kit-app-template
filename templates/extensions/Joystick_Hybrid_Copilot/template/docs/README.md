# {{ extension_display_name }} [{{ extension_name }}]

This is an example of pure python Kit extension. It is intended to be copied and serve as a template to create new ones.

## Overview

This extension provides a small `JoystickManager` which polls for joystick/gamepad events
using either the `inputs` (preferred) or `pygame` libraries when available. In headless
or test environments a conservative "heartbeat" fallback is used so code relying on events
can be developed without hardware.

## Usage

Within another extension or the Kit Python environment you can access this extension and
register a callback as follows:

```python
import omni.kit.app

ext = omni.kit.app.get_app().get_extension_instance("{{ extension_name }}")

def cb(evt):
	print(evt)

ext.register_callback(cb)
```

## Optional Dependencies

To enable real joystick/gamepad input, install one of the following in your Kit Python environment:

- `inputs` (recommended)
- `pygame` (fallback)

On Windows/Developer workstations, you can install with pip. Make sure to install into
the Kit Python environment used by `repo.bat`/`repo.sh`.

```powershell
# Windows (PowerShell)
.\tools\packman\python.bat -m pip install inputs
.\tools\packman\python.bat -m pip install pygame
```

If you plan to distribute your extension or want reproducible builds, consider adding
these optional dependencies under your project's packaging rules (pip prebundle) so
they are included in the build process.
