import omni.ext
import omni.ui as ui
import omni.kit.commands # New
import omni.usd # New
from typing import List # New

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MyExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[dli.example.command_library] MyExtension startup")

        self._window = ui.Window("My Window", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                ui.Label("Prim Scaler")

                def on_click():
                    self.stage = omni.usd.get_context().get_stage()
                    ctx = omni.usd.get_context()
                    selection = ctx.get_selection()
                    selected_paths = selection.get_selected_prim_paths()
                    for p in selected_paths:
                        omni.kit.commands.execute('ScaleIncrement', prim_paths=p)

                ui.Button("Scale up!", clicked_fn=lambda: on_click())

    def on_shutdown(self):
        print("[dli.example.command_library] MyExtension shutdown")
        self._window.destroy()
        self._window = None

class ScaleIncrement(omni.kit.commands.Command):
    def __init__(self, prim_paths: str):
        self.stage = omni.usd.get_context().get_stage()
        self.prim_paths = prim_paths
        self.prim = self.stage.GetPrimAtPath(prim_paths)
        # TODO: Replace FIXME below
        self.scale_attribute = self.prim.GetAttribute('xformOp:scale')

    def do(self):
        self.set_scale()
        return self.scale_attribute.Get() # Optional Result

    def undo(self):
        self.set_scale(True)

    def set_scale(self, undo: bool=False):
        old_scale = self.scale_attribute.Get()
        new_scale = tuple(x + 1 for x in old_scale)
        if undo:
            new_scale = tuple(x - 1 for x in old_scale)
        self.scale_attribute.Set(new_scale)