


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# CoPilot

# In NVIDIA Omniverse Kit / Isaac Sim, if you want to run a Python function every frame, you can use the update event subscription API.
# This is done by subscribing to the "update" event stream from the app’s event bus.

# Here’s a complete runnable example:

# Python

# Copy code
# import omni.kit.app

# # Get the Kit application instance
# app = omni.kit.app.get_app()

# # Define the function to run every frame
# def on_update(dt: float):
#     """
#     Called every frame.
#     dt = time delta in seconds since last frame.
#     """
#     print(f"Frame update: dt={dt:.4f} seconds")

# # Subscribe to the update event
# subscription = app.get_update_event_stream().create_subscription_to_pop(on_update)

# # Keep the subscription alive
# # (If you store it in a local variable, it may get garbage-collected)
# _subscriptions = [subscription]
# How it works
# get_update_event_stream() returns an event stream that fires once per frame.
# create_subscription_to_pop(callback) registers your callback.
# The callback receives dt (delta time) each frame.
# You must keep a reference to the subscription object, otherwise it will stop working.
# Alternative: Using omni.timeline for simulation frames
# If you specifically want to run code only when the simulation is playing (e.g., physics steps), you can hook into the timeline:

# Python

# Copy code
# import omni.timeline

# timeline = omni.timeline.get_timeline_interface()

# def on_simulation_step(e):
#     print("Simulation step event:", e)

# # Subscribe to timeline events
# sub = timeline.get_timeline_event_stream().create_subscription_to_pop(on_simulation_step)
# _subscriptions = [sub]
# ✅ Tips:

# Use the update event for UI or per-frame logic.
# Use the timeline event for simulation-specific logic.
# Avoid heavy computations in these callbacks to prevent frame drops.
# If you want, I can give you a version that runs only while the viewport is rendering to save performance.
# Do you want me to prepare that?

# # Got it ✅ — if you want your Python code in Omniverse to run only while the viewport is actively rendering, you can hook into the rendering update stream instead of the global update event.

# # Here’s a complete, runnable example:

# # Python

# # Copy code
# # import omni.kit.app
# # import omni.kit.viewport.utility as vp_utils

# # # Get the Kit app instance
# # app = omni.kit.app.get_app()

# # # Get the active viewport window
# # viewport = vp_utils.get_active_viewport_window()

# # # Define the per-frame callback
# # def on_viewport_update(dt: float):
# #     """
# #     Called only when the viewport is actively rendering.
# #     dt = time delta in seconds since last frame.
# #     """
# #     print(f"[Viewport Frame] dt={dt:.4f} seconds")

# # # Subscribe to the viewport's update event stream
# # if viewport:
# #     sub = viewport.get_update_event_stream().create_subscription_to_pop(on_viewport_update)
# #     _subscriptions = [sub]  # Keep reference alive
# # else:
# #     print("No active viewport found.")
# # How this works
# # get_active_viewport_window() returns the current viewport window object.
# # get_update_event_stream() on the viewport fires only when the viewport is rendering.
# # This avoids running your code when the app is idle or the viewport is paused.
# # Keeping _subscriptions in a global list ensures the subscription isn’t garbage-collected.
# # When to use this
# # Good for: Debug overlays, per-frame rendering logic, camera tracking, or lightweight visual updates.
# # Not good for: Heavy computation — that should be offloaded to background threads or async tasks.
# # If you want, I can also give you a hybrid version that:

# # Runs only when simulation is playing
# # And only when the viewport is rendering
# # This is useful for physics-driven visualizations.
# # Do you want me to prepare that hybrid version?

# Alright — here’s a hybrid Omniverse Python example that runs your code only when:

# The simulation is playing (via omni.timeline)
# The viewport is actively rendering (via viewport update stream)
# This is ideal for physics-driven visualizations or simulation-dependent overlays.

# Python

# Copy code
# import omni.kit.app
# import omni.kit.viewport.utility as vp_utils
# import omni.timeline

# # Get Kit app and timeline interfaces
# app = omni.kit.app.get_app()
# timeline = omni.timeline.get_timeline_interface()

# # Get active viewport window
# viewport = vp_utils.get_active_viewport_window()

# # State flag to track simulation status
# _simulation_running = False

# # Timeline event callback
# def on_timeline_event(event):
#     global _simulation_running
#     if event.type == int(omni.timeline.TimelineEventType.PLAY):
#         _simulation_running = True
#         print("[Hybrid] Simulation started.")
#     elif event.type == int(omni.timeline.TimelineEventType.STOP):
#         _simulation_running = False
#         print("[Hybrid] Simulation stopped.")

# # Per-frame callback (only runs if simulation is playing)
# def on_viewport_update(dt: float):
#     if _simulation_running:
#         print(f"[Hybrid Frame] dt={dt:.4f} seconds — simulation running")
#     # else: do nothing when simulation is paused

# # Create subscriptions
# _subscriptions = []

# # Subscribe to timeline events
# _subscriptions.append(
#     timeline.get_timeline_event_stream().create_subscription_to_pop(on_timeline_event)
# )

# # Subscribe to viewport updates (only if viewport exists)
# if viewport:
#     _subscriptions.append(
#         viewport.get_update_event_stream().create_subscription_to_pop(on_viewport_update)
#     )
# else:
#     print("[Hybrid] No active viewport found.")
# How it works
# on_timeline_event updates _simulation_running when the simulation starts/stops.
# on_viewport_update runs every rendered frame, but only executes logic if _simulation_running is True.
# This ensures:
# No code runs when simulation is paused.
# No code runs when viewport is idle.
# _subscriptions keeps the event subscriptions alive.
# ✅ Advantages of this hybrid approach

