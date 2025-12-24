import omni.ext
import omni.kit.app
import omni.kit.viewport.utility as vp_utils
import omni.timeline
import threading

import omni.kit.app
import threading
import time

class JoystickHybridExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        """Called when the extension is enabled."""
        print("[JoystickExtension] Startup (Lock-Free High-Performance)")

        #ext = omni.kit.app.get_app().get_extension_instance("my.company.hybrid_frame")
        #ext = omni.kit.app.get_app().get_extension_manager().get_extensions()

        # get all registered local extensions (enabled and disabled)
        manager = omni.kit.app.get_app().get_extension_manager()
        for ext in manager.get_extensions():
            print(ext["id"], ext["package_id"], ext["name"], ext["version"], ext["path"], ext["enabled"])

        # Define callbacks
        def logic_a(dt):
            print(f"[Logic A] dt={dt:.4f}")

        def logic_b(dt):
            print(f"[Logic B] dt={dt:.4f}")

        # Register from main thread
        ext.register_callback(logic_a)

        # Register from background thread
        def background_reg():
            time.sleep(1)
            ext.register_callback(logic_b)

        threading.Thread(target=background_reg).start()


    # def on_shutdown(self):
    #     """Called when the extension is disabled."""
    #     print("[HybridFrameExtension] Shutdown — cleaning up subscriptions")
    #     for sub in self._subscriptions:
    #         try:
    #             sub.unsubscribe()
    #         except Exception as e:
    #             print(f"[HybridFrameExtension] Error during unsubscribe: {e}")
    #     self._subscriptions.clear()
    #     with self._lock:
    #         self._callbacks = tuple()


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
