import {{ python_module }}
import omni.kit.test
import time


class Test(omni.kit.test.AsyncTestCaseFailOnLogError):
    async def test_manager_register_and_heartbeat(self):
        mgr = {{ python_module }}.JoystickManager()
        events = []

        def cb(e):
            events.append(e)

        mgr.register_callback(cb)
        mgr.start()
        # give it a short moment to produce heartbeat events when no hardware present
        await omni.kit.test.wait_until(lambda: len(events) >= 1, timeout=2.0)
        mgr.stop()
        self.assertGreaterEqual(len(events), 1)