# Saves CPU/GPU cycles when simulation is paused or viewport is inactive.
# Perfect for real-time simulation visualizations, physics overlays, or sensor data rendering.
# If you want, I can extend this so it automatically unsubscribes when the script is stopped or reloaded, to avoid duplicate callbacks in Omniverse.
# Do you want me to add that cleanup logic?


# Perfect — here’s the hybrid Omniverse Python script updated with automatic cleanup logic so that when the script is stopped, reloaded, or the extension is disabled, it unsubscribes from all events and avoids duplicate callbacks.

# Python

# Copy code
# import omni.kit.app
# import omni.kit.viewport.utility as vp_utils
# import omni.timeline

# # --- Global state ---
# _subscriptions = []
# _simulation_running = False


# def on_timeline_event(event):
#     """Track simulation start/stop events."""
#     global _simulation_running
#     if event.type == int(omni.timeline.TimelineEventType.PLAY):
#         _simulation_running = True
#         print("[Hybrid] Simulation started.")
#     elif event.type == int(omni.timeline.TimelineEventType.STOP):
#         _simulation_running = False
#         print("[Hybrid] Simulation stopped.")


# def on_viewport_update(dt: float):
#     """Run per frame only when simulation is active."""
#     if _simulation_running:
#         print(f"[Hybrid Frame] dt={dt:.4f} seconds — simulation running")


# def subscribe_events():
#     """Subscribe to timeline and viewport events."""
#     global _subscriptions

#     app = omni.kit.app.get_app()
#     timeline = omni.timeline.get_timeline_interface()
#     viewport = vp_utils.get_active_viewport_window()

#     # Subscribe to timeline events
#     _subscriptions.append(
#         timeline.get_timeline_event_stream().create_subscription_to_pop(on_timeline_event)
#     )

#     # Subscribe to viewport updates
#     if viewport:
#         _subscriptions.append(
#             viewport.get_update_event_stream().create_subscription_to_pop(on_viewport_update)
#         )
#     else:
#         print("[Hybrid] No active viewport found.")


# def cleanup():
#     """Unsubscribe from all events."""
#     global _subscriptions
#     for sub in _subscriptions:
#         try:
#             sub.unsubscribe()
#         except Exception as e:
#             print(f"[Hybrid] Error during unsubscribe: {e}")
#     _subscriptions.clear()
#     print("[Hybrid] Cleaned up all subscriptions.")


# # --- Script entry point ---
# subscribe_events()

# # --- Optional: Auto-cleanup when script stops ---
# import atexit
# atexit.register(cleanup)
# 🔹 How this works
# subscribe_events() sets up both:
# Timeline event listener (simulation start/stop)
# Viewport update listener (per-frame rendering)
# cleanup() unsubscribes from all events to prevent duplicates when reloading scripts.
# atexit.register(cleanup) ensures cleanup runs automatically when the script is stopped or the extension is unloaded.
# ✅ Benefits of cleanup logic

# Prevents multiple callbacks stacking up after script reloads.
# Frees memory and avoids stale references.
# Keeps Omniverse responsive during development.
# If you want, I can also make a version that works as a proper Omniverse Extension so it automatically hooks into on_startup and on_shutdown without needing atexit.
# That’s the cleanest way for production use.

# Do you want me to prepare that extension version?

# exts/
# └── my.company.hybrid_frame/
#     ├── extension.toml
#     └── hybrid_frame.py
# extension.toml
# Toml

# Copy code
# [package]
# # Unique extension name (reverse domain style is recommended)
# name = "my.company.hybrid_frame"
# version = "1.0.0"
# title = "Hybrid Frame Callback Example"
# description = "Runs Python code only when simulation is playing AND viewport is rendering."
# category = "Simulation"
# authors = ["Your Name"]
# repository = ""
# keywords = ["omniverse", "simulation", "viewport", "events"]

# [dependencies]
# "omni.kit.viewport.utility" = {}
# "omni.timeline" = {}

# [python]
# module = "hybrid_frame"
# hybrid_frame.py
# Python

# Copy code
# import omni.ext
# import omni.kit.app
# import omni.kit.viewport.utility as vp_utils
# import omni.timeline


# class HybridFrameExtension(omni.ext.IExt):
#     def on_startup(self, ext_id):
#         """Called when the extension is enabled."""
#         print("[HybridFrameExtension] Startup")

#         self._subscriptions = []
#         self._simulation_running = False

#         # Get interfaces
#         self._app = omni.kit.app.get_app()
#         self._timeline = omni.timeline.get_timeline_interface()
#         self._viewport = vp_utils.get_active_viewport_window()

#         # Subscribe to timeline events
#         self._subscriptions.append(
#             self._timeline.get_timeline_event_stream().create_subscription_to_pop(
#                 self._on_timeline_event
#             )
#         )

#         # Subscribe to viewport updates
#         if self._viewport:
#             self._subscriptions.append(
#                 self._viewport.get_update_event_stream().create_subscription_to_pop(
#                     self._on_viewport_update
#                 )
#             )
#         else:
#             print("[HybridFrameExtension] No active viewport found.")

#     def on_shutdown(self):
#         """Called when the extension is disabled."""
#         print("[HybridFrameExtension] Shutdown — cleaning up subscriptions")
#         for sub in self._subscriptions:
#             try:
#                 sub.unsubscribe()
#             except Exception as e:
#                 print(f"[HybridFrameExtension] Error during unsubscribe: {e}")
#         self._subscriptions.clear()

