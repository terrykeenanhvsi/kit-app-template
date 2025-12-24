import omni.ext
import omni.kit.app
import omni.kit.viewport.utility as vp_utils
import omni.timeline
import threading
import time
import socket
import omni.appwindow
import carb.input
from carb.input import KeyboardEventType
#import omni
#import carb

class JoystickHybridExtension(omni.ext.IExt):

    # def __init__(self):
    #     super().__init__()
    #     self._lock = threading.Lock()
    #     self._callbacks = tuple()
    #     self._subscriptions = []
    #     # self.bus = omni.kit.app.get_app().get_message_bus_event_stream()
    #     # self.MY_CUSTOM_EVENT = carb.events.type_from_string("my.custom.event")
    #     # self.sub1 = self.bus.create_subscription_to_push_by_type(self.MY_CUSTOM_EVENT, self.on_event)
    #     # self.sub2 = self.bus.create_subscription_to_pop_by_type(self.MY_CUSTOM_EVENT, self.on_event)

    def on_keyboard_input(self, e):
        if e.input == carb.input.KeyboardInput.W:
            if e.type == KeyboardEventType.KEY_PRESS or e.type == KeyboardEventType.KEY_REPEAT:
                self.handle_key_pressed(e.input)
            elif e.type == KeyboardEventType.KEY_RELEASE:
                self.handle_key_released(e.input)

    def handle_key_pressed(self, e):
            print("Keyboard W Pressed")
            (x,y) = self.input.get_mouse_coords_pixel(self.mouse)
            print(f"##################### get_mouse_coords_pixel : {x,y}")
            (x, y) = self.input.get_mouse_coords_normalized(self.mouse)
            print(f"##################### get_mouse_coords_normalized : {x, y}")
            # self.bus.push(MY_CUSTOM_EVENT, payload={"data": 5, "x": "y"})


    def handle_key_released(self, e):
            print("Keyboard W Released")
            (x,y) = self.input.get_mouse_coords_pixel(self.mouse)
            print(f"##################### get_mouse_coords_pixel : {x,y}")
            (x, y) = self.input.get_mouse_coords_normalized(self.mouse)
            print(f"##################### get_mouse_coords_normalized : {x, y}")
            # self.bus.push(self.MY_CUSTOM_EVENT, payload={"data": 5, "x": "y"})

    # def on_event(self, e):
    #     #print(e.type, e.type == self.MY_CUSTOM_EVENT, e.payload)
    #     print("[JoystickExtension] Custom event")


    def on_startup(self, ext_id):
        """Called when the extension is enabled ."""
        print("[JoystickExtension] Startup (Lock-Free High-Performance)")

       # Event is unique integer id. Create it from string by hashing, using helper function.
        # [ext name].[event name] is a recommended naming convention:
        # MY_CUSTOM_EVENT = carb.events.type_from_string("omni.my.extension.MY_CUSTOM_EVENT")

        # App provides common event bus. It is event queue which is popped every update (frame).
        # self.bus = omni.kit.app.get_app().get_message_bus_event_stream()

        # def on_event(e):
        #     print(e.type, e.type == self.MY_CUSTOM_EVENT, e.payload)
        #     print("[JoystickExtension] Custom event")

        # Subscribe to the bus. Keep subscription objects (sub1, sub2) alive for subscription to work.
        # Push to queue is called immediately when pushed
        # self.sub1 = self.bus.create_subscription_to_push_by_type(self.MY_CUSTOM_EVENT, on_event)
        # Pop is called on next update
        # self.sub2 = self.bus.create_subscription_to_pop_by_type(self.MY_CUSTOM_EVENT, on_event)

        # Push event the bus with custom payload
        # bus.push(MY_CUSTOM_EVENT, payload={"data": 5, "z": "w"})
        #self.bus.push(self.MY_CUSTOM_EVENT, payload={"data": 4, "x": "y"})

        # Mouse input
        self.input = carb.input.acquire_input_interface()
        self.mouse = omni.appwindow.get_default_app_window().get_mouse()

        # Keyborad input
        app_window = omni.appwindow.get_default_app_window()
        self.keyboard = app_window.get_keyboard()
        input = carb.input.acquire_input_interface()
        self.keyboard_sub_id = input.subscribe_to_keyboard_events(self.keyboard, self.on_keyboard_input)

        # UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(('localhost', 12444))

        # ext = omni.kit.app.get_app().get_extension_instance("my.company.hybrid_frame")
        # Get the extension manager
        ext_manager = omni.kit.app.get_app().get_extension_manager()

        # Retrieve all registered extensions
        extensions = ext_manager.get_extensions()

        # # Print extension info

        for ext_id, ext_info in enumerate(extensions):
            print(f"ID: {ext_id}")
            print(f"  Name: {ext_info.get('name')}")
            print(f"  Version: {ext_info.get('version')}")
            print(f"  Path: {ext_info.get('path')}")
            print(f"  Enabled: {ext_info.get('enabled')}")
            print("-" * 40)
            if ext_info.get('name') == 'my_company.multi_callback_hybrid':
                hybrid_ext_id = ext_id

            # ID: 400
            #   Name: my_company.multi_callback_hybrid
            #   Version: (0, 1, 0, '', '')
            #   Path: c:/terry/nvidia_training/kit-app-template/_build/windows-x86_64/release/exts/my_company.multi_callback_hybrid
            #   Enabled: False

        # Define callbacks
        def logic_a(dt):
            print(f"[Logic A] dt={dt:.4f}")

        def logic_b(dt):
            print(f"[Logic B] dt={dt:.4f}")


        # Register from main thread
        # hybrid_ext_id.register_callback(logic_a)

        # callback_id = omni.kit.commands.register_callback("*", logic_a)

        # Register from background thread
        def background_reg():
            time.sleep(1)
            # hybrid_ext_id.register_callback(logic_b)

        # threading.Thread(target=background_reg).start()

    def on_shutdown(self):
        """Called when the extension is disabled."""
        print("[HybridFrameExtension] Shutdown — cleaning up subscriptions")

        # input = carb.input.acquire_input_interface()
        # self.keyboard = app_window.get_keyboard()
        # input.unsubscribe_to_keyboard_events(keyboard, self.keyboard_sub_id)

        # or just...
        self.keyboard_sub_id = None

        for sub in self._subscriptions:
            try:
                sub.unsubscribe()
            except Exception as e:
                print(f"[HybridFrameExtension] Error during unsubscribe: {e}")
        self._subscriptions.clear()
        with self._lock:
            self._callbacks = tuple()


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
