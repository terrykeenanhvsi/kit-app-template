import omni.usd
from pxr import UsdGeom, UsdShade, Sdf, Gf
import omni.kit.app
import math

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

# --- Animation Update ---
def on_update(dt):
    global anim_time, start_y, target_y
    if anim_time < anim_duration:
        anim_time += dt
        t = anim_time / anim_duration
        # Spring easing: overshoot and settle
        spring_t = (math.sin(t * math.pi * (0.5 + 2 * t)) * (1 - t) * 0.2) + t
        new_y = start_y + (target_y - start_y) * spring_t
        translate_op.Set(Gf.Vec3f(0.0, new_y, 0.0))

# --- Click Handler ---
def on_click(event):
    global is_clicked, anim_time, start_y, target_y
    if event.type == int(omni.kit.app.MouseEventType.CLICK):
        hit_prim = event.payload.get("prim_path")
        if hit_prim == "/Button":
            is_clicked = not is_clicked
            UsdShade.MaterialBindingAPI(button).Bind(clicked_mat if is_clicked else default_mat)

            # Set animation targets
            start_y = translate_op.Get()[1]
            target_y = 0.05 - press_offset if is_clicked else 0.05
            anim_time = 0.0

            print(f"Button {'pressed' if is_clicked else 'released'} — smooth spring animation triggered.")

# Subscribe to events
omni.kit.app.get_app().get_mouse_interface().subscribe_to_mouse_events(on_click)
omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop(on_update)

print("Smooth, springy button ready — click to see it bounce and change color.")