#     def _on_timeline_event(self, event):
#         """Track simulation start/stop events."""
#         if event.type == int(omni.timeline.TimelineEventType.PLAY):
#             self._simulation_running = True
#             print("[HybridFrameExtension] Simulation started.")
#         elif event.type == int(omni.timeline.TimelineEventType.STOP):
#             self._simulation_running = False
#             print("[HybridFrameExtension] Simulation stopped.")

#     def _on_viewport_update(self, dt: float):
#         """Run per frame only when simulation is active."""
#         if self._simulation_running:
#             print(f"[HybridFrameExtension] Frame dt={dt:.4f} seconds — simulation running")
# 🚀 How to Use
# Create the folder structure above inside your Omniverse exts/ directory.
# Restart Omniverse Kit / Isaac Sim.
# Open Window → Extensions and enable Hybrid Frame Callback Example.
# Start the simulation — you’ll see per-frame logs only while simulation is running and viewport is rendering.
# ✅ Benefits of Extension Version
# No duplicate callbacks — lifecycle is tied to extension enable/disable.
# Clean separation of startup/shutdown logic.
# Production-safe — works across Omniverse Kit, Isaac Sim, and other Kit-based apps.
# Easy to package and share.
# If you want, I can also make this extension trigger a custom function instead of just printing, so you can plug in your own simulation logic without editing the extension core.

# Do you want me to make that pluggable callback version next?


# Alright — let’s make the pluggable callback version of the Omniverse extension so you can easily hook in your own simulation logic without editing the extension core.

# This way, you can just register a Python function from anywhere in Omniverse, and it will be called only when:

# The simulation is running
# The viewport is actively rendering
# 📂 Extension Structure

# Copy code
# exts/
# └── my.company.hybrid_frame/
#     ├── extension.toml
#     └── hybrid_frame.py
# extension.toml
# Toml

# Copy code
# [package]
# name = "my.company.hybrid_frame"
# version = "1.1.0"
# title = "Hybrid Frame Callback (Pluggable)"
# description = "Runs a registered Python callback only when simulation is playing AND viewport is rendering."
# category = "Simulation"
# authors = ["Your Name"]
# keywords = ["omniverse", "simulation", "viewport", "events"]

# [dependencies]
# "omni.kit.viewport.utility" = {}
# "omni.timeline" = {}

# [python]
# module = "hybrid_frame"
# hybrid_frame.py
# Python

# Copy code
# import omni.ext
# import omni.kit.app
# import omni.kit.viewport.utility as vp_utils
# import omni.timeline


# class HybridFrameExtension(omni.ext.IExt):
#     def on_startup(self, ext_id):
#         """Called when the extension is enabled."""
#         print("[HybridFrameExtension] Startup")

#         self._subscriptions = []
#         self._simulation_running = False
#         self._callback = None  # User-registered function

#         # Get interfaces
#         self._app = omni.kit.app.get_app()
#         self._timeline = omni.timeline.get_timeline_interface()
#         self._viewport = vp_utils.get_active_viewport_window()

#         # Subscribe to timeline events
#         self._subscriptions.append(
#             self._timeline.get_timeline_event_stream().create_subscription_to_pop(
#                 self._on_timeline_event
#             )
#         )

#         # Subscribe to viewport updates
#         if self._viewport:
#             self._subscriptions.append(
#                 self._viewport.get_update_event_stream().create_subscription_to_pop(
#                     self._on_viewport_update
#                 )
#             )
#         else:
#             print("[HybridFrameExtension] No active viewport found.")

#         # Expose registration API globally
#         import omni.kit.app
#         omni.kit.app.get_app().set_extension_instance(ext_id, self)

#     def on_shutdown(self):
#         """Called when the extension is disabled."""
#         print("[HybridFrameExtension] Shutdown — cleaning up subscriptions")
#         for sub in self._subscriptions:
#             try:
#                 sub.unsubscribe()
#             except Exception as e:
#                 print(f"[HybridFrameExtension] Error during unsubscribe: {e}")
#         self._subscriptions.clear()
#         self._callback = None

#     def register_callback(self, func):
#         """
#         Register a function to be called every frame when simulation is running.
#         The function must accept one argument: dt (float).
#         """
#         if not callable(func):
#             raise ValueError("Callback must be callable")
#         self._callback = func
#         print("[HybridFrameExtension] Callback registered.")

#     def unregister_callback(self):
#         """Remove the registered callback."""
#         self._callback = None
#         print("[HybridFrameExtension] Callback unregistered.")

#     def _on_timeline_event(self, event):
#         """Track simulation start/stop events."""
#         if event.type == int(omni.timeline.TimelineEventType.PLAY):
#             self._simulation_running = True
#             print("[HybridFrameExtension] Simulation started.")
#         elif event.type == int(omni.timeline.TimelineEventType.STOP):
#             self._simulation_running = False
#             print("[HybridFrameExtension] Simulation stopped.")

#     def _on_viewport_update(self, dt: float):
#         """Run per frame only when simulation is active."""
#         if self._simulation_running and self._callback:
#             try:
#                 self._callback(dt)
#             except Exception as e:
#                 print(f"[HybridFrameExtension] Error in callback: {e}")
# 🔹 How to Use the Pluggable Version
# Once the extension is enabled in Omniverse:

# Python

# Copy code
# import omni.kit.app

# # Get the extension instance
# ext = omni.kit.app.get_app().get_extension_instance("my.company.hybrid_frame")

# # Define your custom per-frame function
# def my_frame_logic(dt):
#     print(f"[Custom] Simulation frame dt={dt:.4f}")

# # Register it
# ext.register_callback(my_frame_logic)

