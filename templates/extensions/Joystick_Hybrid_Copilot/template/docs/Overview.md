# Overview

This extension demonstrates a simple approach to integrating joystick or gamepad input
inside an Omniverse Kit Python extension. It uses a background thread to poll input libraries
and offers a safe callback registration API so other extensions can subscribe to events.

The polling manager prefers `inputs` (when available) and falls back to `pygame`, while
providing a `heartbeat` fallback for safe testing in environments without hardware.
