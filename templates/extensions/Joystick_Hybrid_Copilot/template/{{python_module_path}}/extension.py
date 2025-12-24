import omni.ext
import omni.kit.app
import threading
import time
from typing import Callable, List, Dict, Optional


class JoystickManager:
    """Small, cross-platform joystick input manager used by the template.

    It attempts to use `inputs` (linux/windows) and falls back to `pygame` if
    `inputs` is not available. In headless/test environments the manager emits
    a lightweight "heartbeat" event so callbacks can be exercised during tests.
    """

    def __init__(self) -> None:
        self._callbacks: List[Callable[[Dict], None]] = []
        self._lock = threading.Lock()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._impl = None  # 'inputs', 'pygame', or 'heartbeat'

        # Choose an implementation at import-time
        try:
            # inputs is cross-platform and preferable when available
            from inputs import get_gamepad  # type: ignore

            self._impl = "inputs"
            self._get_gamepad = get_gamepad
        except Exception:
            try:
                import pygame  # type: ignore

                pygame.init()
                pygame.joystick.init()
                self._impl = "pygame"
                self._pygame = pygame
            except Exception:
                # No joystick libraries available; fall back to heartbeat
                self._impl = "heartbeat"

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if not self._running:
            return
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=0.5)
            self._thread = None

    def register_callback(self, cb: Callable[[Dict], None]) -> None:
        with self._lock:
            if cb not in self._callbacks:
                self._callbacks.append(cb)

    def unregister_callback(self, cb: Callable[[Dict], None]) -> None:
        with self._lock:
            try:
                self._callbacks.remove(cb)
            except ValueError:
                pass

    def _dispatch(self, event: Dict) -> None:
        # Copy for thread-safety
        with self._lock:
            cbs = list(self._callbacks)
        for cb in cbs:
            try:
                cb(event)
            except Exception:
                # Swallow exceptions from user callbacks to avoid bringing down the polling thread
                pass

    def _poll_loop(self) -> None:
        if self._impl == "inputs":
            self._poll_inputs_impl()
        elif self._impl == "pygame":
            self._poll_pygame_impl()
        else:
            self._poll_heartbeat()

    def _poll_inputs_impl(self) -> None:
        # Using `inputs.get_gamepad()` which blocks until events are available
        try:
            while self._running:
                events = self._get_gamepad()
                for e in events:
                    event = {"type": e.ev_type, "code": e.code, "state": e.state}
                    self._dispatch(event)
        except Exception:
            # Implementation error — stop polling
            self._running = False

    def _poll_pygame_impl(self) -> None:
        pygame = getattr(self, "_pygame")
        # If there are no joysticks the loop will fallback to the heartbeat behavior
        count = pygame.joystick.get_count()
        if count == 0:
            return self._poll_heartbeat()
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        while self._running:
            try:
                pygame.event.pump()
                axis_states = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]
                button_states = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
                event = {"type": "gamepad", "axis": axis_states, "buttons": button_states}
                self._dispatch(event)
            except Exception:
                break
            time.sleep(0.01)

    def _poll_heartbeat(self) -> None:
        # Useful in tests and headless environments. Emits a sparse "heartbeat" event.
        while self._running:
            self._dispatch({"type": "heartbeat", "timestamp": time.time()})
            time.sleep(0.1)


class JoystickHybridCopliotExtension(omni.ext.IExt):
    """Joysticks in Kit: provide a simple background-polling manager with a callback API.

    - `JoystickManager` picks a library and starts a polling thread.
    - Use `register_callback` to receive events: `cb(event: dict)`.
    - Extension guarantees safe start/stop in `on_startup`/`on_shutdown`.
    """

    def on_startup(self, ext_id: str) -> None:
        self._joystick_manager = JoystickManager()
        self._joystick_manager.start()

        # Example callback to show activity in the console
        def debug_cb(evt: Dict) -> None:
            print(f"[Joystick] {evt}")

        self._joystick_manager.register_callback(debug_cb)

        # Store debug callback for cleanup
        self._debug_cb = debug_cb

    def on_shutdown(self) -> None:
        if hasattr(self, "_joystick_manager"):
            try:
                self._joystick_manager.unregister_callback(self._debug_cb)
            except Exception:
                pass
            self._joystick_manager.stop()

    # Public convenience methods so other extensions can use the joystick manager
    def register_callback(self, cb: Callable[[Dict], None]) -> None:
        if hasattr(self, "_joystick_manager"):
            self._joystick_manager.register_callback(cb)

    def unregister_callback(self, cb: Callable[[Dict], None]) -> None:
        if hasattr(self, "_joystick_manager"):
            self._joystick_manager.unregister_callback(cb)