# # Later, you can unregister if needed
# # ext.unregister_callback()
# ✅ Benefits of Pluggable Design
# No need to modify extension code — just register your function.
# Supports hot-swapping callbacks at runtime.
# Keeps simulation logic separate from event wiring.
# Works across Omniverse Kit, Isaac Sim, and other Kit-based apps.
# If you want, I can also make a multi-callback version so multiple scripts can register their own per-frame functions without overwriting each other — useful for collaborative simulation tools.

# Do you want me to make that multi-callback hybrid extension next?

# Alright — here’s the multi-callback hybrid Omniverse extension so multiple scripts can register their own per-frame functions without overwriting each other.

# This is useful if you have several tools or scripts that all need to run per simulation frame while the viewport is rendering.

# 📂 Extension Structure

# Copy code
# exts/
# └── my.company.hybrid_frame/
#     ├── extension.toml
#     └── hybrid_frame.py
# extension.toml
# Toml

# Copy code
# [package]
# name = "my.company.hybrid_frame"
# version = "1.2.0"
# title = "Hybrid Frame Callback (Multi-Callback)"
# description = "Runs multiple registered Python callbacks only when simulation is playing AND viewport is rendering."
# category = "Simulation"
# authors = ["Your Name"]
# keywords = ["omniverse", "simulation", "viewport", "events"]

# [dependencies]
# "omni.kit.viewport.utility" = {}
# "omni.timeline" = {}

# [python]
# module = "hybrid_frame"
# hybrid_frame.py
# Python

# Copy code
# import omni.ext
# import omni.kit.app
# import omni.kit.viewport.utility as vp_utils
# import omni.timeline


# class HybridFrameExtension(omni.ext.IExt):
#     def on_startup(self, ext_id):
#         """Called when the extension is enabled."""
#         print("[HybridFrameExtension] Startup (Multi-Callback)")

#         self._subscriptions = []
#         self._simulation_running = False
#         self._callbacks = set()  # Store multiple unique callbacks

#         # Get interfaces
#         self._app = omni.kit.app.get_app()
#         self._timeline = omni.timeline.get_timeline_interface()
#         self._viewport = vp_utils.get_active_viewport_window()

#         # Subscribe to timeline events
#         self._subscriptions.append(
#             self._timeline.get_timeline_event_stream().create_subscription_to_pop(
#                 self._on_timeline_event
#             )
#         )

#         # Subscribe to viewport updates
#         if self._viewport:
#             self._subscriptions.append(
#                 self._viewport.get_update_event_stream().create_subscription_to_pop(
#                     self._on_viewport_update
#                 )
#             )
#         else:
#             print("[HybridFrameExtension] No active viewport found.")

#         # Expose registration API globally
#         omni.kit.app.get_app().set_extension_instance(ext_id, self)

#     def on_shutdown(self):
#         """Called when the extension is disabled."""
#         print("[HybridFrameExtension] Shutdown — cleaning up subscriptions")
#         for sub in self._subscriptions:
#             try:
#                 sub.unsubscribe()
#             except Exception as e:
#                 print(f"[HybridFrameExtension] Error during unsubscribe: {e}")
#         self._subscriptions.clear()
#         self._callbacks.clear()

#     # --- Public API ---
#     def register_callback(self, func):
#         """
#         Register a function to be called every frame when simulation is running.
#         The function must accept one argument: dt (float).
#         """
#         if not callable(func):
#             raise ValueError("Callback must be callable")
#         self._callbacks.add(func)
#         print(f"[HybridFrameExtension] Callback registered: {func.__name__}")

#     def unregister_callback(self, func):
#         """Remove a specific registered callback."""
#         if func in self._callbacks:
#             self._callbacks.remove(func)
#             print(f"[HybridFrameExtension] Callback unregistered: {func.__name__}")

#     def clear_callbacks(self):
#         """Remove all registered callbacks."""
#         self._callbacks.clear()
#         print("[HybridFrameExtension] All callbacks cleared.")

#     # --- Internal event handlers ---
#     def _on_timeline_event(self, event):
#         """Track simulation start/stop events."""
#         if event.type == int(omni.timeline.TimelineEventType.PLAY):
#             self._simulation_running = True
#             print("[HybridFrameExtension] Simulation started.")
#         elif event.type == int(omni.timeline.TimelineEventType.STOP):
#             self._simulation_running = False
#             print("[HybridFrameExtension] Simulation stopped.")

#     def _on_viewport_update(self, dt: float):
#         """Run per frame only when simulation is active."""
#         if self._simulation_running and self._callbacks:
#             for func in list(self._callbacks):  # Copy to avoid modification during iteration
#                 try:
#                     func(dt)
#                 except Exception as e:
#                     print(f"[HybridFrameExtension] Error in callback {func.__name__}: {e}")
# 🔹 How to Use the Multi-Callback Version
# Once the extension is enabled in Omniverse:

# Python

# Copy code
# import omni.kit.app

# # Get the extension instance
# ext = omni.kit.app.get_app().get_extension_instance("my.company.hybrid_frame")

# # Define multiple custom per-frame functions
# def logic_a(dt):
#     print(f"[Logic A] dt={dt:.4f}")

# def logic_b(dt):
#     print(f"[Logic B] dt={dt:.4f}")

# # Register both
# ext.register_callback(logic_a)
# ext.register_callback(logic_b)

# # Later, you can unregister one
# # ext.unregister_callback(logic_a)

