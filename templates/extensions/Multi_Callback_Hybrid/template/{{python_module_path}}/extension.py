import omni.ext
import omni.kit.app
import omni.kit.viewport.utility as vp_utils
import omni.timeline
import threading

class HybridFrameExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        """Called when the extension is enabled."""
        print("[HybridFrameExtension] Startup (Lock-Free High-Performance)")

        self._subscriptions = []
        self._simulation_running = False

        # Callbacks list is replaced atomically (copy-on-write)
        self._callbacks = tuple()
        self._lock = threading.Lock()  # Only used for writes

        # Get interfaces
        self._app = omni.kit.app.get_app()
        self._timeline = omni.timeline.get_timeline_interface()
        self._viewport = vp_utils.get_active_viewport_window()

        # Subscribe to timeline events
        self._subscriptions.append(
            self._timeline.get_timeline_event_stream().create_subscription_to_pop(
                self._on_timeline_event
            )
        )

        # Subscribe to viewport updates
        if self._viewport:
            self._subscriptions.append(
                self._viewport.get_update_event_stream().create_subscription_to_pop(
                    self._on_viewport_update
                )
            )
        else:
            print("[HybridFrameExtension] No active viewport found.")

        # Expose registration API globally
        omni.kit.app.get_app().set_extension_instance(ext_id, self)

    def on_shutdown(self):
        """Called when the extension is disabled."""
        print("[HybridFrameExtension] Shutdown — cleaning up subscriptions")
        for sub in self._subscriptions:
            try:
                sub.unsubscribe()
            except Exception as e:
                print(f"[HybridFrameExtension] Error during unsubscribe: {e}")
        self._subscriptions.clear()
        with self._lock:
            self._callbacks = tuple()

    # --- Public API ---
    def register_callback(self, func):
        """Thread-safe registration with copy-on-write."""
        if not callable(func):
            raise ValueError("Callback must be callable")
        with self._lock:
            new_callbacks = list(self._callbacks)
            if func not in new_callbacks:
                new_callbacks.append(func)
                self._callbacks = tuple(new_callbacks)
        print(f"[HybridFrameExtension] Callback registered: {func.__name__}")

    def unregister_callback(self, func):
        """Thread-safe removal with copy-on-write."""
        with self._lock:
            new_callbacks = [cb for cb in self._callbacks if cb != func]
            self._callbacks = tuple(new_callbacks)
        print(f"[HybridFrameExtension] Callback unregistered: {func.__name__}")

    def clear_callbacks(self):
        """Thread-safe removal of all callbacks."""
        with self._lock:
            self._callbacks = tuple()
        print("[HybridFrameExtension] All callbacks cleared.")

    # --- Internal event handlers ---
    def _on_timeline_event(self, event):
        """Track simulation start/stop events."""
        if event.type == int(omni.timeline.TimelineEventType.PLAY):
            self._simulation_running = True
            print("[HybridFrameExtension] Simulation started.")
        elif event.type == int(omni.timeline.TimelineEventType.STOP):
            self._simulation_running = False
            print("[HybridFrameExtension] Simulation stopped.")

    def _on_viewport_update(self, dt: float):
        """Run per frame only when simulation is active."""
        if self._simulation_running:
            # Lock-free read of callbacks
            for func in self._callbacks:
                try:
                    func(dt)
                except Exception as e:
                    print(f"[HybridFrameExtension] Error in callback {func.__name__}: {e}")


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