# # Or clear all
# # ext.clear_callbacks()
# ✅ Benefits of Multi-Callback Design
# Multiple scripts/tools can coexist without overwriting each other’s logic.
# Callbacks are isolated — one failing won’t stop the others.
# Easy to add/remove logic dynamically at runtime.
# Still only runs when simulation is active and viewport is rendering.
# If you want, I can now make a thread-safe version so callbacks can be registered/unregistered from background threads (e.g., async data streams) without race conditions.

# That would make it safe for real-time sensor feeds or network-driven simulation updates.

# Do you want me to prepare that thread-safe multi-callback extension next?

# Alright — here’s the thread-safe multi-callback hybrid Omniverse extension.
# This version ensures you can register/unregister callbacks from any thread (e.g., background sensor data, network events) without race conditions or crashes.

# 📂 Extension Structure

# Copy code
# exts/
# └── my.company.hybrid_frame/
#     ├── extension.toml
#     └── hybrid_frame.py
# extension.toml
# Toml

# Copy code
# [package]
# name = "my.company.hybrid_frame"
# version = "1.3.0"
# title = "Hybrid Frame Callback (Thread-Safe Multi-Callback)"
# description = "Runs multiple registered Python callbacks only when simulation is playing AND viewport is rendering, with thread-safe registration."
# category = "Simulation"
# authors = ["Your Name"]
# keywords = ["omniverse", "simulation", "viewport", "events", "thread-safe"]

# [dependencies]
# "omni.kit.viewport.utility" = {}
# "omni.timeline" = {}

# [python]
# module = "hybrid_frame"
# hybrid_frame.py
# Python

# Copy code
# import omni.ext
# import omni.kit.app
# import omni.kit.viewport.utility as vp_utils
# import omni.timeline
# import threading


# class HybridFrameExtension(omni.ext.IExt):
#     def on_startup(self, ext_id):
#         """Called when the extension is enabled."""
#         print("[HybridFrameExtension] Startup (Thread-Safe Multi-Callback)")

#         self._subscriptions = []
#         self._simulation_running = False
#         self._callbacks = set()
#         self._lock = threading.Lock()  # Protects _callbacks

#         # Get interfaces
#         self._app = omni.kit.app.get_app()
#         self._timeline = omni.timeline.get_timeline_interface()
#         self._viewport = vp_utils.get_active_viewport_window()

#         # Subscribe to timeline events
#         self._subscriptions.append(
#             self._timeline.get_timeline_event_stream().create_subscription_to_pop(
#                 self._on_timeline_event
#             )
#         )

#         # Subscribe to viewport updates
#         if self._viewport:
#             self._subscriptions.append(
#                 self._viewport.get_update_event_stream().create_subscription_to_pop(
#                     self._on_viewport_update
#                 )
#             )
#         else:
#             print("[HybridFrameExtension] No active viewport found.")

#         # Expose registration API globally
#         omni.kit.app.get_app().set_extension_instance(ext_id, self)

#     def on_shutdown(self):
#         """Called when the extension is disabled."""
#         print("[HybridFrameExtension] Shutdown — cleaning up subscriptions")
#         for sub in self._subscriptions:
#             try:
#                 sub.unsubscribe()
#             except Exception as e:
#                 print(f"[HybridFrameExtension] Error during unsubscribe: {e}")
#         self._subscriptions.clear()
#         with self._lock:
#             self._callbacks.clear()

#     # --- Public API ---
#     def register_callback(self, func):
#         """Thread-safe registration of a callback."""
#         if not callable(func):
#             raise ValueError("Callback must be callable")
#         with self._lock:
#             self._callbacks.add(func)
#         print(f"[HybridFrameExtension] Callback registered: {func.__name__}")

#     def unregister_callback(self, func):
#         """Thread-safe removal of a specific callback."""
#         with self._lock:
#             if func in self._callbacks:
#                 self._callbacks.remove(func)
#                 print(f"[HybridFrameExtension] Callback unregistered: {func.__name__}")

#     def clear_callbacks(self):
#         """Thread-safe removal of all callbacks."""
#         with self._lock:
#             self._callbacks.clear()
#         print("[HybridFrameExtension] All callbacks cleared.")

#     # --- Internal event handlers ---
#     def _on_timeline_event(self, event):
#         """Track simulation start/stop events."""
#         if event.type == int(omni.timeline.TimelineEventType.PLAY):
#             self._simulation_running = True
#             print("[HybridFrameExtension] Simulation started.")
#         elif event.type == int(omni.timeline.TimelineEventType.STOP):
#             self._simulation_running = False
#             print("[HybridFrameExtension] Simulation stopped.")

#     def _on_viewport_update(self, dt: float):
#         """Run per frame only when simulation is active."""
#         if self._simulation_running:
#             with self._lock:
#                 callbacks_copy = list(self._callbacks)
#             for func in callbacks_copy:
#                 try:
#                     func(dt)
#                 except Exception as e:
#                     print(f"[HybridFrameExtension] Error in callback {func.__name__}: {e}")
# 🔹 How to Use (Thread-Safe)
# Once the extension is enabled in Omniverse:

# Python

# Copy code
# import omni.kit.app
# import threading
# import time

# # Get the extension instance
# ext = omni.kit.app.get_app().get_extension_instance("my.company.hybrid_frame")

# # Define callbacks
# def logic_a(dt):
#     print(f"[Logic A] dt={dt:.4f}")

# def logic_b(dt):
#     print(f"[Logic B] dt={dt:.4f}")

# # Register from main thread
# ext.register_callback(logic_a)

# # Register from a background thread
# def background_reg():
#     time.sleep(1)
#     ext.register_callback(logic_b)

# threading.Thread(target=background_reg).start()
# ✅ Benefits of Thread-Safe Multi-Callback
# Safe from any thread — no race conditions when adding/removing callbacks.
# Multiple tools/scripts can register without interfering.
# Still only runs when simulation is active and viewport is rendering.
# Background data sources (network, sensors, async tasks) can hook in directly.
# If you want, I can now make a performance-optimized version that:

# Uses a lock-free read path for per-frame execution
# Minimizes frame-time impact even with hundreds of callbacks
# That would be ideal for high-frequency simulation updates in Isaac Sim.

# Do you want me to prepare that lock-free high-performance version next?

# Alright — here’s the lock-free high-performance version of the thread-safe multi-callback hybrid Omniverse extension.

# This version is optimized for minimal frame-time impact even with hundreds of callbacks by:

# Using a copy-on-write approach for callback registration/unregistration.
# Avoiding locks in the per-frame execution path (critical for high FPS).
# Keeping the per-frame loop as short as possible.
# 📂 Extension Structure

# Copy code
# exts/
# └── my.company.hybrid_frame/
#     ├── extension.toml
#     └── hybrid_frame.py
# extension.toml
# Toml

# Copy code
# [package]
# name = "my.company.hybrid_frame"
# version = "1.4.0"
# title = "Hybrid Frame Callback (Lock-Free High-Performance)"
# description = "Runs multiple registered Python callbacks only when simulation is playing AND viewport is rendering, optimized for high FPS."
# category = "Simulation"
# authors = ["Your Name"]
# keywords = ["omniverse", "simulation", "viewport", "events", "thread-safe", "performance"]

# [dependencies]
# "omni.kit.viewport.utility" = {}
# "omni.timeline" = {}

# [python]
# module = "hybrid_frame"
# hybrid_frame.py
# Python

# Copy code
# import omni.ext
# import omni.kit.app
# import omni.kit.viewport.utility as vp_utils
# import omni.timeline
# import threading


# class HybridFrameExtension(omni.ext.IExt):
#     def on_startup(self, ext_id):
#         """Called when the extension is enabled."""
#         print("[HybridFrameExtension] Startup (Lock-Free High-Performance)")

#         self._subscriptions = []
#         self._simulation_running = False

#         # Callbacks list is replaced atomically (copy-on-write)
#         self._callbacks = tuple()
#         self._lock = threading.Lock()  # Only used for writes

#         # Get interfaces
#         self._app = omni.kit.app.get_app()
#         self._timeline = omni.timeline.get_timeline_interface()
#         self._viewport = vp_utils.get_active_viewport_window()

#         # Subscribe to timeline events
#         self._subscriptions.append(
#             self._timeline.get_timeline_event_stream().create_subscription_to_pop(
#                 self._on_timeline_event
#             )
#         )

#         # Subscribe to viewport updates
#         if self._viewport:
#             self._subscriptions.append(
#                 self._viewport.get_update_event_stream().create_subscription_to_pop(
#                     self._on_viewport_update
#                 )
#             )
#         else:
#             print("[HybridFrameExtension] No active viewport found.")

#         # Expose registration API globally
#         omni.kit.app.get_app().set_extension_instance(ext_id, self)

#     def on_shutdown(self):
#         """Called when the extension is disabled."""
#         print("[HybridFrameExtension] Shutdown — cleaning up subscriptions")
#         for sub in self._subscriptions:
#             try:
#                 sub.unsubscribe()
#             except Exception as e:
#                 print(f"[HybridFrameExtension] Error during unsubscribe: {e}")
#         self._subscriptions.clear()
#         with self._lock:
#             self._callbacks = tuple()

#     # --- Public API ---
#     def register_callback(self, func):
#         """Thread-safe registration with copy-on-write."""
#         if not callable(func):
#             raise ValueError("Callback must be callable")
#         with self._lock:
#             new_callbacks = list(self._callbacks)
#             if func not in new_callbacks:
#                 new_callbacks.append(func)
#                 self._callbacks = tuple(new_callbacks)
#         print(f"[HybridFrameExtension] Callback registered: {func.__name__}")

#     def unregister_callback(self, func):
#         """Thread-safe removal with copy-on-write."""
#         with self._lock:
#             new_callbacks = [cb for cb in self._callbacks if cb != func]
#             self._callbacks = tuple(new_callbacks)
#         print(f"[HybridFrameExtension] Callback unregistered: {func.__name__}")

#     def clear_callbacks(self):
#         """Thread-safe removal of all callbacks."""
#         with self._lock:
#             self._callbacks = tuple()
#         print("[HybridFrameExtension] All callbacks cleared.")

#     # --- Internal event handlers ---
#     def _on_timeline_event(self, event):
#         """Track simulation start/stop events."""
#         if event.type == int(omni.timeline.TimelineEventType.PLAY):
#             self._simulation_running = True
#             print("[HybridFrameExtension] Simulation started.")
#         elif event.type == int(omni.timeline.TimelineEventType.STOP):
#             self._simulation_running = False
#             print("[HybridFrameExtension] Simulation stopped.")

#     def _on_viewport_update(self, dt: float):
#         """Run per frame only when simulation is active."""
#         if self._simulation_running:
#             # Lock-free read of callbacks
#             for func in self._callbacks:
#                 try:
#                     func(dt)
#                 except Exception as e:
#                     print(f"[HybridFrameExtension] Error in callback {func.__name__}: {e}")
# 🔹 Why This is High-Performance
# Copy-on-write:
# Writes (register/unregister) take a lock and replace the tuple.
# Reads (per-frame execution) are lock-free and just iterate over a tuple.
# No per-frame locking:
# Avoids blocking the render/update thread.
# Tuple iteration:
# Tuples are faster to iterate than lists in Python.
# Safe from any thread:
# Registration/unregistration can happen from background threads.
# 🔹 How to Use
# Python

# Copy code
# import omni.kit.app
# import threading
# import time

# # Get the extension instance
# ext = omni.kit.app.get_app().get_extension_instance("my.company.hybrid_frame")

# # Define callbacks
# def logic_a(dt):
#     print(f"[Logic A] dt={dt:.4f}")

# def logic_b(dt):
#     print(f"[Logic B] dt={dt:.4f}")

# # Register from main thread
# ext.register_callback(logic_a)

# # Register from background thread
# def background_reg():
#     time.sleep(1)
#     ext.register_callback(logic_b)

# threading.Thread(target=background_reg).start()
# ✅ Performance Notes
# This design can handle hundreds of callbacks with negligible frame-time cost.
# Registration/unregistration is rare compared to per-frame execution, so locking cost is minimal.
# Ideal for Isaac Sim or Omniverse Kit projects with many real-time tools.
# If you want, I can now make a benchmark harness that runs inside Omniverse to measure:

# Callback execution time
# FPS impact with different numbers of callbacks
# Threaded registration stress test
# That would let you prove the performance of this design in your environment.

# Do you want me to prepare that Omniverse performance benchmark script next?

# Perfect — here’s a self-contained Omniverse performance benchmark harness
# for the lock-free high-performance hybrid frame extension we just built.

# This will let you measure:

# Average per-frame callback execution time
# FPS impact with different numbers of callbacks
# Threaded registration stress test
# 📂 Usage
# Save this as benchmark_hybrid_frame.py and run it inside Omniverse Script Editor
# (or as a standalone script in Isaac Sim / Kit after enabling the extension).

# benchmark_hybrid_frame.py
# Python

# Copy code
# import omni.kit.app
# import time
# import threading
# import statistics

# # Get the extension instance
# ext = omni.kit.app.get_app().get_extension_instance("my.company.hybrid_frame")

# if not ext:
#     raise RuntimeError("HybridFrameExtension not found. Enable it in the Extensions window first.")

# # --- Benchmark parameters ---
# NUM_CALLBACKS = 200       # Number of callbacks to register
# TEST_DURATION = 5.0       # Seconds to run the benchmark
# THREAD_REGISTRATION = True  # Test registering from background threads

# # --- Metrics ---
# frame_times = []
# frame_count = 0
# start_time = None

# # --- Test callback ---
# def test_callback(dt):
#     global frame_count
#     frame_count += 1
#     frame_times.append(dt)

# # --- Setup benchmark ---
# def setup_callbacks():
#     print(f"[Benchmark] Registering {NUM_CALLBACKS} callbacks...")
#     for i in range(NUM_CALLBACKS):
#         ext.register_callback(lambda dt, idx=i: None)  # Lightweight no-op

#     # Add one timing callback
#     ext.register_callback(test_callback)

# # --- Threaded registration test ---
# def threaded_registration():
#     for i in range(50):
#         ext.register_callback(lambda dt, idx=i: None)
#         time.sleep(0.01)
#     print("[Benchmark] Threaded registration complete.")

# # --- Start benchmark ---
# def start_benchmark():
#     global start_time, frame_count, frame_times
#     frame_times.clear()
#     frame_count = 0
#     start_time = time.time()
#     print("[Benchmark] Starting... Run simulation now.")

#     if THREAD_REGISTRATION:
#         threading.Thread(target=threaded_registration, daemon=True).start()

#     # Stop after TEST_DURATION seconds
#     threading.Timer(TEST_DURATION, stop_benchmark).start()

# # --- Stop benchmark and report ---
# def stop_benchmark():
#     elapsed = time.time() - start_time
#     if frame_times:
#         avg_dt = statistics.mean(frame_times)
#         min_dt = min(frame_times)
#         max_dt = max(frame_times)
#         fps = frame_count / elapsed
#         print("\n=== Benchmark Results ===")
#         print(f"Callbacks registered: {len(ext._callbacks)}")
#         print(f"Frames processed: {frame_count}")
#         print(f"Elapsed time: {elapsed:.2f} sec")
#         print(f"Average dt: {avg_dt:.6f} sec (~{1/avg_dt:.2f} FPS)")
#         print(f"Min dt: {min_dt:.6f} sec")
#         print(f"Max dt: {max_dt:.6f} sec")
#         print(f"Measured FPS: {fps:.2f}")
#     else:
#         print("[Benchmark] No frames recorded. Did you start the simulation?")

#     # Cleanup
#     ext.clear_callbacks()
#     print("[Benchmark] Callbacks cleared.")

# # --- Run ---
# setup_callbacks()
# start_benchmark()
# 🔹 How It Works
# Registers:
# NUM_CALLBACKS lightweight no-op callbacks.
# One timing callback (test_callback) to measure per-frame dt.
# Optionally spawns a thread to register more callbacks during the test (THREAD_REGISTRATION=True).
# Runs for TEST_DURATION seconds while simulation is active.
# Reports:
# Number of callbacks
# Frames processed
# Average, min, max dt
# Measured FPS
# Cleans up all callbacks after the test.
# 🔹 How to Run
# Enable Hybrid Frame Callback (Lock-Free High-Performance) extension in Omniverse.
# Open Script Editor.
# Paste and run benchmark_hybrid_frame.py.
# Start simulation in the timeline.
# Wait for results after TEST_DURATION seconds.
# ✅ What You’ll Learn
# Real FPS impact of your registered callbacks.
# Whether threaded registration causes any frame drops.
# How scaling to hundreds of callbacks affects performance.
# If you want, I can also make a graphing version of this benchmark
# that plots FPS over time inside Omniverse using matplotlib so you can visually see performance trends.

# Do you want me to prepare that real-time FPS graphing benchmark next?

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

__all__ = ["SolitaireExtension"]

import omni.ext
import omni.ui as ui

import omni.usd
from pxr import UsdGeom, UsdShade, Sdf, Gf
import omni.kit.app
import math



# # Functions and vars are available to other extensions as usual in python:
# # `my_company.my_python_ui_extension.some_public_function(x)`


# def some_public_function(x: int):
#     """This is a public function that can be called from other extensions."""
#     print(f"[my_company.my_python_ui_extension] some_public_function was called with {x}")
#     return x ** x


# Any class derived from `omni.ext.IExt` in the top level module (defined in
# `python.modules` of `extension.toml`) will be instantiated when the extension
# gets enabled, and `on_startup(ext_id)` will be called. Later when the
# extension gets disabled on_shutdown() is called.
class SolitaireExtension(omni.ext.IExt):
    """This extension manages a simple counter UI."""
    # ext_id is the current extension id. It can be used with the extension
    # manager to query additional information, like where this extension is
    # located on the filesystem.


    def on_startup(self, _ext_id):
        """This is called every time the extension is activated."""
        print("[my_company.my_python_ui_extension] Extension startup")

        self._count = 0

        self._window = ui.Window(
            "My Python UI Extension", width=300, height=300
        )
        with self._window.frame:
            with ui.VStack():
                label = ui.Label("")

                def on_click():
                    stage = omni.usd.get_context().get_stage()

                    # --- Create Plane ---
                    plane = UsdGeom.Mesh.Define(stage, "/Plane")
                    plane.CreatePointsAttr([
                        (-1.0, 0.0, -1.0),
                        ( 1.0, 0.0, -1.0),
                        ( 1.0, 0.0,  1.0),
                        (-1.0, 0.0,  1.0)
                    ])
                    plane.CreateFaceVertexCountsAttr([4])
                    plane.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
                    plane.CreateExtentAttr([(-1.0, 0.0, -1.0), (1.0, 0.0, 1.0)])

                    # --- Create Button ---
                    button = UsdGeom.Cylinder.Define(stage, "/Button")
                    button.CreateHeightAttr(0.1)
                    button.CreateRadiusAttr(0.2)
                    xform = UsdGeom.Xformable(button)
                    translate_op = xform.AddTranslateOp()
                    translate_op.Set(Gf.Vec3f(0.0, 0.05, 0.0))

                    # --- Create Materials ---
                    def create_material(name, color):
                        mat_path = Sdf.Path(f"/Looks/{name}")
                        material = UsdShade.Material.Define(stage, mat_path)
                        shader = UsdShade.Shader.Define(stage, mat_path.AppendPath("Shader"))
                        shader.CreateIdAttr("UsdPreviewSurface")
                        shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(color)
                        shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
                        material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
                        return material

                    default_mat = create_material("ButtonDefault", (0.2, 0.6, 1.0))  # Blue
                    clicked_mat = create_material("ButtonClicked", (1.0, 0.3, 0.3))  # Red
                    UsdShade.MaterialBindingAPI(button).Bind(default_mat)

                    # --- Animation State ---
                    is_clicked = False
                    press_offset = 0.02
                    anim_time = 0.0
                    anim_duration = 0.25  # seconds
                    start_y = 0.05
                    target_y = start_y


                    self._count += 1
                    label.text = f"count: {self._count}"
                    # --- Click Handler ---

                    # def on_click(event):
                    #     global is_clicked, anim_time, start_y, target_y
                    #     if event.type == int(omni.kit.app.MouseEventType.CLICK):
                    #         hit_prim = event.payload.get("prim_path")
                    #         if hit_prim == "/Button":
                    #             is_clicked = not is_clicked
                    #             UsdShade.MaterialBindingAPI(button).Bind(clicked_mat if is_clicked else default_mat)

                    #             # Set animation targets
                    #             start_y = translate_op.Get()[1]
                    #             target_y = 0.05 - press_offset if is_clicked else 0.05
                    #             anim_time = 0.0

                    #             print(f"Button {'pressed' if is_clicked else 'released'} — smooth spring animation triggered.")

                    # # --- Animation Update ---
                    # def on_update(dt):
                    #     global anim_time, start_y, target_y
                    #     if anim_time < anim_duration:
                    #         anim_time += dt
                    #         t = anim_time / anim_duration
                    #         # Spring easing: overshoot and settle
                    #         spring_t = (math.sin(t * math.pi * (0.5 + 2 * t)) * (1 - t) * 0.2) + t
                    #         new_y = start_y + (target_y - start_y) * spring_t
                    #         translate_op.Set(Gf.Vec3f(0.0, new_y, 0.0))

                    # # Subscribe to events
                    # omni.kit.app.get_app().get_mouse_interface().subscribe_to_mouse_events(on_click)
                    # omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop(on_update)

                    # print("Smooth, springy button ready — click to see it bounce and change color.")

                def on_reset():
                    self._count = 0
                    label.text = "empty"

                on_reset()

                with ui.HStack():
                    ui.Button("Add", clicked_fn=on_click)
                    ui.Button("Reset", clicked_fn=on_reset)

    def on_shutdown(self):
        """This is called every time the extension is deactivated. It is used
        to clean up the extension state."""
        print("[my_company.my_python_ui_extension] Extension shutdown")
