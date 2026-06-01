import asyncio
import math
from pydoc import text
import omni.usd
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.ext
import omni.ui as ui
import omni.ui.scene as sc
from pxr import UsdGeom, Gf
from .style import scatter_window_style
from .utils import get_selection
from .combo_box_model import ComboBoxModel
from .scatter import scatter
from .utils import duplicate_prims
from .PlanetLoader import PlanetLoader
from .CalendarLoader import CalendarLoader
from pxr import UsdGeom, Gf
from datetime import datetime, timedelta

import omni.kit.viewport.utility as vp_utils
from omni.kit.widget.viewport.capture import FileCapture
from omni.kit.viewport.utility import create_viewport_window
from omni.kit.async_engine import run_coroutine
import omni.kit.app
import os
import asyncio
import omni.kit.app

Calendar = CalendarLoader()
Planets = PlanetLoader()

import omni
import omni.usd
from pxr import Sdf
import omni.kit.commands

from pxr import Usd, Sdf
from omni.usd import get_context
import numpy as np
import csv
import random

LABEL_WIDTH = 120
SPACING = 4
# OmniUILabel = ui.Label

# import omni.ui as ui

# class LabelExample:
# def __init__(self):
# self._window = ui.Window("Omni UI Label Example", width=300, height=200)
# with self._window.frame:
# with ui.VStack():
# ui.Label("Selected Prim Path:")
# self.label = ui.Label("No prim selected")

# def update_label(self, prim_path):
# self.label.text = f"Prim Path: {prim_path}"

# # Instantiate and update the label
# example = LabelExample()
# example.update_label("/World/MyPrim")

class ScatterWindow(ui.Window):
    """The class that represents the window"""

    # Example async function
    async def load_stage_async(self):
        # import omni.usd
        # stage_url = "omniverse://localhost/Users/test/scene.usd"
        # print("Loading stage...")
        # await omni.usd.get_context().open_stage_async(stage_url)
        # print("Stage loaded!")
        # viewport_window = create_viewport_window("Viewport Camera", width=800, height=600)
        viewport_window = vp_utils.get_active_viewport_window()
        viewport_api = viewport_window.viewport_api

        await asyncio.sleep(1)

        image_path = "C:/Terry/NVIDIA_Training/First_Project/Data/Calander_Dataoutput.png"
        capture = viewport_api.schedule_capture(FileCapture(image_path))
        captured_aovs = await capture.wait_for_result()

        if captured_aovs:
            print(f'AOV "{captured_aovs[0]}" saved to "{image_path}"')
        else:
            print("No image was written.")

        return "Done"

    def __init__(self, title: str, delegate=None, **kwargs):
        self.__label_width = LABEL_WIDTH

        super().__init__(title, **kwargs)

        viewport_window = vp_utils.get_active_viewport_window()
        output_path = "C:\\Terry\\NVIDIA_Training\\First_Project\\Data\\screenshot.png"
        #  viewport_window.screenshot(output_path, resolution=(1920, 1080))

        # omni.kit.viewport.utility.capture_viewport_to_file(
        #     viewport_api,
        #     file_path: str | Sequence[str] = None,
        #     is_hdr: bool = False,
        #     render_product_path: str = None,
        #     format_desc: dict = None,
        #     frame_to_capture=None,
        #     )

        self.Deck_Position = np.zeros(80, dtype=int)
        self.Deck_Cut_Left = np.zeros(80, dtype=int)
        self.Deck_Cut_Middle = np.zeros(80, dtype=int)
        self.Deck_Cut_Right = np.zeros(80, dtype=int)
        self.Deck_Temp = np.zeros(80, dtype=int)
        self.test_deck = np.zeros(80, dtype=int)
        self.rows = []
        self.count = 0
        self.count_Left = 0
        self.count_Right = 0
        self.count_Temp = 0
        self.Slider_Value = 38
        self.Slider_Value1 = 50
        self.Slider_Value2 = 50
        self.SliderLeft_Value1 = 180
        self.SliderRight_Value2 = 180
        self.SliderDay_Value = 6
        self.Stack1Button = None
        self.Stack2Button = None
        self.Stack3Button = None
        self.AspectButton = None
        self.GoodButton = None
        self.BadButton = None
        self.StackCombine = 0
        self.Load_Point = 1
        self.Calander_Days = 1
        self.TestDay = 28
        self.TestMonth = 2
        self.TestYear = 1959



        # Define the data and data types
        data = [('Alice', 25, 55.0), ('Bob', 32, 60.5)]
        dtypes = [('name', 'U10'), ('age', 'i4'), ('weight', 'f4')]

        # Create the structured array
        people = np.array(data, dtype=dtypes)

        # Accessing and modifying structured arrays
        print(people['name']) # Output: ['Alice' 'Bob']
        people['age'] += 1
        print(people['age']) # Output: [26 33]

        # self.Checkout()

        # # Generate 5 unique random integers between 0 and 100
        # random_numbers = random.sample(range(1, 79), 78)
        # print(random_numbers)

        # Planets.sun_diff = 3.3

        self.Calander_Days = 2
        # for i in range(1, self.Calander_Days + 1):  # for i in range(1, 14):  # 1..13
        #     # self.today = self.today.strftime("%Y-%m-%d")
        #     self.today = datetime.now()
        #     self.terry = datetime(1959, 2, 28)
        #     self.default = datetime(1959, 2, 28)
        #     self.target_date = datetime.now() + timedelta(days=i-1)

        #     Planets.start(self.SliderLeft_Value1, self.SliderRight_Value2, self.default, self.target_date, i, 0)
        #     #Planets.start(341.1492844, 332.7710469)


        print("PlanetLoader Test Sun Diff: ", Planets.sun_diff)
        print("CalendarLoader Test Sun Diff: ", Calendar.sun_diff)

        # for item in self.Deck_Position:
        #     print(item)

        # # Define the dtype
        #     dtype = [('name', 'U10'), ('age', 'i4'), ('height', 'f4')]

        #     # Define the data
        #     data = [('Alice', 30, 5.6), ('Bob', 25, 5.8), ('Charlie', 35, 5.9)]

        #     # Create the structured array
        #     structured_array = np.array(data, dtype=dtype)

        #     print("Structured Array:\n", structured_array)

       # with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
        #     csvFile = csv.DictReader(file)
        #     #for lines in csvFile:
        #     #   print(lines)



        # omni.kit.commands.execute('CreateMeshPrimWithDefaultXform',
        #     prim_type='Plane',
        #     prim_path='/World/Plane',
        #     select_new_prim=True,
        #     prepend_default_prim=False,
        #     above_ground=True)

        # omni.kit.commands.execute('CreateAndBindMdlMaterialFromLibrary',
        #     mdl_name='OmniPBR.mdl',
        #     mtl_name='OmniPBR',
        #     mtl_created_list=['/World/Looks/OmniPBR'],
        #     bind_selected_prims=['/World/Plane'],
        #     prim_name='OmniPBR')

        # stage = get_context().get_stage()
        # if not stage:
        #     print("❌ No USD stage loaded.")


        # material_prim = stage.GetPrimAtPath('/World/Looks/OmniPBR')
        # if not material_prim.IsValid():
        #     print(f"❌ Material not found at {'/World/Looks/OmniPBR'}")

        # shader_path = Sdf.Path("./World/Looks/OmniPBR/Shader")
        # shader_prim = stage.GetPrimAtPath(shader_path)
        # if not shader_prim.IsValid():
        #     print(f"❌ Shader not found at {'./World/Looks/OmniPBR/Shader'}")

        # shader = None
        # for rel in material_prim.GetRelationships():
        #     if "surface" in rel.GetName().lower():
        #         targets = rel.GetTargets()
        #         if targets:
        #             shader_prim = stage.GetPrimAtPath(str(targets[0]))
        #             if shader_prim.IsValid():
        #                 shader = shader_prim
        #                 break

        # if not shader:
        #     print(f"❌ No shader found for material {'/World/Looks/OmniPBR'}")


        # omni.kit.commands.execute('ChangePropertyCommand',
        #     prop_path=Sdf.Path('/World/Looks/OmniPBR/Shader.inputs:diffuse_texture'),
        #     value=Sdf.AssetPath('C:/Terry/NVIDIA_Training/First_Project/Assets/Textures/Tarot/1910/TheChariot.png'),
        #     prev=Sdf.AssetPath(''))

        # omni.kit.commands.execute('ChangeProperty',
        #     prop_path=Sdf.Path('/World/Looks/OmniPBR/Shader.inputs:diffuse_texture'),
        #     value=Sdf.AssetPath('C:/Terry/NVIDIA_Training/First_Project/Assets/Textures/Tarot/1910/TheChariot.png'),
        #     prev=None,
        #     target_layer=Sdf.Find('anon:00000170D1884160:World0.usd'),
        #     usd_context_name=omni.usd.get_context().get_stage())

        # Models
        self._source_prim_model = ui.SimpleStringModel()
        self._scatter_prim_model = ui.SimpleStringModel()
        self._scatter_type_model = ComboBoxModel("Reference", "Copy", "PointInstancer")
        self._scatter_seed_model = ui.SimpleIntModel()
        self._scatter_count_models = [ui.SimpleIntModel(), ui.SimpleIntModel(), ui.SimpleIntModel()]
        self._scatter_distance_models = [ui.SimpleFloatModel(), ui.SimpleFloatModel(), ui.SimpleFloatModel()]
        self._scatter_random_models = [ui.SimpleFloatModel(), ui.SimpleFloatModel(), ui.SimpleFloatModel()]
        self._scale_models = [ui.SimpleFloatModel(), ui.SimpleFloatModel(), ui.SimpleFloatModel()]
       # Defaults
        self._scatter_prim_model.as_string = "/World/Scatter01"
        self._scatter_count_models[0].as_int = 15
        self._scatter_count_models[1].as_int = 1
        self._scatter_count_models[2].as_int = 1
        self._scatter_distance_models[0].as_float = 10
        self._scatter_distance_models[1].as_float = 10
        self._scatter_distance_models[2].as_float = 10
        self._scale_models[0].as_float = 1
        self._scale_models[1].as_float = 1
        self._scale_models[2].as_float = 1
        self.input_sliderLeft = None
        self.input_sliderRight = None
        self.sliderLeft = None
        self.sliderRight = None
        self.selabel_ref = None
        self.Sun_Label = None
        self.Moon_Label = None
        self.Mercury_Label = None
        self.Venus_Label = None
        self.Mars_Label = None
        self.Jupiter_Label = None
        self.Saturn_Label = None
        self.Uranus_Label = None
        self.Neptune_Label = None
        self.Pluto_Label = None
        self.Marker_Label = None
        self.sliderDay = None
        self.input_sliderDay = None


        # Apply the style to all the widgets of this window
        self.frame.style = scatter_window_style
        # Set the function that is called to build widgets when the window is
        # visible
        self.frame.set_build_fn(self._build_fn)

    #     # Create a SceneView in the viewport
    #     self._scene_view = sc.SceneView()

    #     with self._scene_view.scene:
    #         # Position the UI in 3D space
    #         with sc.Transform(transform=sc.Matrix44.get_translation_matrix(0, 1, 0)):
    #             with sc.Label("Hello Omniverse!", alignment=ui.Alignment.CENTER):
    #                 pass

    # def on_shutdown(self):
    #     print("[MySceneUIExtension] Shutdown")
    #     self._scene_view = None

    def _build_fn(self):
        """
        The method that is called to build all the UI once the window is
        visible.
        """

        # Create a simple window
        self._window = ui.Window("My UI Frame Example", width=300, height=150)

        # Build the UI inside the window
        with self._window.frame:
            with ui.VStack(spacing=10, height=0):
                # Add a frame with a label inside
                with ui.Frame(height=50, style={"background_color": 0xFF202020}):
                    ui.Label(
                        "Hello Omniverse!",
                        alignment=ui.Alignment.CENTER,
                        style={"color": 0xFFFFFFFF, "font_size": 18}
                    )

            # Another label outside the frame
            ui.Label("This is outside the frame", style={"color": 0xFFAAAAAA})

        with ui.CollapsableFrame("Entanglement Tarot", name="group"):
            with ui.ScrollingFrame():
                with ui.VStack(height=0):
                    with ui.HStack(style={"margin": 1}, visible=True):

                        self.input_sliderLeft = ui.IntField()
                        self.input_sliderLeft.model.set_value(self.sliderLeft)
                        self.input_sliderLeft.model.add_value_changed_fn(lambda m: self.on_input_sliderLeft_changed(self.input_sliderLeft))

                        self.sliderLeft = ui.UIntSlider(min=1, max=360, step=1)
                        self.sliderLeft.model.set_value(180)  # Set initial value
                        self.sliderLeft.model.add_value_changed_fn(lambda m: self.on_sliderLeft_changed(self.sliderLeft))

                    with ui.HStack(style={"margin": 1}, visible=True):

                        self.input_sliderRight = ui.IntField()
                        self.input_sliderRight.model.set_value(self.sliderRight)
                        self.input_sliderRight.model.add_value_changed_fn(lambda m: self.on_input_sliderRight_changed(self.input_sliderRight))

                        self.sliderRight = ui.UIntSlider(min=1, max=360, step=1)
                        self.sliderRight.model.set_value(180)  # Set initial value
                        self.sliderRight.model.add_value_changed_fn(lambda m: self.on_sliderRight_changed(self.sliderRight))

                    # The Go button
                    ui.Button("Shuffle", clicked_fn=self._on_scatter)
                    # Create the UIntSlider
                    slider = ui.UIntSlider(min=1, max=78, step=1)
                    slider.model.set_value(50)  # Set initial value
                    slider.model.add_value_changed_fn(lambda m: self.on_slider_changed(slider))
                    self._build_Cut_Deck()
                    self._build_Card_Layout()
                    self._build_Calendar_Frame()
                    self._build_Chakra_Frame()
                    self._build_Chakra_Natal_Frame()
                    self._build_Chakra_Sign_Frame()
                    # self._build_source()
                    #self._build_scatter()
                    #self._build_axis(0, "X Axis")
                    #self._build_axis(1, "Y Axis")
                    #self._build_axis(2, "Z Axis")


    async def take_screenshot(file_path: str):
        """
        Capture a screenshot from the active viewport in Omniverse Kit.

        Args:
            file_path (str): Full path where the screenshot will be saved.
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Get the active viewport window
            viewport = vp_utils.get_active_viewport_window()
            if viewport is None:
                print("❌ No active viewport found.")
                return

            # Capture the screenshot asynchronously
            await viewport.viewport_api.capture_image(file_path)
            print(f"✅ Screenshot saved to: {file_path}")

        except Exception as e:
            print(f"❌ Failed to take screenshot: {e}")

    # Entry point for Omniverse async execution
    async def main():
        # Save screenshot to user's home directory
        output_path = os.path.expanduser("~/omniverse_screenshot.png")
        #await self.take_screenshot(output_path)

    @property
    def label_width(self):
        """The width of the attribute label"""
        return self.__label_width

    @label_width.setter
    def label_width(self, value):
        """The width of the attribute label"""
        self.__label_width = value
        self.frame.rebuild()

    def destroy(self):
        # It will destroy all the children
        super().destroy()

    def change_label_text(self):
        """
        Change the label text using omni.kit.commands.execute.
        The built-in command is 'ChangeProperty'.
        """
        omni.kit.commands.execute(
            "ChangeProperty",
            prop_path=self.label.widget.text,  # Property to change
            value="Updated Text"               # New value
        )

   # Callback function for slider value changes
    def on_slider_changed(self, slider):
        self.Slider_Value = slider.model.get_value_as_int()
        print(f"Slider value changed to: {self.Slider_Value}")

    def on_sliderLeft_changed(self, sliderLeft):
        self.SliderLeft_Value1 = sliderLeft.model.get_value_as_int()
        self.input_sliderLeft.model.set_value(int(self.SliderLeft_Value1))
        # print(f"Slider Left value changed to: {self.SliderLeft_Value1}")

    def on_sliderDay_changed(self, sliderDay):
        self.SliderDay_Value = sliderDay.model.get_value_as_int()
        self.calander_Day.model.set_value(int(self.SliderDay_Value))
        # print(f"Slider Day value changed to: {self.SliderDay_Value}")

    def on_sliderRight_changed(self, sliderRight):
        self.SliderRight_Value2 = sliderRight.model.get_value_as_int()
        self.input_sliderRight.model.set_value(int(self.SliderRight_Value2))

    def on_input_sliderLeft_changed(self, input):
        value = input.model.get_value_as_int()
        value = max(self.sliderLeft.min, min(self.sliderLeft.max, value))
        self.sliderLeft.model.set_value(value)

    def on_input_sliderDay_changed(self, input):
        value = input.model.get_value_as_int()
        value = max(self.sliderDay.min, min(self.sliderDay.max, value))
        self.sliderDay.model.set_value(value)

    def on_input_sliderRight_changed(self, input):
        value = input.model.get_value_as_int()
        value = max(self.sliderRight.min, min(self.sliderRight.max, value))
        self.sliderRight.model.set_value(value)

    def _build_Cut_Deck(self):
        """Build the widgets of the "Cut Deck" group"""
        with ui.CollapsableFrame("Cut Deck", name="group"):
            with ui.VStack(height=0, spacing=SPACING):

                self.slider1 = ui.UIntSlider(min=1, max=78, step=1)
                self.slider1.model.set_value(50)  # Set initial value
                self.slider1.model.add_value_changed_fn(lambda m: self.on_slider_cut1(self.slider1))

                self.slider2 = ui.UIntSlider(min=1, max=78, step=1)
                self.slider2.model.set_value(50)  # Set initial value
                self.slider2.model.add_value_changed_fn(lambda m: self.on_slider_cut2(self.slider2))

                ui.Button("Cut Three Stacks", clicked_fn=self._on_cut_deck)

                with ui.HStack():
                    self.Stack1Button = ui.Button(
                        "Stack 1",
                        visible=False,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_stack1,
                        tooltip="Three Card Layout",
                    )
                    self.Stack2Button = ui.Button(
                        "Stack 2",
                        visible=False,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_stack2,
                        tooltip="Collider Layout",
                    )
                    self.Stack3Button = ui.Button(
                        "Stack 3",
                        visible=False,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_stack3,
                        tooltip="Chakra Layout",
                    )

    def _build_Card_Layout(self):
        """Build the widgets of the "Layout" group"""
        with ui.CollapsableFrame("Layout", name="group"):
            with ui.VStack(height=0, spacing=SPACING):
                ui.Button("Three_Card", clicked_fn=self._on_three_card_current)
                ui.Button("Collider", clicked_fn=self._on_collider_current)
                ui.Button("Chakra", clicked_fn=self._on_chakra_current)

    def _build_Chakra_Frame(self):
        """Build the widgets of the "Layout" group"""
        with ui.CollapsableFrame("Chakra Current Totals", name="group"):
            with ui.VStack(height=0, spacing=SPACING):
                with ui.HStack():
                    self.AspectButton = ui.Button(
                        "Total",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_total_aspect,
                        tooltip="Total Aspect",
                    )
                    self.GoodButton = ui.Button(
                        "Good",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_good_aspect,
                        tooltip="Total Good Aspect",
                    )
                    self.BadButton = ui.Button(
                        "Bad",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_bad_aspect,
                        tooltip="Total Bad Aspect",
                    )
                with ui.HStack():
                    self.ConjuctButton = ui.Button(
                        "Conjuct",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_conjunct_aspect,
                        tooltip="Total Conjuct Aspect",
                    )
                    self.SextileButton = ui.Button(
                        "Sextile",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_sextile_aspect,
                        tooltip="Total Sextile Aspect",
                    )
                    self.SquareButton = ui.Button(
                        "Square",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_square_aspect,
                        tooltip="Total Square Aspect",
                    )
                with ui.HStack():
                    self.TrineButton = ui.Button(
                        "Trine",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_trine_aspect,
                        tooltip="Total Trine Aspect",
                    )
                    self.OppositeButton = ui.Button(
                        "Opposite",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_opposite_aspect,
                        tooltip="Total Opposite Aspect",
                    )
                with ui.VStack(height=0, spacing=SPACING):
                    # Create a label with text  "Hello, Omniverse!
                    self.Sun_Label = ui.Label(str(Planets.sun.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)
                    self.Moon_Label = ui.Label(str(Planets.moon.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)
                    self.Mercury_Label = ui.Label(str(Planets.mercury.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)
                    self.Venus_Label = ui.Label(str(Planets.venus.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Mars_Label = ui.Label(str(Planets.mars.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Jupiter_Label = ui.Label(str(Planets.jupiter.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Saturn_Label = ui.Label(str(Planets.saturn.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Uranus_Label = ui.Label(str(Planets.uranus.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Neptune_Label = ui.Label(str(Planets.neptune.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Pluto_Label = ui.Label(str(Planets.pluto.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Marker_Label = ui.Label(str(Planets.marker.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)


                    ui.Label("Initial Text", height=20, style={"color": 0xFF00FF00})  # Static label
                    self.selabel_ref = ui.Label("Waiting...", height=20, style={"color": 0xFFFFFFFF})


                    # Another label with wrapping enabled
                    ui.Label("This is a longer label that will wrap automatically "
                            "if the window is too narrow.",
                            word_wrap=True,
                            style={"color": 0xFFFFFFFF, "font_size": 14})

    def _on_total_aspect(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Total Aspect Selected')
        self.Sun_Label.text = str("Sun : " + str(round(Planets.sun.total_aspect, 2)) + " S: " + str(round(Planets.current_planets_2[0].house, 2))) + " D: " +str(round(Planets.current_planets_2[0].degree * 30, 2))
        self.Moon_Label.text = str("Moon : " + str(round(Planets.moon.total_aspect, 2)) + " S: " + str(round(Planets.current_planets_2[1].house, 2))) + " D: " +str(round(Planets.current_planets_2[1].degree * 30, 2))
        self.Mercury_Label.text = str("Mercury : " + str(round(Planets.mercury.total_aspect, 2)) + " S: " + str(round(Planets.current_planets_2[2].house, 2))) + " D: " +str(round(Planets.current_planets_2[2].degree * 30, 2))
        self.Venus_Label.text = str("Venus : " + str(round(Planets.venus.total_aspect, 2)) + " S: " + str(round(Planets.current_planets_2[3].house, 2))) + " D: " +str(round(Planets.current_planets_2[3].degree * 30, 2))
        self.Mars_Label.text = str("Mars : " + str(round(Planets.mars.total_aspect, 2)) + " S: " + str(round(Planets.current_planets_2[4].house, 2))) + " D: " +str(round(Planets.current_planets_2[4].degree * 30, 2))
        self.Jupiter_Label.text = str("Jupiter : " + str(round(Planets.jupiter.total_aspect, 2)) + " S: " + str(round(Planets.current_planets_2[5].house, 2))) + " D: " +str(round(Planets.current_planets_2[5].degree * 30, 2))
        self.Saturn_Label.text = str("Saturn : " + str(round(Planets.saturn.total_aspect, 2)) + " S: " + str(round(Planets.current_planets_2[6].house, 2))) + " D: " +str(round(Planets.current_planets_2[6].degree * 30, 2))
        self.Uranus_Label.text = str("Uranus : " + str(round(Planets.uranus.total_aspect, 2)) + " S: " + str(round(Planets.current_planets_2[7].house, 2))) + " D: " +str(round(Planets.current_planets_2[7].degree * 30, 2))
        self.Neptune_Label.text = str("Neptune : " + str(round(Planets.neptune.total_aspect, 2)) + " S: " + str(round(Planets.current_planets_2[8].house, 2))) + " D: " +str(round(Planets.current_planets_2[8].degree * 30, 2))
        self.Pluto_Label.text = str("Pluto : " + str(round(Planets.pluto.total_aspect, 2)) + " S: " + str(round(Planets.current_planets_2[9].house, 2))) + " D: " +str(round(Planets.current_planets_2[9].degree * 30, 2))
        self.Marker_Label.text = str("Marker : " + str(round(Planets.marker.total_aspect, 2)))

    def _on_good_aspect(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Good Aspect Selected')
        self.Sun_Label.text = str("Sun : " + str(round(Planets.sun.total_good, 2)))
        self.Moon_Label.text = str("Moon : " + str(round(Planets.moon.total_good, 2)))
        self.Mercury_Label.text = str("Mercury : " + str(round(Planets.mercury.total_good, 2)))
        self.Venus_Label.text = str("Venus : " + str(round(Planets.venus.total_good, 2)))
        self.Mars_Label.text = str("Mars : " + str(round(Planets.mars.total_good, 2)))
        self.Jupiter_Label.text = str("Jupiter : " + str(round(Planets.jupiter.total_good, 2)))
        self.Saturn_Label.text = str("Saturn : " + str(round(Planets.saturn.total_good, 2)))
        self.Uranus_Label.text = str("Uranus : " + str(round(Planets.uranus.total_good, 2)))
        self.Neptune_Label.text = str("Neptune : " + str(round(Planets.neptune.total_good, 2)))
        self.Pluto_Label.text = str("Pluto : " + str(round(Planets.pluto.total_good, 2)))
        self.Marker_Label.text = str("Marker : " + str(round(Planets.marker.total_good, 2)))

    def _on_bad_aspect(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Bad Aspect Selected')
        self.Sun_Label.text = str("Sun : " + str(round(Planets.sun.total_bad, 2)))
        self.Moon_Label.text = str("Moon : " + str(round(Planets.moon.total_bad, 2)))
        self.Mercury_Label.text = str("Mercury : " + str(round(Planets.mercury.total_bad, 2)))
        self.Venus_Label.text = str("Venus : " + str(round(Planets.venus.total_bad, 2)))
        self.Mars_Label.text = str("Mars : " + str(round(Planets.mars.total_bad, 2)))
        self.Jupiter_Label.text = str("Jupiter : " + str(round(Planets.jupiter.total_bad, 2)))
        self.Saturn_Label.text = str("Saturn : " + str(round(Planets.saturn.total_bad, 2)))
        self.Uranus_Label.text = str("Uranus : " + str(round(Planets.uranus.total_bad, 2)))
        self.Neptune_Label.text = str("Neptune : " + str(round(Planets.neptune.total_bad, 2)))
        self.Pluto_Label.text = str("Pluto : " + str(round(Planets.pluto.total_bad, 2)))
        self.Marker_Label.text = str("Marker : " + str(round(Planets.marker.total_bad, 2)))

    def _on_conjunct_aspect(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Conjunct Aspect Selected')
        self.Sun_Label.text = str("Sun : " + str(round(Planets.sun.total_conjunct, 2)))
        self.Moon_Label.text = str("Moon : " + str(round(Planets.moon.total_conjunct, 2)))
        self.Mercury_Label.text = str("Mercury : " + str(round(Planets.mercury.total_conjunct, 2)))
        self.Venus_Label.text = str("Venus : " + str(round(Planets.venus.total_conjunct, 2)))
        self.Mars_Label.text = str("Mars : " + str(round(Planets.mars.total_conjunct, 2)))
        self.Jupiter_Label.text = str("Jupiter : " + str(round(Planets.jupiter.total_conjunct, 2)))
        self.Saturn_Label.text = str("Saturn : " + str(round(Planets.saturn.total_conjunct, 2)))
        self.Uranus_Label.text = str("Uranus : " + str(round(Planets.uranus.total_conjunct, 2)))
        self.Neptune_Label.text = str("Neptune : " + str(round(Planets.neptune.total_conjunct, 2)))
        self.Pluto_Label.text = str("Pluto : " + str(round(Planets.pluto.total_conjunct, 2)))
        self.Marker_Label.text = str("Marker : " + str(round(Planets.marker.total_conjunct, 2)))

    def _on_sextile_aspect(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Sextile Aspect Selected')
        self.Sun_Label.text = str("Sun : " + str(round(Planets.sun.total_sextile, 2)))
        self.Moon_Label.text = str("Moon : " + str(round(Planets.moon.total_sextile, 2)))
        self.Mercury_Label.text = str("Mercury : " + str(round(Planets.mercury.total_sextile, 2)))
        self.Venus_Label.text = str("Venus : " + str(round(Planets.venus.total_sextile, 2)))
        self.Mars_Label.text = str("Mars : " + str(round(Planets.mars.total_sextile, 2)))
        self.Jupiter_Label.text = str("Jupiter : " + str(round(Planets.jupiter.total_sextile, 2)))
        self.Saturn_Label.text = str("Saturn : " + str(round(Planets.saturn.total_sextile, 2)))
        self.Uranus_Label.text = str("Uranus : " + str(round(Planets.uranus.total_sextile, 2)))
        self.Neptune_Label.text = str("Neptune : " + str(round(Planets.neptune.total_sextile, 2)))
        self.Pluto_Label.text = str("Pluto : " + str(round(Planets.pluto.total_sextile, 2)))
        self.Marker_Label.text = str("Marker : " + str(round(Planets.marker.total_sextile, 2)))

    def _on_square_aspect(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Square Aspect Selected')
        self.Sun_Label.text = str("Sun : " + str(round(Planets.sun.total_square, 2)))
        self.Moon_Label.text = str("Moon : " + str(round(Planets.moon.total_square, 2)))
        self.Mercury_Label.text = str("Mercury : " + str(round(Planets.mercury.total_square, 2)))
        self.Venus_Label.text = str("Venus : " + str(round(Planets.venus.total_square, 2)))
        self.Mars_Label.text = str("Mars : " + str(round(Planets.mars.total_square, 2)))
        self.Jupiter_Label.text = str("Jupiter : " + str(round(Planets.jupiter.total_square, 2)))
        self.Saturn_Label.text = str("Saturn : " + str(round(Planets.saturn.total_square, 2)))
        self.Uranus_Label.text = str("Uranus : " + str(round(Planets.uranus.total_square, 2)))
        self.Neptune_Label.text = str("Neptune : " + str(round(Planets.neptune.total_square, 2)))
        self.Pluto_Label.text = str("Pluto : " + str(round(Planets.pluto.total_square, 2)))
        self.Marker_Label.text = str("Marker : " + str(round(Planets.marker.total_square, 2)))

    def _on_trine_aspect(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Trine Aspect Selected')
        self.Sun_Label.text = str("Sun : " + str(round(Planets.sun.total_trine, 2)))
        self.Moon_Label.text = str("Moon : " + str(round(Planets.moon.total_trine, 2)))
        self.Mercury_Label.text = str("Mercury : " + str(round(Planets.mercury.total_trine, 2)))
        self.Venus_Label.text = str("Venus : " + str(round(Planets.venus.total_trine, 2)))
        self.Mars_Label.text = str("Mars : " + str(round(Planets.mars.total_trine, 2)))
        self.Jupiter_Label.text = str("Jupiter : " + str(round(Planets.jupiter.total_trine, 2)))
        self.Saturn_Label.text = str("Saturn : " + str(round(Planets.saturn.total_trine, 2)))
        self.Uranus_Label.text = str("Uranus : " + str(round(Planets.uranus.total_trine, 2)))
        self.Neptune_Label.text = str("Neptune : " + str(round(Planets.neptune.total_trine, 2)))
        self.Pluto_Label.text = str("Pluto : " + str(round(Planets.pluto.total_trine, 2)))
        self.Marker_Label.text = str("Marker : " + str(round(Planets.marker.total_trine, 2)))

    def _on_opposite_aspect(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Opposite Aspect Selected')
        self.Sun_Label.text = str("Sun : " + str(round(Planets.sun.total_opposite, 2)))
        self.Moon_Label.text = str("Moon : " + str(round(Planets.moon.total_opposite, 2)))
        self.Mercury_Label.text = str("Mercury : " + str(round(Planets.mercury.total_opposite, 2)))
        self.Venus_Label.text = str("Venus : " + str(round(Planets.venus.total_opposite, 2)))
        self.Mars_Label.text = str("Mars : " + str(round(Planets.mars.total_opposite, 2)))
        self.Jupiter_Label.text = str("Jupiter : " + str(round(Planets.jupiter.total_opposite, 2)))
        self.Saturn_Label.text = str("Saturn : " + str(round(Planets.saturn.total_opposite, 2)))
        self.Uranus_Label.text = str("Uranus : " + str(round(Planets.uranus.total_opposite, 2)))
        self.Neptune_Label.text = str("Neptune : " + str(round(Planets.neptune.total_opposite, 2)))
        self.Pluto_Label.text = str("Pluto : " + str(round(Planets.pluto.total_opposite, 2)))
        self.Marker_Label.text = str("Marker : " + str(round(Planets.marker.total_opposite, 2)))

    # # Async function to update the label text periodically
    # async def update_label():
    #     counter = 0
    #     while True:
    #         await asyncio.sleep(1)  # Wait 1 second
    #         counter += 1
    #         if selabel_ref:
    #             selabel_ref.text = f"Updated {counter} times"

    def _build_Calendar_Frame(self):
        """Build the widgets of the "Layout" group"""
        with ui.CollapsableFrame("Calander_frame", name="group"):
            with ui.VStack(height=0, spacing=SPACING):
                with ui.HStack():

                    self.calander_Day = ui.IntField()
                    self.calander_Day.model.set_value(self.sliderDay)
                    self.calander_Day.model.add_value_changed_fn(lambda m: self.on_input_sliderDay_changed(self.calander_Day))

                    self.sliderDay = ui.UIntSlider(min=1, max=31, step=1)
                    self.sliderDay.model.set_value(6)  # Set initial value
                    self.sliderDay.model.add_value_changed_fn(lambda m: self.on_sliderDay_changed(self.sliderDay))

                with ui.HStack():

                    self.Calander_button = ui.Button(
                        "Run",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_calander,
                        tooltip="Calander_Frame",
                    )

                    self.OneCard_button = ui.Button(
                        "One Card",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_one_card_calander,
                        tooltip="One Card Calander",
                    )

                    self.threeCard_button = ui.Button(
                        "Three Card",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_three_card_calander,
                        tooltip="Three Card Calander",
                    )

                with ui.HStack():

                    self.collider_button = ui.Button(
                        "Collider",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_collider_calander,
                        tooltip="Collider Calander",
                    )

                    self.chakra_button = ui.Button(
                        "Chakra",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_chakra_calander,
                        tooltip="Chakra Calander",
                    )
                with ui.VStack(height=0, spacing=SPACING):
                    self.Mind_Label = ui.Label(str(Planets.Mind),
                                    style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                    alignment=ui.Alignment.LEFT_CENTER)
                    self.Body_Label = ui.Label(str(Planets.Body),
                                    style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                    alignment=ui.Alignment.LEFT_CENTER)
                    self.Spirit_Label = ui.Label(str(Planets.Spirit),
                                    style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                    alignment=ui.Alignment.LEFT_CENTER)
                    self.Mind_cur_Label = ui.Label(str(Planets.Mind_cur),
                                    style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                    alignment=ui.Alignment.LEFT_CENTER)
                    self.Body_cur_Label = ui.Label(str(Planets.Body_cur),
                                    style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                    alignment=ui.Alignment.LEFT_CENTER)
                    self.Spirit_cur_Label = ui.Label(str(Planets.Spirit_cur),
                                    style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                    alignment=ui.Alignment.LEFT_CENTER)

    # def on_calander_day_changed(self, model):
    #     try:
    #         value = model.get_value()  # You can also use as_float for decimal numbers
    #         print(f"User entered number: {value}")
    #     except Exception as e:
    #         print(f"Invalid input: {e}")

    def _on_calander(self):
        """Called when the user presses the "Get From Selection" button"""
        #print('Calander Day: ')

        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
            csvFileCalander = csv.reader(file)
            self.rowsCalander = list(csvFileCalander)
            # print(self.rows[5][3])
            # for i in range(80):  # for i in range(1, 14):  # 1..13
            #     if(self.count == 0): self.Deck_Temp[self.count] = 0
            #     else:  self.Deck_Temp[self.count] = int(self.rowsCalander[self.count][3])
            #     # print(self.rowsCalander[self.count][3])
            #     # print(self.Deck_Position[self.count])
            #     # print(self.count)
            #     self.count += 1

        self.Calander_Days = 5 #self.SliderDay_Value
        for k in range(3, 10):  # for i in range(1, 14):  # 1..13

            Planets.Calander_1_card.clear()
            Planets.Calander_3_card.clear()
            Planets.Calander_13_card.clear()
            Planets.Calander_22_card.clear()

            for i in range(3):
                Planets.calander_layout = 0
                self.Slider_Value = 34
                self._on_scatter()

            Planets.Calander_layout = 1
            self.Slider_Value = 72
            self._on_scatter()

            for i in range(3):
                Planets.Calander_layout = 0
                self.Slider_Value = 44
                self._on_scatter()

            Planets.Calander_layout = 3
            self.Slider_Value = 33
            self._on_scatter()

            for i in range(3):
                Planets.Calander_layout = 0
                self.Slider_Value = 48
                self._on_scatter()

            Planets.Calander_layout = 13
            self.Slider_Value = 65
            self._on_scatter()

            for i in range(3):
                Planets.Calander_layout = 0
                self.Slider_Value = 38
                self._on_scatter()

            Planets.Calander_layout = 22
            self.Slider_Value = 44
            self._on_scatter()

            # self.today = self.today.strftime("%Y-%m-%d")
            self.today = datetime.now()
            self.terry = datetime(1959, 2, 28)
            self.default = datetime(1959, 2, 28)
            self.target_date = datetime.now() + timedelta(days = k - 3)

            self.BirthText = self.rowsCalander[9][1]
            self.birthParts = self.BirthText.split('/')
            self.birthMonth = int(self.birthParts[0])
            self.birthDay = int(self.birthParts[1])
            self.birthYear = int(self.birthParts[2])

            self.birthdayDate = datetime(self.birthYear, self.birthMonth, self.birthDay)
            self.default = self.birthdayDate

            self.TestDay = self.target_date.day
            self.TestMonth = self.target_date.month
            self.TestYear = self.target_date.year

            Planets.start(self.SliderLeft_Value1, self.SliderRight_Value2, self.default, self.target_date, k, Planets.Calander_layout)
            #Planets.start(341.1492844, 332.7710469)

            #self.sync_function()

            #omni.kit.app.get_app().next_update_async(self.main())
            #print('Calander Day: ')


    def _build_Chakra_Natal_Frame(self):
        """Build the widgets of the "Layout" group"""
        with ui.CollapsableFrame("Chakra Natal Totals", name="group"):
            with ui.VStack(height=0, spacing=SPACING):
                with ui.HStack():
                    self.AspectButtonNatal = ui.Button(
                        "Total",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_total_natal_aspect,
                        tooltip="Total Aspect",
                    )
                    self.GoodButtonNatal = ui.Button(
                        "Good",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_good_natal_aspect,
                        tooltip="Total Good Aspect",
                    )
                    self.BadButtonNatal = ui.Button(
                        "Bad",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_bad_natal_aspect,
                        tooltip="Total Bad Aspect",
                    )
                with ui.HStack():
                    self.ConjuctButtonNatal = ui.Button(
                        "Conjuct",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_conjunct_natal_aspect,
                        tooltip="Total Conjuct Aspect",
                    )
                    self.SextileButtonNatal  = ui.Button(
                        "Sextile",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_sextile_natal_aspect,
                        tooltip="Total Sextile Aspect",
                    )
                    self.SquareButtonNatal = ui.Button(
                        "Square",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_square_natal_aspect,
                        tooltip="Total Square Aspect",
                    )
                with ui.HStack():
                    self.TrineButtonNatal = ui.Button(
                        "Trine",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_trine_aspect,
                        tooltip="Total Trine Aspect",
                    )
                    self.OppositeButtonNatal = ui.Button(
                        "Opposite",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_opposite_aspect,
                        tooltip="Total Opposite Aspect",
                    )
                with ui.VStack(height=0, spacing=SPACING):
                    # Create a label with text  "Hello, Omniverse!
                    self.Sun_LabelNatal = ui.Label(str(Planets.sun_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)
                    self.Moon_LabelNatal = ui.Label(str(Planets.moon_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)
                    self.Mercury_LabelNatal = ui.Label(str(Planets.mercury_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)
                    self.Venus_LabelNatal = ui.Label(str(Planets.venus_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Mars_LabelNatal = ui.Label(str(Planets.mars_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Jupiter_LabelNatal = ui.Label(str(Planets.jupiter_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Saturn_LabelNatal = ui.Label(str(Planets.saturn_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Uranus_LabelNatal = ui.Label(str(Planets.uranus_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Neptune_LabelNatal = ui.Label(str(Planets.neptune_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Pluto_LabelNatal = ui.Label(str(Planets.pluto_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Marker_LabelNatal = ui.Label(str(Planets.marker_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)


                    ui.Label("Initial Text", height=20, style={"color": 0xFF00FF00})  # Static label
                    self.selabel_ref = ui.Label("Waiting...", height=20, style={"color": 0xFFFFFFFF})


                    # Another label with wrapping enabled
                    ui.Label("This is a longer label that will wrap automatically "
                            "if the window is too narrow.",
                            word_wrap=True,
                            style={"color": 0xFFFFFFFF, "font_size": 14})

    def _build_Chakra_Sign_Frame(self):
        """Build the widgets of the "Layout" group"""
        with ui.CollapsableFrame("Chakra Sign Totals", name="group"):
            with ui.VStack(height=0, spacing=SPACING):
                with ui.HStack():
                    self.AspectButtonSign = ui.Button(
                        "Sign Total",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_total_sign,
                        tooltip="Total Aspect",
                    )
                    self.GoodButtonSign = ui.Button(
                        "Natal",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_natal_sign,
                        tooltip="Total Natal Aspect",
                    )
                    self.BadButtonSign = ui.Button(
                        "Current",
                        visible=True,
                        enabled=True,
                        width=100,
                        height=0,
                        style={"margin": 5},
                        clicked_fn=self._on_current_sign,
                        tooltip="Total Current Aspect",
                    )
                with ui.VStack(height=0, spacing=SPACING):
                    # Create a label with text  "Hello, Omniverse!
                    self.Aries_LabelSign = ui.Label(str(Planets.sun_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Taurus_LabelSign = ui.Label(str(Planets.moon_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Gemini_LabelSign = ui.Label(str(Planets.mercury_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Cancer_LabelSign = ui.Label(str(Planets.venus_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Leo_LabelSign = ui.Label(str(Planets.mars_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Virgo_LabelSign = ui.Label(str(Planets.jupiter_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Libra_LabelSign = ui.Label(str(Planets.saturn_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Scorpio_LabelSign = ui.Label(str(Planets.uranus_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)
                    self.Sagittarius_LabelSign = ui.Label(str(Planets.neptune_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Capricorn_LabelSign = ui.Label(str(Planets.pluto_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Aquarius_LabelSign = ui.Label(str(Planets.marker_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    self.Pisces_LabelSign = ui.Label(str(Planets.marker_cur.total_aspect),
                                        style={"color": 0xFF00FF00,  # ARGB format (Green text)
                                    "font_size": 20},    # Font size in points
                                        alignment=ui.Alignment.LEFT_CENTER)

                    ui.Label("Initial Text", height=20, style={"color": 0xFF00FF00})  # Static label
                    self.selabel_ref = ui.Label("Waiting...", height=20, style={"color": 0xFFFFFFFF})


                    # Another label with wrapping enabled
                    ui.Label("This is a longer label that will wrap automatically "
                            "if the window is too narrow.",
                            word_wrap=True,
                            style={"color": 0xFFFFFFFF, "font_size": 14})

    def _on_total_sign(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Total Aspect Selected')
        self.Aries_LabelSign.text = str("Aries : " + str(round(Planets.Aries + Planets.Aries_cur, 2)))
        self.Taurus_LabelSign.text = str("Taurus : " + str(round(Planets.Taurus + Planets.Taurus_cur, 2)))
        self.Gemini_LabelSign.text = str("Gemini : " + str(round(Planets.Gemini + Planets.Gemini_cur, 2)))
        self.Cancer_LabelSign.text = str("Cancer : " + str(round(Planets.Cancer + Planets.Cancer_cur, 2)))
        self.Leo_LabelSign.text = str("Leo : " + str(round(Planets.Leo + Planets.Leo_cur, 2)))
        self.Virgo_LabelSign.text = str("Virgo : " + str(round(Planets.Virgo + Planets.Virgo_cur, 2)))
        self.Libra_LabelSign.text = str("Libra : " + str(round(Planets.Libra + Planets.Libra_cur, 2)))
        self.Scorpio_LabelSign.text = str("Scorpio : " + str(round(Planets.Scorpio + Planets.Scorpio_cur, 2)))
        self.Sagittarius_LabelSign.text = str("Sagittarius : " + str(round(Planets.Sagittarius + Planets.Sagittarius_cur, 2)))
        self.Capricorn_LabelSign.text = str("Capricorn : " + str(round(Planets.Capricorn + Planets.Capricorn_cur, 2)))
        self.Aquarius_LabelSign.text = str("Aquarius : " + str(round(Planets.Aquarius + Planets.Aquarius_cur, 2)))
        self.Pisces_LabelSign.text = str("Pisces : " + str(round(Planets.Pisces + Planets.Pisces_cur, 2)))

    def _on_natal_sign(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Total Aspect Selected')
        self.Aries_LabelSign.text = str("Aries : " + str(round(Planets.Aries, 2)))
        self.Taurus_LabelSign.text = str("Taurus : " + str(round(Planets.Taurus, 2)))
        self.Gemini_LabelSign.text = str("Gemini : " + str(round(Planets.Gemini, 2)))
        self.Cancer_LabelSign.text = str("Cancer : " + str(round(Planets.Cancer, 2)))
        self.Leo_LabelSign.text = str("Leo : " + str(round(Planets.Leo, 2)))
        self.Virgo_LabelSign.text = str("Virgo : " + str(round(Planets.Virgo, 2)))
        self.Libra_LabelSign.text = str("Libra : " + str(round(Planets.Libra, 2)))
        self.Scorpio_LabelSign.text = str("Scorpio : " + str(round(Planets.Scorpio, 2)))
        self.Sagittarius_LabelSign.text = str("Sagittarius : " + str(round(Planets.Sagittarius, 2)))
        self.Capricorn_LabelSign.text = str("Capricorn : " + str(round(Planets.Capricorn, 2)))
        self.Aquarius_LabelSign.text = str("Aquarius : " + str(round(Planets.Aquarius, 2)))
        self.Pisces_LabelSign.text = str("Pisces : " + str(round(Planets.Pisces, 2)))

    def _on_current_sign(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Total Aspect Selected')
        self.Aries_LabelSign.text = str("Aries : " + str(round(Planets.Aries_cur, 2)))
        self.Taurus_LabelSign.text = str("Taurus : " + str(round(Planets.Taurus_cur, 2)))
        self.Gemini_LabelSign.text = str("Gemini : " + str(round(Planets.Gemini_cur, 2)))
        self.Cancer_LabelSign.text = str("Cancer : " + str(round(Planets.Cancer_cur, 2)))
        self.Leo_LabelSign.text = str("Leo : " + str(round(Planets.Leo_cur, 2)))
        self.Virgo_LabelSign.text = str("Virgo : " + str(round(Planets.Virgo_cur, 2)))
        self.Libra_LabelSign.text = str("Libra : " + str(round(Planets.Libra_cur, 2)))
        self.Scorpio_LabelSign.text = str("Scorpio : " + str(round(Planets.Scorpio_cur, 2)))
        self.Sagittarius_LabelSign.text = str("Sagittarius : " + str(round(Planets.Sagittarius_cur, 2)))
        self.Capricorn_LabelSign.text = str("Capricorn : " + str(round(Planets.Capricorn_cur, 2)))
        self.Aquarius_LabelSign.text = str("Aquarius : " + str(round(Planets.Aquarius_cur, 2)))
        self.Pisces_LabelSign.text = str("Pisces : " + str(round(Planets.Pisces_cur, 2)))

    def _on_total_natal_aspect(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Total Aspect Selected')
        self.Sun_LabelNatal.text = str("Sun P: " + str(round(Planets.sun_cur.total_aspect, 2)) + " S: " + str(round(Planets.natal_planets[0].house, 2))) + " D: " +str(round(Planets.natal_planets[0].degree * 30, 2))
        self.Moon_LabelNatal.text = str("Moon P: " + str(round(Planets.moon_cur.total_aspect, 2)) + " S: " + str(round(Planets.natal_planets[1].house, 2))) + " D: " +str(round(Planets.natal_planets[1].degree * 30, 2))
        self.Mercury_LabelNatal.text = str("Mercury P: " + str(round(Planets.mercury_cur.total_aspect, 2)) + " S: " + str(round(Planets.natal_planets[2].house, 2))) + " D: " +str(round(Planets.natal_planets[2].degree * 30, 2))
        self.Venus_LabelNatal.text = str("Venus P: " + str(round(Planets.venus_cur.total_aspect, 2)) + " S: " + str(round(Planets.natal_planets[3].house, 2))) + " D: " +str(round(Planets.natal_planets[3].degree * 30, 2))
        self.Mars_LabelNatal.text = str("Mars P: " + str(round(Planets.mars_cur.total_aspect, 2)) + " S: " + str(round(Planets.natal_planets[4].house, 2))) + " D: " +str(round(Planets.natal_planets[4].degree * 30, 2))
        self.Jupiter_LabelNatal.text = str("Jupiter P: " + str(round(Planets.jupiter_cur.total_aspect, 2)) + " S: " + str(round(Planets.natal_planets[5].house, 2))) + " D: " +str(round(Planets.natal_planets[5].degree * 30, 2))
        self.Saturn_LabelNatal.text = str("Saturn P: " + str(round(Planets.saturn_cur.total_aspect, 2)) + " S: " + str(round(Planets.natal_planets[6].house, 2))) + " D: " +str(round(Planets.natal_planets[6].degree * 30, 2))
        self.Uranus_LabelNatal.text = str("Uranus P: " + str(round(Planets.uranus_cur.total_aspect, 2)) + " S: " + str(round(Planets.natal_planets[7].house, 2))) + " D: " +str(round(Planets.natal_planets[7].degree * 30, 2))
        self.Neptune_LabelNatal.text = str("Neptune P: " + str(round(Planets.neptune_cur.total_aspect, 2)) + " S: " + str(round(Planets.natal_planets[8].house, 2))) + " D: " +str(round(Planets.natal_planets[8].degree * 30, 2))
        self.Pluto_LabelNatal.text = str("Pluto P: " + str(round(Planets.pluto_cur.total_aspect, 2)) + " S: " + str(round(Planets.natal_planets[9].house, 2))) + " D: " +str(round(Planets.natal_planets[9].degree * 30, 2))
        self.Marker_LabelNatal.text = str("Marker P: " + str(round(Planets.marker_cur.total_aspect, 2)))

    def _on_good_natal_aspect(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Good Aspect Selected')
        self.Sun_LabelNatal.text = str("Sun : " + str(round(Planets.sun_cur.total_good, 2)))
        self.Moon_LabelNatal.text = str("Moon : " + str(round(Planets.moon_cur.total_good, 2)))
        self.Mercury_LabelNatal.text = str("Mercury : " + str(round(Planets.mercury_cur.total_good, 2)))
        self.Venus_LabelNatal.text = str("Venus : " + str(round(Planets.venus_cur.total_good, 2)))
        self.Mars_LabelNatal.text = str("Mars : " + str(round(Planets.mars_cur.total_good, 2)))
        self.Jupiter_LabelNatal.text = str("Jupiter : " + str(round(Planets.jupiter_cur.total_good, 2)))
        self.Saturn_LabelNatal.text = str("Saturn : " + str(round(Planets.saturn_cur.total_good, 2)))
        self.Uranus_LabelNatal.text = str("Uranus : " + str(round(Planets.uranus_cur.total_good, 2)))
        self.Neptune_LabelNatal.text = str("Neptune : " + str(round(Planets.neptune_cur.total_good, 2)))
        self.Pluto_LabelNatal.text = str("Pluto : " + str(round(Planets.pluto_cur.total_good, 2)))
        self.Marker_LabelNatal.text = str("Marker : " + str(round(Planets.marker_cur.total_good, 2)))

    def _on_bad_natal_aspect(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Bad Aspect Selected')
        self.Sun_LabelNatal.text = str("Sun : " + str(round(Planets.sun_cur.total_bad, 2)))
        self.Moon_LabelNatal.text = str("Moon : " + str(round(Planets.moon_cur.total_bad, 2)))
        self.Mercury_LabelNatal.text = str("Mercury : " + str(round(Planets.mercury_cur.total_bad, 2)))
        self.Venus_LabelNatal.text = str("Venus : " + str(round(Planets.venus_cur.total_bad, 2)))
        self.Mars_LabelNatal.text = str("Mars : " + str(round(Planets.mars_cur.total_bad, 2)))
        self.Jupiter_LabelNatal.text = str("Jupiter : " + str(round(Planets.jupiter_cur.total_bad, 2)))
        self.Saturn_LabelNatal.text = str("Saturn : " + str(round(Planets.saturn_cur.total_bad, 2)))
        self.Uranus_LabelNatal.text = str("Uranus : " + str(round(Planets.uranus_cur.total_bad, 2)))
        self.Neptune_LabelNatal.text = str("Neptune : " + str(round(Planets.neptune_cur.total_bad, 2)))
        self.Pluto_LabelNatal.text = str("Pluto : " + str(round(Planets.pluto_cur.total_bad, 2)))
        self.Marker_LabelNatal.text = str("Marker : " + str(round(Planets.marker_cur.total_bad, 2)))

    def _on_conjunct_natal_aspect(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Conjunct Aspect Selected')
        self.Sun_LabelNatal.text = str("Sun : " + str(round(Planets.sun_cur.total_conjunct, 2)))
        self.Moon_LabelNatal.text = str("Moon : " + str(round(Planets.moon_cur.total_conjunct, 2)))
        self.Mercury_LabelNatal.text = str("Mercury : " + str(round(Planets.mercury_cur.total_conjunct, 2)))
        self.Venus_LabelNatal.text = str("Venus : " + str(round(Planets.venus_cur.total_conjunct, 2)))
        self.Mars_LabelNatal.text = str("Mars : " + str(round(Planets.mars_cur.total_conjunct, 2)))
        self.Jupiter_LabelNatal.text = str("Jupiter : " + str(round(Planets.jupiter_cur.total_conjunct, 2)))
        self.Saturn_LabelNatal.text = str("Saturn : " + str(round(Planets.saturn_cur.total_conjunct, 2)))
        self.Uranus_LabelNatal.text = str("Uranus : " + str(round(Planets.uranus_cur.total_conjunct, 2)))
        self.Neptune_LabelNatal.text = str("Neptune : " + str(round(Planets.neptune_cur.total_conjunct, 2)))
        self.Pluto_LabelNatal.text = str("Pluto : " + str(round(Planets.pluto_cur.total_conjunct, 2)))
        self.Marker_LabelNatal.text = str("Marker : " + str(round(Planets.marker_cur.total_conjunct, 2)))

    def _on_sextile_natal_aspect(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Sextile Aspect Selected')
        self.Sun_LabelNatal.text = str("Sun : " + str(round(Planets.sun_cur.total_sextile, 2)))
        self.Moon_LabelNatal.text = str("Moon : " + str(round(Planets.moon_cur.total_sextile, 2)))
        self.Mercury_LabelNatal.text = str("Mercury : " + str(round(Planets.mercury_cur.total_sextile, 2)))
        self.Venus_LabelNatal.text = str("Venus : " + str(round(Planets.venus_cur.total_sextile, 2)))
        self.Mars_LabelNatal.text = str("Mars : " + str(round(Planets.mars_cur.total_sextile, 2)))
        self.Jupiter_LabelNatal.text = str("Jupiter : " + str(round(Planets.jupiter_cur.total_sextile, 2)))
        self.Saturn_LabelNatal.text = str("Saturn : " + str(round(Planets.saturn_cur.total_sextile, 2)))
        self.Uranus_LabelNatal.text = str("Uranus : " + str(round(Planets.uranus_cur.total_sextile, 2)))
        self.Neptune_LabelNatal.text = str("Neptune : " + str(round(Planets.neptune_cur.total_sextile, 2)))
        self.Pluto_LabelNatal.text = str("Pluto : " + str(round(Planets.pluto_cur.total_sextile, 2)))
        self.Marker_LabelNatal.text = str("Marker : " + str(round(Planets.marker_cur.total_sextile, 2)))

    def _on_square_natal_aspect(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Square Aspect Selected')
        self.Sun_LabelNatal.text = str("Sun : " + str(round(Planets.sun_cur.total_square, 2)))
        self.Moon_LabelNatal.text = str("Moon : " + str(round(Planets.moon_cur.total_square, 2)))
        self.Mercury_LabelNatal.text = str("Mercury : " + str(round(Planets.mercury_cur.total_square, 2)))
        self.Venus_LabelNatal.text = str("Venus : " + str(round(Planets.venus_cur.total_square, 2)))
        self.Mars_LabelNatal.text = str("Mars : " + str(round(Planets.mars_cur.total_square, 2)))
        self.Jupiter_LabelNatal.text = str("Jupiter : " + str(round(Planets.jupiter_cur.total_square, 2)))
        self.Saturn_LabelNatal.text = str("Saturn : " + str(round(Planets.saturn_cur.total_square, 2)))
        self.Uranus_LabelNatal.text = str("Uranus : " + str(round(Planets.uranus_cur.total_square, 2)))
        self.Neptune_LabelNatal.text = str("Neptune : " + str(round(Planets.neptune_cur.total_square, 2)))
        self.Pluto_LabelNatal.text = str("Pluto : " + str(round(Planets.pluto_cur.total_square, 2)))
        self.Marker_LabelNatal.text = str("Marker : " + str(round(Planets.marker_cur.total_square, 2)))

    def _on_trine_natal_aspect(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Trine Aspect Selected')
        self.Sun_LabelNatal.text = str("Sun : " + str(round(Planets.sun_cur.total_trine, 2)))
        self.Moon_LabelNatal.text = str("Moon : " + str(round(Planets.moon_cur.total_trine, 2)))
        self.Mercury_LabelNatal.text = str("Mercury : " + str(round(Planets.mercury_cur.total_trine, 2)))
        self.Venus_LabelNatal.text = str("Venus : " + str(round(Planets.venus_cur.total_trine, 2)))
        self.Mars_LabelNatal.text = str("Mars : " + str(round(Planets.mars_cur.total_trine, 2)))
        self.Jupiter_LabelNatal.text = str("Jupiter : " + str(round(Planets.jupiter_cur.total_trine, 2)))
        self.Saturn_LabelNatal.text = str("Saturn : " + str(round(Planets.saturn_cur.total_trine, 2)))
        self.Uranus_LabelNatal.text = str("Uranus : " + str(round(Planets.uranus_cur.total_trine, 2)))
        self.Neptune_LabelNatal.text = str("Neptune : " + str(round(Planets.neptune_cur.total_trine, 2)))
        self.Pluto_LabelNatal.text = str("Pluto : " + str(round(Planets.pluto_cur.total_trine, 2)))
        self.Marker_LabelNatal.text = str("Marker : " + str(round(Planets.marker_cur.total_trine, 2)))

    def _on_opposite_natal_aspect(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Opposite Aspect Selected')
        self.Sun_LabelNatal.text = str("Sun : " + str(round(Planets.sun_cur.total_opposite, 2)))
        self.Moon_LabelNatal.text = str("Moon : " + str(round(Planets.moon_cur.total_opposite, 2)))
        self.Mercury_LabelNatal.text = str("Mercury : " + str(round(Planets.mercury_cur.total_opposite, 2)))
        self.Venus_LabelNatal.text = str("Venus : " + str(round(Planets.venus_cur.total_opposite, 2)))
        self.Mars_LabelNatal.text = str("Mars : " + str(round(Planets.mars_cur.total_opposite, 2)))
        self.Jupiter_LabelNatal.text = str("Jupiter : " + str(round(Planets.jupiter_cur.total_opposite, 2)))
        self.Saturn_LabelNatal.text = str("Saturn : " + str(round(Planets.saturn_cur.total_opposite, 2)))
        self.Uranus_LabelNatal.text = str("Uranus : " + str(round(Planets.uranus_cur.total_opposite, 2)))
        self.Neptune_LabelNatal.text = str("Neptune : " + str(round(Planets.neptune_cur.total_opposite, 2)))
        self.Pluto_LabelNatal.text = str("Pluto : " + str(round(Planets.pluto_cur.total_opposite, 2)))
        self.Marker_LabelNatal.text = str("Marker : " + str(round(Planets.marker_cur.total_opposite, 2)))

    # def _build_source(self):
    #     """Build the widgets of the "Source" group"""
    #     with ui.CollapsableFrame("Source", name="group"):
    #         with ui.VStack(height=0, spacing=SPACING):
    #             with ui.HStack():
    #                 ui.Label("Prim", name="attribute_name", width=self.label_width)
    #                 ui.StringField(model=self._source_prim_model)
    #                 # Button that puts the selection to the string field
    #                 ui.Button(
    #                     " S ",
    #                     width=0,
    #                     height=0,
    #                     style={"margin": 0},
    #                     clicked_fn=self._on_get_selection,
    #                     tooltip="Get From Selection",
    #                 )

    def _on_cut_deck(self):
        """Called when the user presses the "Get From Selection" button"""
        self.Stack1Button.visible = True
        self.Stack2Button.visible = True
        self.Stack3Button.visible = True
        self.count = 1
        self._on_reset()

        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
            csvFile = csv.reader(file)
            self.rows = list(csvFile)
            #  print("Load File: ",self.rows[5][3])
            for i in range(0, 79):  # for i in range(1, 14):  # 1..13
                self.Deck_Position[i] = int(self.rows[i + 1][3])
                # print(self.rows[self.count][3])
                print("Load File Cut: ", self.Deck_Position[i + 1])
                # print(self.count)

        self.Deck_Cut_Left = np.zeros(80, dtype=int)
        self.Deck_Cut_Middle = np.zeros(80, dtype=int)
        self.Deck_Cut_Right = np.zeros(80, dtype=int)
        self.Deck_Temp = np.zeros(80, dtype=int)
        self.count = 0 # Header is zero
        self.count_Left = self.Slider_Value1 -1
        self.count_Middle = self.Slider_Value2 - self.Slider_Value1
        self.count_Right = 79 - self.Slider_Value2
        self.Load_Point = 1

        #print("Left Deck Cut:")
        # Cut the Deck into Left, Middle, Right
        for i in range(self.count_Left):  # for i in range(1, 14):  # 1..13  (// is floor division)
            self.Deck_Cut_Left[i] = self.Deck_Position[i]
            #print(self.Deck_Cut_Left[i])
            # print(self.count)

        self.count = 0  # Skip Header

        print("Middle Deck Cut:")
        for i in range(self.count_Middle):  # for i in range(1, 14):  # 1..13
            self.Deck_Cut_Middle[i] = self.Deck_Position[i + self.count_Left]
            #print(self.Deck_Cut_Middle[i])
            # print(self.count)

        self.count = 0  # Skip Header

        #print("Right Deck Cut:")
        for i in range(self.count_Right):  # for i in range(1, 14):  # 1..13
            self.Deck_Cut_Right[i] = self.Deck_Position[i + self.count_Left + self.count_Middle]
            #print(self.Deck_Cut_Right[i])
            # print(self.count)

        self.StackCombine = 3

    def _on_get_selection(self):
        """Called when the user presses the "Get From Selection" button"""
        self._source_prim_model.as_string = ", ".join(get_selection())
        pass

    def _build_scatter(self):
        """Build the widgets of the "Scatter" group"""
        with ui.CollapsableFrame("Scatter", name="group"):
            with ui.VStack(height=0, spacing=SPACING):
                with ui.HStack():
                     # TODO 2.5.1: Add _scatter_prim_model
                    ui.Label("Prim Path", name="attribute_name", width=self.label_width)
                    ui.StringField(model=self._scatter_prim_model)

                with ui.HStack():
                    # TODO 2.5.2: Add _scatter_type_model
                    ui.Label("Prim Type", name="attribute_name", width=self.label_width)
                    #ui.ComboBox(self._scatter_type_model)

                with ui.HStack():
                    # TODO 2.5.3: Add _scatter_seed_model
                    ui.Label("Seed", name="attribute_name", width=self.label_width)
                    ui.IntDrag(model=self._scatter_seed_model, min=0, max=10000)

                with ui.HStack():
                    # TODO 2.5.4: Add _scale_models
                    ui.Label("Scale", name="attribute_name", width=self.label_width)
                    for field in zip(["X:", "Y:", "Z:"], self._scale_models):
                        ui.Label(field[0], width=0, style={"margin": 3.0})
                        ui.FloatField(model=field[1], height=0, style={"margin": 3.0})

    def _build_axis(self, axis_id, axis_name):
        """Build the widgets of the "X" or "Y" or "Z" group"""
        with ui.CollapsableFrame(axis_name, name="group"):
            with ui.VStack(height=0, spacing=SPACING):
                with ui.HStack():
                    ui.Label("Object Count", name="attribute_name", width=self.label_width)
                    ui.IntDrag(model=self._scatter_count_models[axis_id], min=1, max=100)

                with ui.HStack():
                    ui.Label("Distance", name="attribute_name", width=self.label_width)
                    ui.FloatDrag(self._scatter_distance_models[axis_id], min=0, max=10000)

                with ui.HStack():
                    ui.Label("Random", name="attribute_name", width=self.label_width)
                    ui.FloatDrag(self._scatter_random_models[axis_id], min=0, max=10000)

    def on_slider_cut1(self, slider1):
        """Called when the user presses the "Get From Selection" button"""
        self.Slider_Value1 = self.slider1.model.get_value_as_int()
        self.slider2.min = self.Slider_Value1 + 1
        self.slider2.max = 78
        # print('Slider1 Cut Selected',self.Slider_Value1)

    def on_slider_cut2(self, slider2):
        """Called when the user presses the "Get From Selection" button"""
        self.Slider_Value2 = self.slider2.model.get_value_as_int()
        # print('Slider2 Cut Selected', self.Slider_Value2)

    def _on_stack1(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Stack 1 Layout Selected')
        print('StackCombine =: ',self.StackCombine)
        print('self.Slider_Value1',self.Slider_Value1)
        print('self.Slider_Value2',self.Slider_Value2)
        self.Stack1Button.visible = False

        self.count_Left = self.Slider_Value1 -1
        self.count_Middle = self.Slider_Value2 - self.Slider_Value1
        self.count_Right = 78 - self.Slider_Value2

        if(self.StackCombine == 3):
                for i in range(self.count_Left):  # for i in range(1, 14):  # 1..13
                        self.Deck_Temp[i + self.Load_Point] = self.Deck_Cut_Left[i]
                        if(self.Deck_Temp[i + self.Load_Point] == 0):
                             print("Stack 1 - 3 - : ", i )
                        #print('StackCombine == 3: ',self.StackCombine)
        if(self.StackCombine == 2):
                for i in range(self.count_Left):  # for i in range(1, 14):  # 1..13
                        self.Deck_Temp[i + self.Load_Point] = self.Deck_Cut_Left[i]
                        if(self.Deck_Temp[i + self.Load_Point] == 0):
                             print("Stack 1 - 2 - : ", i )
                        #print('StackCombine == 2: ',self.StackCombine)
        if(self.StackCombine == 1):
                for i in range(self.count_Left):  # for i in range(1, 14):  # 1..13
                        self.Deck_Temp[i  + self.Load_Point] = self.Deck_Cut_Left[i]
                        if(self.Deck_Temp[i + self.Load_Point] == 0):
                             print("Stack 1 - 2 - : ", i )
                        #print('StackCombine == 2: ',self.StackCombine)
        self.StackCombine -= 1
        self.Load_Point += self.count_Left

        if self.StackCombine < 1:
            print("Stack 1 Save Cards: ")
            # for i in range(1, 80):
                # print("Stack 3 Output: ", self.Deck_Temp[i])

            self._on_save_cards()

    def _on_stack2(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Stack 2 Layout Selected')
        print('StackCombine =: ',self.StackCombine)
        self.Stack2Button.visible = False

        self.count_Left = self.Slider_Value1 -1
        self.count_Middle = self.Slider_Value2 - self.Slider_Value1
        self.count_Right = 78 - self.Slider_Value2

        if(self.StackCombine == 3):
                for i in range(self.count_Middle):  # for i in range(1, 14):  # 1..13
                        self.Deck_Temp[i  + self.Load_Point] = self.Deck_Cut_Middle[i]
                        if(self.Deck_Temp[i + self.Load_Point] == 0):
                             print("Stack 2 - 3 - : ", i )
                        #print('StackCombine == 3: ',self.StackCombine)  Deck_Cut_Left  count_Left
        if(self.StackCombine == 2):
                for i in range(self.count_Middle):  # for i in range(1, 14):  # 1..13
                        self.Deck_Temp[i + self.Load_Point] = self.Deck_Cut_Middle[i]
                        if(self.Deck_Temp[i + self.Load_Point] == 0):
                             print("Stack 2 - 2 - : ", i )
                        #print('StackCombine == 2: ',self.StackCombine)  Deck_Cut_Middle  count_Middle
        if(self.StackCombine == 1):
                for i in range(self.count_Middle):  # for i in range(1, 14):  # 1..13
                        self.Deck_Temp[i + self.Load_Point] = self.Deck_Cut_Middle[i]
                        if(self.Deck_Temp[i + self.Load_Point] == 0):
                             print("Stack 2 - 1 - : ", i )
                       #print('StackCombine == 2: ',self.StackCombine) Deck_Cut_Right  count_Right
        self.StackCombine -= 1
        self.Load_Point += self.count_Middle

        if self.StackCombine < 1:
            print("Stack 2 Save Cards: ")
            # for i in range(1, 80):
            #     print("Stack 2 Output: ", self.Deck_Temp[i])

            self._on_save_cards()

    def _on_stack3(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Stack 3 Layout Selected')
        print('StackCombine =: ',self.StackCombine)
        self.Stack3Button.visible = False

        self.count_Left = self.Slider_Value1 -1
        self.count_Middle = self.Slider_Value2 - self.Slider_Value1
        self.count_Right = 79 - self.Slider_Value2

        if(self.StackCombine == 3):
                for i in range(self.count_Right):  # for i in range(1, 14):  # 1..13
                        self.Deck_Temp[i + self.Load_Point] = self.Deck_Cut_Right[i]
                        if(self.Deck_Temp[i + self.Load_Point] == 0):
                             print("Stack 3 - 3 - : ", i )
                         #print('StackCombine == 3: ',self.StackCombine)
        if(self.StackCombine == 2):
                for i in range(self.count_Right):  # for i in range(1, 14):  # 1..13
                        self.Deck_Temp[i + self.Load_Point] = self.Deck_Cut_Right[i]
                        if(self.Deck_Temp[i + self.Load_Point] == 0):
                             print("Stack 3 - 2 - : ", i)
                       #print('StackCombine == 2: ',self.StackCombine)
        if(self.StackCombine == 1):
                for i in range(self.count_Right):  # for i in range(1, 14):  # 1..13
                        self.Deck_Temp[i + self.Load_Point] = self.Deck_Cut_Right[i]
                        if(self.Deck_Temp[i + self.Load_Point] == 0):
                             print("Stack 3 - 1 - : ", i)
                         #print('StackCombine == 2: ',self.StackCombine)
        self.StackCombine -= 1
        self.Load_Point += self.count_Right

        if self.StackCombine < 1:
            print("Stack 3 Save Cards: ")
            # for i in range(1, 80):
            #     print("Stack 3 Output: ", self.Deck_Temp[i])

            self._on_save_cards()

    def _on_scatter(self):
        """Called when the user presses the "Scatter" button"""
        self._on_reset()
        self.count = 0

        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
            csvFile = csv.reader(file)
            self.rows = list(csvFile)
            # print(self.rows[5][3])
            for i in range(80):  # for i in range(1, 14):  # 1..13
                if(self.count == 0): self.Deck_Position[self.count] = 0
                else:  self.Deck_Position[self.count] = int(self.rows[self.count][3])
                # print(self.rows[self.count][3])
                # print(self.Deck_Position[self.count])
                # print(self.count)
                self.count += 1

        self.Deck_Cut_Left = np.zeros(80, dtype=int)
        self.Deck_Cut_Middle = np.zeros(80, dtype=int)
        self.Deck_Cut_Right = np.zeros(80, dtype=int)
        self.Deck_Temp = np.zeros(80, dtype=int)
        self.count = 1 # Header is zero

        #print("Left Deck Cut:")
        # Cut the Deck into Left, Middle, Right
        for i in range(1, self.Slider_Value):  # for i in range(1, 14):  # 1..13
            if(self.count == 0): self.Deck_Cut_Left[self.count] = 0
            else:  self.Deck_Cut_Left[self.count] = self.Deck_Position[self.count]
            # print(self.Deck_Cut_Left[self.count])
            # print(self.count)
            self.count += 1

        self.count = 1  # Skip Header

        #print("Right Deck Cut:")
        for i in range(self.Slider_Value, 79):  # for i in range(1, 14):  # 1..13
            self.Deck_Cut_Right[self.count] = self.Deck_Position[i]
            # print(self.Deck_Cut_Right[self.count])
            # print(self.count)
            self.count += 1

        self.count = random.randint(1, 4)  # Left Right Toggle
        self.count_Left = 1
        self.count_Right = 1
        self.count_Temp = 0

        #print("Temp Deck result:")
        for i in range(1, 80):  # for i in range(1, 14):  # 1..13
            if(self.count < 3):
                if(self.Deck_Cut_Left[self.count_Left] != 0):
                    self.Deck_Temp[i] = self.Deck_Cut_Left[self.count_Left]
                    self.count_Left += 1
                else:
                    if(self.Deck_Cut_Right[self.count_Right] != 0):
                        self.Deck_Temp[i] = self.Deck_Cut_Right[self.count_Right]
                        self.count_Right += 1
            if(self.count > 2):
                if(self.Deck_Cut_Right[self.count_Right] != 0):
                    self.Deck_Temp[i] = self.Deck_Cut_Right[self.count_Right]
                    self.count_Right += 1
                else:
                    if(self.Deck_Cut_Left[self.count_Left] != 0):
                        self.Deck_Temp[i] = self.Deck_Cut_Left[self.count_Left]
                        self.count_Left += 1

            self.count -= 1
            condition = (self.count == 0) or (self.count == 2) # Boolean equation form
            if condition:
                self.count = random.randint(1, 4)

        random_numbers = random.sample(range(1, 79), 78)
        #print(random_numbers) # random_numbers[1]][0] rows[self.Deck_Temp[1]][0]),

        self._on_save_cards()
        #print("Scatter Save Cards: ")


    def _on_save_cards(self):
        """Called when the user presses the "Get From Selection" button"""
        # print('ON Card Save')
        #for i in range(1, 80):
        #    print("Card Save Input: ", self.Deck_Temp[i])

        self._on_test_deck()

        self.count = 0

        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
            csvFile = csv.reader(file)
            self.rows = list(csvFile)
            # print(self.rows[5][0])
            # print("Read File again < 1: ",self.rows[5][0])
            #for lines in csvFile:
            #   print(lines)

        for i in range(1, 80):
            self.rows[i][3] = self.Deck_Temp[i]
                #print("Card Save Output: ", self.Deck_Temp[i])

        if Planets.Calander_layout == 1:
            Planets.Calander_1_card.append(self.Deck_Temp[1])
            #print('Loaded Calander 1 Cards: ')

        if Planets.Calander_layout == 3:
            Planets.Calander_3_card.append(self.Deck_Temp[1])
            Planets.Calander_3_card.append(self.Deck_Temp[2])
            Planets.Calander_3_card.append(self.Deck_Temp[3])
            #print('Loaded Calander 3 Cards: ')

        if Planets.Calander_layout == 13:
            Planets.Calander_13_card.append(self.Deck_Temp[1])
            Planets.Calander_13_card.append(self.Deck_Temp[2])
            Planets.Calander_13_card.append(self.Deck_Temp[3])
            Planets.Calander_13_card.append(self.Deck_Temp[4])
            Planets.Calander_13_card.append(self.Deck_Temp[5])
            Planets.Calander_13_card.append(self.Deck_Temp[6])
            Planets.Calander_13_card.append(self.Deck_Temp[7])
            Planets.Calander_13_card.append(self.Deck_Temp[8])
            Planets.Calander_13_card.append(self.Deck_Temp[9])
            Planets.Calander_13_card.append(self.Deck_Temp[10])
            Planets.Calander_13_card.append(self.Deck_Temp[11])
            Planets.Calander_13_card.append(self.Deck_Temp[12])
            Planets.Calander_13_card.append(self.Deck_Temp[13])
            #print('Loaded Calander 13 Cards: ')

        if Planets.Calander_layout == 22:
            Planets.Calander_22_card.append(self.Deck_Temp[1])
            Planets.Calander_22_card.append(self.Deck_Temp[2])
            Planets.Calander_22_card.append(self.Deck_Temp[3])
            Planets.Calander_22_card.append(self.Deck_Temp[4])
            Planets.Calander_22_card.append(self.Deck_Temp[5])
            Planets.Calander_22_card.append(self.Deck_Temp[6])
            Planets.Calander_22_card.append(self.Deck_Temp[7])
            Planets.Calander_22_card.append(self.Deck_Temp[8])
            Planets.Calander_22_card.append(self.Deck_Temp[9])
            Planets.Calander_22_card.append(self.Deck_Temp[10])
            Planets.Calander_22_card.append(self.Deck_Temp[11])
            Planets.Calander_22_card.append(self.Deck_Temp[12])
            Planets.Calander_22_card.append(self.Deck_Temp[13])
            Planets.Calander_22_card.append(self.Deck_Temp[14])
            Planets.Calander_22_card.append(self.Deck_Temp[15])
            Planets.Calander_22_card.append(self.Deck_Temp[16])
            Planets.Calander_22_card.append(self.Deck_Temp[17])
            Planets.Calander_22_card.append(self.Deck_Temp[18])
            Planets.Calander_22_card.append(self.Deck_Temp[19])
            Planets.Calander_22_card.append(self.Deck_Temp[20])
            Planets.Calander_22_card.append(self.Deck_Temp[21])
            Planets.Calander_22_card.append(self.Deck_Temp[22])
            #print('Loaded Calander 22 Cards: ')


        # Data to be written
        data = [
            [self.rows[0][0], self.rows[0][1], self.rows[0][2], self.rows[0][3], self.rows[0][4], self.rows[0][5], self.rows[0][6], self.rows[0][7], self.rows[0][8], self.rows[0][9], self.rows[0][10], self.rows[0][11], self.rows[0][12], self.rows[0][13], self.rows[0][14], self.rows[0][15], self.rows[0][16]],
            [self.rows[1][0], self.rows[1][1], self.rows[1][2], self.rows[1][3], self.rows[1][4], self.rows[1][5], self.rows[1][6], self.rows[1][7], self.rows[1][8], self.rows[1][9], self.rows[1][10], self.rows[1][11], self.rows[1][12], self.rows[1][13], self.rows[1][14], self.rows[1][15], self.rows[1][16]],
            [self.rows[2][0], self.rows[2][1], self.rows[2][2], self.rows[2][3], self.rows[2][4], self.rows[2][5], self.rows[2][6], self.rows[2][7], self.rows[2][8], self.rows[2][9], self.rows[2][10], self.rows[2][11], self.rows[2][12], self.rows[2][13], self.rows[2][14], self.rows[2][15], self.rows[2][16]],
            [self.rows[3][0], self.rows[3][1], self.rows[3][2], self.rows[3][3], self.rows[3][4], self.rows[3][5], self.rows[3][6], self.rows[3][7], self.rows[3][8], self.rows[3][9], self.rows[3][10], self.rows[3][11], self.rows[3][12], self.rows[3][13], self.rows[3][14], self.rows[3][15], self.rows[3][16]],
            [self.rows[4][0], self.rows[4][1], self.rows[4][2], self.rows[4][3], self.rows[4][4], self.rows[4][5], self.rows[4][6], self.rows[4][7], self.rows[4][8], self.rows[4][9], self.rows[4][10], self.rows[4][11], self.rows[4][12], self.rows[4][13], self.rows[4][14], self.rows[4][15], self.rows[4][16]],
            [self.rows[5][0], self.rows[5][1], self.rows[5][2], self.rows[5][3], self.rows[5][4], self.rows[5][5], self.rows[5][6], self.rows[5][7], self.rows[5][8], self.rows[5][9], self.rows[5][10], self.rows[5][11], self.rows[5][12], self.rows[5][13], self.rows[5][14], self.rows[5][15], self.rows[5][16]],
            [self.rows[6][0], self.rows[6][1], self.rows[6][2], self.rows[6][3], self.rows[6][4], self.rows[6][5], self.rows[6][6], self.rows[6][7], self.rows[6][8], self.rows[6][9], self.rows[6][10], self.rows[6][11], self.rows[6][12], self.rows[6][13], self.rows[6][14], self.rows[6][15], self.rows[6][16]],
            [self.rows[7][0], self.rows[7][1], self.rows[7][2], self.rows[7][3], self.rows[7][4], self.rows[7][5], self.rows[7][6], self.rows[7][7], self.rows[7][8], self.rows[7][9], self.rows[7][10], self.rows[7][11], self.rows[7][12], self.rows[7][13], self.rows[7][14], self.rows[7][15], self.rows[7][16]],
            [self.rows[8][0], self.rows[8][1], self.rows[8][2], self.rows[8][3], self.rows[8][4], self.rows[8][5], self.rows[8][6], self.rows[8][7], self.rows[8][8], self.rows[8][9], self.rows[8][10], self.rows[8][11], self.rows[8][12], self.rows[8][13], self.rows[8][14], self.rows[8][15], self.rows[8][16]],
            [self.rows[9][0], self.rows[9][1], self.rows[9][2], self.rows[9][3], self.rows[9][4], self.rows[9][5], self.rows[9][6], self.rows[9][7], self.rows[9][8], self.rows[9][9], self.rows[9][10], self.rows[9][11], self.rows[9][12], self.rows[9][13], self.rows[9][14], self.rows[9][15], self.rows[9][16]],

            [self.rows[10][0], self.rows[10][1], self.rows[10][2], self.rows[10][3], self.rows[10][4], self.rows[10][5], self.rows[10][6], self.rows[10][7], self.rows[10][8], self.rows[10][9], self.rows[10][10], self.rows[10][11], self.rows[10][12], self.rows[10][13], self.rows[10][14], self.rows[10][15], self.rows[10][16]],
            [self.rows[11][0], self.rows[11][1], self.rows[11][2], self.rows[11][3], self.rows[11][4], self.rows[11][5], self.rows[11][6], self.rows[11][7], self.rows[11][8], self.rows[11][9], self.rows[11][10], self.rows[11][11], self.rows[11][12], self.rows[11][13], self.rows[11][14], self.rows[11][15], self.rows[11][16]],
            [self.rows[12][0], self.rows[12][1], self.rows[12][2], self.rows[12][3], self.rows[12][4], self.rows[12][5], self.rows[12][6], self.rows[12][7], self.rows[12][8], self.rows[12][9], self.rows[12][10], self.rows[12][11], self.rows[12][12], self.rows[12][13], self.rows[12][14], self.rows[12][15], self.rows[12][16]],
            [self.rows[13][0], self.rows[13][1], self.rows[13][2], self.rows[13][3], self.rows[13][4], self.rows[13][5], self.rows[13][6], self.rows[13][7], self.rows[13][8], self.rows[13][9], self.rows[13][10], self.rows[13][11], self.rows[13][12], self.rows[13][13], self.rows[13][14], self.rows[13][15], self.rows[13][16]],
            [self.rows[14][0], self.rows[14][1], self.rows[14][2], self.rows[14][3], self.rows[14][4], self.rows[14][5], self.rows[14][6], self.rows[14][7], self.rows[14][8], self.rows[14][9], self.rows[14][10], self.rows[14][11], self.rows[14][12], self.rows[14][13], self.rows[14][14], self.rows[14][15], self.rows[14][16]],
            [self.rows[15][0], self.rows[15][1], self.rows[15][2], self.rows[15][3], self.rows[15][4], self.rows[15][5], self.rows[15][6], self.rows[15][7], self.rows[15][8], self.rows[15][9], self.rows[15][10], self.rows[15][11], self.rows[15][12], self.rows[15][13], self.rows[15][14], self.rows[15][15], self.rows[15][16]],
            [self.rows[16][0], self.rows[16][1], self.rows[16][2], self.rows[16][3], self.rows[16][4], self.rows[16][5], self.rows[16][6], self.rows[16][7], self.rows[16][8], self.rows[16][9], self.rows[16][10], self.rows[16][11], self.rows[16][12], self.rows[16][13], self.rows[16][14], self.rows[16][15], self.rows[16][16]],
            [self.rows[17][0], self.rows[17][1], self.rows[17][2], self.rows[17][3], self.rows[17][4], self.rows[17][5], self.rows[17][6], self.rows[17][7], self.rows[17][8], self.rows[17][9], self.rows[17][10], self.rows[17][11], self.rows[17][12], self.rows[17][13], self.rows[17][14], self.rows[17][15], self.rows[17][16]],
            [self.rows[18][0], self.rows[18][1], self.rows[18][2], self.rows[18][3], self.rows[18][4], self.rows[18][5], self.rows[18][6], self.rows[18][7], self.rows[18][8], self.rows[18][9], self.rows[18][10], self.rows[18][11], self.rows[18][12], self.rows[18][13], self.rows[18][14], self.rows[18][15], self.rows[18][16]],
            [self.rows[19][0], self.rows[19][1], self.rows[19][2], self.rows[19][3], self.rows[19][4], self.rows[19][5], self.rows[19][6], self.rows[19][7], self.rows[19][8], self.rows[19][9], self.rows[19][10], self.rows[19][11], self.rows[19][12], self.rows[19][13], self.rows[19][14], self.rows[19][15], self.rows[19][16]],

            [self.rows[20][0], self.rows[20][1], self.rows[20][2], self.rows[20][3], self.rows[20][4], self.rows[20][5], self.rows[20][6], self.rows[20][7], self.rows[20][8], self.rows[20][9], self.rows[20][10], self.rows[20][11], self.rows[20][12], self.rows[20][13], self.rows[20][14], self.rows[20][15], self.rows[20][16]],
            [self.rows[21][0], self.rows[21][1], self.rows[21][2], self.rows[21][3], self.rows[21][4], self.rows[21][5], self.rows[21][6], self.rows[21][7], self.rows[21][8], self.rows[21][9], self.rows[21][10], self.rows[21][11], self.rows[21][12], self.rows[21][13], self.rows[21][14], self.rows[21][15], self.rows[21][16]],
            [self.rows[22][0], self.rows[22][1], self.rows[22][2], self.rows[22][3], self.rows[22][4], self.rows[22][5], self.rows[22][6], self.rows[22][7], self.rows[22][8], self.rows[22][9], self.rows[22][10], self.rows[22][11], self.rows[22][12], self.rows[22][13], self.rows[22][14], self.rows[22][15], self.rows[22][16]],
            [self.rows[23][0], self.rows[23][1], self.rows[23][2], self.rows[23][3], self.rows[23][4], self.rows[23][5], self.rows[23][6], self.rows[23][7], self.rows[23][8], self.rows[23][9], self.rows[23][10], self.rows[23][11], self.rows[23][12], self.rows[23][13], self.rows[23][14], self.rows[23][15], self.rows[23][16]],
            [self.rows[24][0], self.rows[24][1], self.rows[24][2], self.rows[24][3], self.rows[24][4], self.rows[24][5], self.rows[24][6], self.rows[24][7], self.rows[24][8], self.rows[24][9], self.rows[24][10], self.rows[24][11], self.rows[24][12], self.rows[24][13], self.rows[24][14], self.rows[24][15], self.rows[24][16]],
            [self.rows[25][0], self.rows[25][1], self.rows[25][2], self.rows[25][3], self.rows[25][4], self.rows[25][5], self.rows[25][6], self.rows[25][7], self.rows[25][8], self.rows[25][9], self.rows[25][10], self.rows[25][11], self.rows[25][12], self.rows[25][13], self.rows[25][14], self.rows[25][15], self.rows[25][16]],
            [self.rows[26][0], self.rows[26][1], self.rows[26][2], self.rows[26][3], self.rows[26][4], self.rows[26][5], self.rows[26][6], self.rows[26][7], self.rows[26][8], self.rows[26][9], self.rows[26][10], self.rows[26][11], self.rows[26][12], self.rows[26][13], self.rows[26][14], self.rows[26][15], self.rows[26][16]],
            [self.rows[27][0], self.rows[27][1], self.rows[27][2], self.rows[27][3], self.rows[27][4], self.rows[27][5], self.rows[27][6], self.rows[27][7], self.rows[27][8], self.rows[27][9], self.rows[27][10], self.rows[27][11], self.rows[27][12], self.rows[27][13], self.rows[27][14], self.rows[27][15], self.rows[27][16]],
            [self.rows[28][0], self.rows[28][1], self.rows[28][2], self.rows[28][3], self.rows[28][4], self.rows[28][5], self.rows[28][6], self.rows[28][7], self.rows[28][8], self.rows[28][9], self.rows[28][10], self.rows[28][11], self.rows[28][12], self.rows[28][13], self.rows[28][14], self.rows[28][15], self.rows[28][16]],
            [self.rows[29][0], self.rows[29][1], self.rows[29][2], self.rows[29][3], self.rows[29][4], self.rows[29][5], self.rows[29][6], self.rows[29][7], self.rows[29][8], self.rows[29][9], self.rows[29][10], self.rows[29][11], self.rows[29][12], self.rows[29][13], self.rows[29][14], self.rows[29][15], self.rows[29][16]],

            [self.rows[30][0], self.rows[30][1], self.rows[30][2], self.rows[30][3], self.rows[30][4], self.rows[30][5], self.rows[30][6], self.rows[30][7], self.rows[30][8], self.rows[30][9], self.rows[30][10], self.rows[30][11], self.rows[30][12], self.rows[30][13], self.rows[30][14], self.rows[30][15], self.rows[30][16]],
            [self.rows[31][0], self.rows[31][1], self.rows[31][2], self.rows[31][3], self.rows[31][4], self.rows[31][5], self.rows[31][6], self.rows[31][7], self.rows[31][8], self.rows[31][9], self.rows[31][10], self.rows[31][11], self.rows[31][12], self.rows[31][13], self.rows[31][14], self.rows[31][15], self.rows[31][16]],
            [self.rows[32][0], self.rows[32][1], self.rows[32][2], self.rows[32][3], self.rows[32][4], self.rows[32][5], self.rows[32][6], self.rows[32][7], self.rows[32][8], self.rows[32][9], self.rows[32][10], self.rows[32][11], self.rows[32][12], self.rows[32][13], self.rows[32][14], self.rows[32][15], self.rows[32][16]],
            [self.rows[33][0], self.rows[33][1], self.rows[33][2], self.rows[33][3], self.rows[33][4], self.rows[33][5], self.rows[33][6], self.rows[33][7], self.rows[33][8], self.rows[33][9], self.rows[33][10], self.rows[33][11], self.rows[33][12], self.rows[33][13], self.rows[33][14], self.rows[33][15], self.rows[33][16]],
            [self.rows[34][0], self.rows[34][1], self.rows[34][2], self.rows[34][3], self.rows[34][4], self.rows[34][5], self.rows[34][6], self.rows[34][7], self.rows[34][8], self.rows[34][9], self.rows[34][10], self.rows[34][11], self.rows[34][12], self.rows[34][13], self.rows[34][14], self.rows[34][15], self.rows[34][16]],
            [self.rows[35][0], self.rows[35][1], self.rows[35][2], self.rows[35][3], self.rows[35][4], self.rows[35][5], self.rows[35][6], self.rows[35][7], self.rows[35][8], self.rows[35][9], self.rows[35][10], self.rows[35][11], self.rows[35][12], self.rows[35][13], self.rows[35][14], self.rows[35][15], self.rows[35][16]],
            [self.rows[36][0], self.rows[36][1], self.rows[36][2], self.rows[36][3], self.rows[36][4], self.rows[36][5], self.rows[36][6], self.rows[36][7], self.rows[36][8], self.rows[36][9], self.rows[36][10], self.rows[36][11], self.rows[36][12], self.rows[36][13], self.rows[36][14], self.rows[36][15], self.rows[36][16]],
            [self.rows[37][0], self.rows[37][1], self.rows[37][2], self.rows[37][3], self.rows[37][4], self.rows[37][5], self.rows[37][6], self.rows[37][7], self.rows[37][8], self.rows[37][9], self.rows[37][10], self.rows[37][11], self.rows[37][12], self.rows[37][13], self.rows[37][14], self.rows[37][15], self.rows[37][16]],
            [self.rows[38][0], self.rows[38][1], self.rows[38][2], self.rows[38][3], self.rows[38][4], self.rows[38][5], self.rows[38][6], self.rows[38][7], self.rows[38][8], self.rows[38][9], self.rows[38][10], self.rows[38][11], self.rows[38][12], self.rows[38][13], self.rows[38][14], self.rows[38][15], self.rows[38][16]],
            [self.rows[39][0], self.rows[39][1], self.rows[39][2], self.rows[39][3], self.rows[39][4], self.rows[39][5], self.rows[39][6], self.rows[39][7], self.rows[39][8], self.rows[39][9], self.rows[39][10], self.rows[39][11], self.rows[39][12], self.rows[39][13], self.rows[39][14], self.rows[39][15], self.rows[39][16]],

            [self.rows[40][0], self.rows[40][1], self.rows[40][2], self.rows[40][3], self.rows[40][4], self.rows[40][5], self.rows[40][6], self.rows[40][7], self.rows[40][8], self.rows[40][9], self.rows[40][10], self.rows[40][11], self.rows[40][12], self.rows[40][13], self.rows[40][14], self.rows[40][15], self.rows[40][16]],
            [self.rows[41][0], self.rows[41][1], self.rows[41][2], self.rows[41][3], self.rows[41][4], self.rows[41][5], self.rows[41][6], self.rows[41][7], self.rows[41][8], self.rows[41][9], self.rows[41][10], self.rows[41][11], self.rows[41][12], self.rows[41][13], self.rows[41][14], self.rows[41][15], self.rows[41][16]],
            [self.rows[42][0], self.rows[42][1], self.rows[42][2], self.rows[42][3], self.rows[42][4], self.rows[42][5], self.rows[42][6], self.rows[42][7], self.rows[42][8], self.rows[42][9], self.rows[42][10], self.rows[42][11], self.rows[42][12], self.rows[42][13], self.rows[42][14], self.rows[42][15], self.rows[42][16]],
            [self.rows[43][0], self.rows[43][1], self.rows[43][2], self.rows[43][3], self.rows[43][4], self.rows[43][5], self.rows[43][6], self.rows[43][7], self.rows[43][8], self.rows[43][9], self.rows[43][10], self.rows[43][11], self.rows[43][12], self.rows[43][13], self.rows[43][14], self.rows[43][15], self.rows[43][16]],
            [self.rows[44][0], self.rows[44][1], self.rows[44][2], self.rows[44][3], self.rows[44][4], self.rows[44][5], self.rows[44][6], self.rows[44][7], self.rows[44][8], self.rows[44][9], self.rows[44][10], self.rows[44][11], self.rows[44][12], self.rows[44][13], self.rows[44][14], self.rows[44][15], self.rows[44][16]],
            [self.rows[45][0], self.rows[45][1], self.rows[45][2], self.rows[45][3], self.rows[45][4], self.rows[45][5], self.rows[45][6], self.rows[45][7], self.rows[45][8], self.rows[45][9], self.rows[45][10], self.rows[45][11], self.rows[45][12], self.rows[45][13], self.rows[45][14], self.rows[45][15], self.rows[45][16]],
            [self.rows[46][0], self.rows[46][1], self.rows[46][2], self.rows[46][3], self.rows[46][4], self.rows[46][5], self.rows[46][6], self.rows[46][7], self.rows[46][8], self.rows[46][9], self.rows[46][10], self.rows[46][11], self.rows[46][12], self.rows[46][13], self.rows[46][14], self.rows[46][15], self.rows[46][16]],
            [self.rows[47][0], self.rows[47][1], self.rows[47][2], self.rows[47][3], self.rows[47][4], self.rows[47][5], self.rows[47][6], self.rows[47][7], self.rows[47][8], self.rows[47][9], self.rows[47][10], self.rows[47][11], self.rows[47][12], self.rows[47][13], self.rows[47][14], self.rows[47][15], self.rows[47][16]],
            [self.rows[48][0], self.rows[48][1], self.rows[48][2], self.rows[48][3], self.rows[48][4], self.rows[48][5], self.rows[48][6], self.rows[48][7], self.rows[48][8], self.rows[48][9], self.rows[48][10], self.rows[48][11], self.rows[48][12], self.rows[48][13], self.rows[48][14], self.rows[48][15], self.rows[48][16]],
            [self.rows[49][0], self.rows[49][1], self.rows[49][2], self.rows[49][3], self.rows[49][4], self.rows[49][5], self.rows[49][6], self.rows[49][7], self.rows[49][8], self.rows[49][9], self.rows[49][10], self.rows[49][11], self.rows[49][12], self.rows[49][13], self.rows[49][14], self.rows[49][15], self.rows[49][16]],

            [self.rows[50][0], self.rows[50][1], self.rows[50][2], self.rows[50][3], self.rows[50][4], self.rows[50][5], self.rows[50][6], self.rows[50][7], self.rows[50][8], self.rows[50][9], self.rows[50][10], self.rows[50][11], self.rows[50][12], self.rows[50][13], self.rows[50][14], self.rows[50][15], self.rows[50][16]],
            [self.rows[51][0], self.rows[51][1], self.rows[51][2], self.rows[51][3], self.rows[51][4], self.rows[51][5], self.rows[51][6], self.rows[51][7], self.rows[51][8], self.rows[51][9], self.rows[51][10], self.rows[51][11], self.rows[51][12], self.rows[51][13], self.rows[51][14], self.rows[51][15], self.rows[51][16]],
            [self.rows[52][0], self.rows[52][1], self.rows[52][2], self.rows[52][3], self.rows[52][4], self.rows[52][5], self.rows[52][6], self.rows[52][7], self.rows[52][8], self.rows[52][9], self.rows[52][10], self.rows[52][11], self.rows[52][12], self.rows[52][13], self.rows[52][14], self.rows[52][15], self.rows[52][16]],
            [self.rows[53][0], self.rows[53][1], self.rows[53][2], self.rows[53][3], self.rows[53][4], self.rows[53][5], self.rows[53][6], self.rows[53][7], self.rows[53][8], self.rows[53][9], self.rows[53][10], self.rows[53][11], self.rows[53][12], self.rows[53][13], self.rows[53][14], self.rows[53][15], self.rows[53][16]],
            [self.rows[54][0], self.rows[54][1], self.rows[54][2], self.rows[54][3], self.rows[54][4], self.rows[54][5], self.rows[54][6], self.rows[54][7], self.rows[54][8], self.rows[54][9], self.rows[54][10], self.rows[54][11], self.rows[54][12], self.rows[54][13], self.rows[54][14], self.rows[54][15], self.rows[54][16]],
            [self.rows[55][0], self.rows[55][1], self.rows[55][2], self.rows[55][3], self.rows[55][4], self.rows[55][5], self.rows[55][6], self.rows[55][7], self.rows[55][8], self.rows[55][9], self.rows[55][10], self.rows[55][11], self.rows[55][12], self.rows[55][13], self.rows[55][14], self.rows[55][15], self.rows[55][16]],
            [self.rows[56][0], self.rows[56][1], self.rows[56][2], self.rows[56][3], self.rows[56][4], self.rows[56][5], self.rows[56][6], self.rows[56][7], self.rows[56][8], self.rows[56][9], self.rows[56][10], self.rows[56][11], self.rows[56][12], self.rows[56][13], self.rows[56][14], self.rows[56][15], self.rows[56][16]],
            [self.rows[57][0], self.rows[57][1], self.rows[57][2], self.rows[57][3], self.rows[57][4], self.rows[57][5], self.rows[57][6], self.rows[57][7], self.rows[57][8], self.rows[57][9], self.rows[57][10], self.rows[57][11], self.rows[57][12], self.rows[57][13], self.rows[57][14], self.rows[57][15], self.rows[57][16]],
            [self.rows[58][0], self.rows[58][1], self.rows[58][2], self.rows[58][3], self.rows[58][4], self.rows[58][5], self.rows[58][6], self.rows[58][7], self.rows[58][8], self.rows[58][9], self.rows[58][10], self.rows[58][11], self.rows[58][12], self.rows[58][13], self.rows[58][14], self.rows[58][15], self.rows[58][16]],
            [self.rows[59][0], self.rows[59][1], self.rows[59][2], self.rows[59][3], self.rows[59][4], self.rows[59][5], self.rows[59][6], self.rows[59][7], self.rows[59][8], self.rows[59][9], self.rows[59][10], self.rows[59][11], self.rows[59][12], self.rows[59][13], self.rows[59][14], self.rows[59][15], self.rows[59][16]],

            [self.rows[60][0], self.rows[60][1], self.rows[60][2], self.rows[60][3], self.rows[60][4], self.rows[60][5], self.rows[60][6], self.rows[60][7], self.rows[60][8], self.rows[60][9], self.rows[60][10], self.rows[60][11], self.rows[60][12], self.rows[60][13], self.rows[60][14], self.rows[60][15], self.rows[60][16]],
            [self.rows[61][0], self.rows[61][1], self.rows[61][2], self.rows[61][3], self.rows[61][4], self.rows[61][5], self.rows[61][6], self.rows[61][7], self.rows[61][8], self.rows[61][9], self.rows[61][10], self.rows[61][11], self.rows[61][12], self.rows[61][13], self.rows[61][14], self.rows[61][15], self.rows[61][16]],
            [self.rows[62][0], self.rows[62][1], self.rows[62][2], self.rows[62][3], self.rows[62][4], self.rows[62][5], self.rows[62][6], self.rows[62][7], self.rows[62][8], self.rows[62][9], self.rows[62][10], self.rows[62][11], self.rows[62][12], self.rows[62][13], self.rows[62][14], self.rows[62][15], self.rows[62][16]],
            [self.rows[63][0], self.rows[63][1], self.rows[63][2], self.rows[63][3], self.rows[63][4], self.rows[63][5], self.rows[63][6], self.rows[63][7], self.rows[63][8], self.rows[63][9], self.rows[63][10], self.rows[63][11], self.rows[63][12], self.rows[63][13], self.rows[63][14], self.rows[63][15], self.rows[63][16]],
            [self.rows[64][0], self.rows[64][1], self.rows[64][2], self.rows[64][3], self.rows[64][4], self.rows[64][5], self.rows[64][6], self.rows[64][7], self.rows[64][8], self.rows[64][9], self.rows[64][10], self.rows[64][11], self.rows[64][12], self.rows[64][13], self.rows[64][14], self.rows[64][15], self.rows[64][16]],
            [self.rows[65][0], self.rows[65][1], self.rows[65][2], self.rows[65][3], self.rows[65][4], self.rows[65][5], self.rows[65][6], self.rows[65][7], self.rows[65][8], self.rows[65][9], self.rows[65][10], self.rows[65][11], self.rows[65][12], self.rows[65][13], self.rows[65][14], self.rows[65][15], self.rows[65][16]],
            [self.rows[66][0], self.rows[66][1], self.rows[66][2], self.rows[66][3], self.rows[66][4], self.rows[66][5], self.rows[66][6], self.rows[66][7], self.rows[66][8], self.rows[66][9], self.rows[66][10], self.rows[66][11], self.rows[66][12], self.rows[66][13], self.rows[66][14], self.rows[66][15], self.rows[66][16]],
            [self.rows[67][0], self.rows[67][1], self.rows[67][2], self.rows[67][3], self.rows[67][4], self.rows[67][5], self.rows[67][6], self.rows[67][7], self.rows[67][8], self.rows[67][9], self.rows[67][10], self.rows[67][11], self.rows[67][12], self.rows[67][13], self.rows[67][14], self.rows[67][15], self.rows[67][16]],
            [self.rows[68][0], self.rows[68][1], self.rows[68][2], self.rows[68][3], self.rows[68][4], self.rows[68][5], self.rows[68][6], self.rows[68][7], self.rows[68][8], self.rows[68][9], self.rows[68][10], self.rows[68][11], self.rows[68][12], self.rows[68][13], self.rows[68][14], self.rows[68][15], self.rows[68][16]],
            [self.rows[69][0], self.rows[69][1], self.rows[69][2], self.rows[69][3], self.rows[69][4], self.rows[69][5], self.rows[69][6], self.rows[69][7], self.rows[69][8], self.rows[69][9], self.rows[69][10], self.rows[69][11], self.rows[69][12], self.rows[69][13], self.rows[69][14], self.rows[69][15], self.rows[69][16]],

            [self.rows[70][0], self.rows[70][1], self.rows[70][2], self.rows[70][3], self.rows[70][4], self.rows[70][5], self.rows[70][6], self.rows[70][7], self.rows[70][8], self.rows[70][9], self.rows[70][10], self.rows[70][11], self.rows[70][12], self.rows[70][13], self.rows[70][14], self.rows[70][15], self.rows[70][16]],
            [self.rows[71][0], self.rows[71][1], self.rows[71][2], self.rows[71][3], self.rows[71][4], self.rows[71][5], self.rows[71][6], self.rows[71][7], self.rows[71][8], self.rows[71][9], self.rows[71][10], self.rows[71][11], self.rows[71][12], self.rows[71][13], self.rows[71][14], self.rows[71][15], self.rows[71][16]],
            [self.rows[72][0], self.rows[72][1], self.rows[72][2], self.rows[72][3], self.rows[72][4], self.rows[72][5], self.rows[72][6], self.rows[72][7], self.rows[72][8], self.rows[72][9], self.rows[72][10], self.rows[72][11], self.rows[72][12], self.rows[72][13], self.rows[72][14], self.rows[72][15], self.rows[72][16]],
            [self.rows[73][0], self.rows[73][1], self.rows[73][2], self.rows[73][3], self.rows[73][4], self.rows[73][5], self.rows[73][6], self.rows[73][7], self.rows[73][8], self.rows[73][9], self.rows[73][10], self.rows[73][11], self.rows[73][12], self.rows[73][13], self.rows[73][14], self.rows[73][15], self.rows[73][16]],
            [self.rows[74][0], self.rows[74][1], self.rows[74][2], self.rows[74][3], self.rows[74][4], self.rows[74][5], self.rows[74][6], self.rows[74][7], self.rows[74][8], self.rows[74][9], self.rows[74][10], self.rows[74][11], self.rows[74][12], self.rows[74][13], self.rows[74][14], self.rows[74][15], self.rows[74][16]],
            [self.rows[75][0], self.rows[75][1], self.rows[75][2], self.rows[75][3], self.rows[75][4], self.rows[75][5], self.rows[75][6], self.rows[75][7], self.rows[75][8], self.rows[75][9], self.rows[75][10], self.rows[75][11], self.rows[75][12], self.rows[75][13], self.rows[75][14], self.rows[75][15], self.rows[75][16]],
            [self.rows[76][0], self.rows[76][1], self.rows[76][2], self.rows[76][3], self.rows[76][4], self.rows[76][5], self.rows[76][6], self.rows[76][7], self.rows[76][8], self.rows[76][9], self.rows[76][10], self.rows[76][11], self.rows[76][12], self.rows[76][13], self.rows[76][14], self.rows[76][15], self.rows[76][16]],
            [self.rows[77][0], self.rows[77][1], self.rows[77][2], self.rows[77][3], self.rows[77][4], self.rows[77][5], self.rows[77][6], self.rows[77][7], self.rows[77][8], self.rows[77][9], self.rows[77][10], self.rows[77][11], self.rows[77][12], self.rows[77][13], self.rows[77][14], self.rows[77][15], self.rows[77][16]],
            [self.rows[78][0], self.rows[78][1], self.rows[78][2], self.rows[78][3], self.rows[78][4], self.rows[78][5], self.rows[78][6], self.rows[78][7], self.rows[78][8], self.rows[78][9], self.rows[78][10], self.rows[78][11], self.rows[78][12], self.rows[78][13], self.rows[78][14], self.rows[78][15], self.rows[78][16]],
            [self.rows[79][0], self.rows[79][1], self.rows[79][2], self.rows[79][3], self.rows[79][4], self.rows[79][5], self.rows[79][6], self.rows[79][7], self.rows[79][8], self.rows[79][9], self.rows[79][10], self.rows[79][11], self.rows[79][12], self.rows[79][13], self.rows[79][14], self.rows[79][15], self.rows[79][16]]
            ]

        # header = ['name', 'area', 'country_code2', 'country_code3']
        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            #writer.writerow(header)
            writer.writerows(data)
            #for i in range(0, 80):
            #    writer.writerow(rows[i])

        #self._on_three_card()

    def _on_chakra_current(self):
        """Called when the user presses the "Get From Selection" button"""
        #print('Chakra Layout Selected')
        self._on_chakra(1)

    def _on_chakra_calander(self):
        """Called when the user presses the "Get From Selection" button"""
        #print('Chakra Layout Selected')
        self._on_chakra(2)

    def _on_collider_current(self):
        """Called when the user presses the "Get From Selection" button"""
        #print('Collider Layout Selected')
        self._on_collider(1)

    def _on_collider_calander(self):
        """Called when the user presses the "Get From Selection" button"""
        #print('Collider Layout Selected')
        self._on_collider(2)

    def _on_three_card_current(self):
        """Called when the user presses the "Get From Selection" button"""
        # print('Three Card Layout Selected')
        self._on_three_card(1)

    def _on_one_card_calander(self):
        """Called when the user presses the "Get From Selection" button"""
        # print('One Card Layout Selected')
        self._on_one_card(2)

    def _on_three_card_calander(self):
        """Called when the user presses the "Get From Selection" button"""
        # print('Three Card Layout Selected')
        self._on_three_card(2)

    def _on_three_card(self, layout_mode):
        """Called when the user presses the "Get From Selection" button"""
        # print('Three Card Layout Selected')

        # Camera Functions
        # import omni.usd
        # from pxr import UsdGeom, Gf
        # # Get the current USD stage
        stage = omni.usd.get_context().get_stage()

        # Define the camera path in the USD scene
        camera_path = "/World/Camera"

        # # Create a camera if it doesn't exist
        if not stage.GetPrimAtPath(camera_path):
            camera = UsdGeom.Camera.Define(stage, camera_path)
        else:
            camera = UsdGeom.Camera(stage.GetPrimAtPath(camera_path))

        # # Set camera position (x, y, z)
        new_position = Gf.Vec3d(100, 50, 200)  # Example position in centimeters
        xform = UsdGeom.Xformable(camera)
        # translate_op = xform.AddTranslateOp()
        # translate_op.Set(new_position)

        # # Retrieve the camera position
        # translate_ops = xform.GetOrderedXformOps()
        # if translate_ops:
        #     current_position = translate_ops[0].Get()
        #     print(f"Camera position: {current_position}")
        # else:
        #     print("No translation operation found for the camera.")

        self._on_reset()

        self.count = 0

        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
            csvFile = csv.reader(file)
            self.rows = list(csvFile)
            # print(self.rows[5][3])
            for i in range(80):  # for i in range(1, 14):  # 1..13
                if(self.count == 0): self.Deck_Temp[self.count] = 0
                else:  self.Deck_Temp[self.count] = int(self.rows[self.count][3])
                # print(self.rows[self.count][3])
                # print(self.Deck_Position[self.count])
                # print(self.count)
                self.count += 1

        if layout_mode == 2:
            with open('C:/Terry/NVIDIA_Training/First_Project/Data/Results_Calander.csv', mode='r') as file:
                csvFile2 = csv.reader(file)
                self.rows2 = list(csvFile2)
                self.count = 1
                # print(self.rows[5][3])
                for i in range(655, 658):  # for i in range(1, 14):  # 1..13
                    self.Deck_Temp[self.count] = int(self.rows2[self.SliderDay_Value][i])
                    # print(self.rows[self.count][3])
                    # print(self.Deck_Position[self.count])
                    # print(self.count)
                    self.count += 1

        # self.Spirit_Label.text = str("Spirit : " + str(self.rows2[self.SliderDay_Value][693]))
        # self.Body_Label.text   = str("Body : " + str(self.rows2[self.SliderDay_Value][694]))
        # self.Mind_Label.text   = str("Mind : " + str(self.rows2[self.SliderDay_Value][695]))

        # self.Spirit_cur_Label.text = str("Spirit Cur : " + str(self.rows2[self.SliderDay_Value][696]))
        # self.Body_cur_Label.text   = str("Body Cur : " + str(self.rows2[self.SliderDay_Value][697]))
        # self.Mind_cur_Label.text   = str("Mind Cur : " + str(self.rows2[self.SliderDay_Value][698]))

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_1_Label'],
            new_translations=[440.0, 0.0, 1220.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4.5, 3.5, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_1_Label')],
            material_path=Sdf.Path('/World/Looks/Past_3_Card'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_2_Label'],
            new_translations=[0.0, 0.0, 1215.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4.5, 3.5, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_2_Label')],
            material_path=Sdf.Path('/World/Looks/Current_3_Card'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_3_Label'],
            new_translations=[-448.0, 0.0, 1215.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4.5, 3.5, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_3_Label')],
            material_path=Sdf.Path('/World/Looks/Future_3_Card'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_4_Label'],
            new_translations=[850.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_4_Label')],
            material_path=Sdf.Path('/World/Looks/Tower'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_5_Label'],
            new_translations=[850.0, -500.0, 1013.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_5_Label')],
            material_path=Sdf.Path('/World/Looks/Hermit'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_6_Label'],
            new_translations=[850.0, -500.0, 1776.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_6_Label')],
            material_path=Sdf.Path('/World/Looks/High_Priestess'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_7_Label'],
            new_translations=[425.0, -500.0, 1776.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_7_Label')],
            material_path=Sdf.Path('/World/Looks/Magician'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_8_Label'],
            new_translations=[425.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_8_Label')],
            material_path=Sdf.Path('/World/Looks/Devil'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_9_Label'],
            new_translations=[425.0, -500.0, 1013.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_9_Label')],
            material_path=Sdf.Path('/World/Looks/Leo'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_10_Label'],
            new_translations=[0.0, -500.0, 1776.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_10_Label')],
            material_path=Sdf.Path('/World/Looks/Emperor'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_11_Label'],
            new_translations=[0.0, -500.0, 1013.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_11_Label')],
            material_path=Sdf.Path('/World/Looks/Justice'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_12_Label'],
            new_translations=[0.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_12_Label')],
            material_path=Sdf.Path('/World/Looks/Moon'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_13_Label'],
            new_translations=[-425.0, -500.0, 1013.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_13_Label')],
            material_path=Sdf.Path('/World/Looks/Wheel_Fortune'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_14_Label'],
            new_translations=[-425.0, -500.0, 1776.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_14_Label')],
            material_path=Sdf.Path('/World/Looks/Empress'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_15_Label'],
            new_translations=[-425.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_15_Label')],
            material_path=Sdf.Path('/World/Looks/Star'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_16_Label'],
            new_translations=[-850.0, -500.0, 1776.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_16_Label')],
            material_path=Sdf.Path('/World/Looks/Lovers'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_17_Label'],
            new_translations=[-1275.0, -500.0, 1776.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_17_Label')],
            material_path=Sdf.Path('/World/Looks/Chariot'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_18_Label'],
            new_translations=[-850.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_18_Label')],
            material_path=Sdf.Path('/World/Looks/Judgement'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_19_Label'],
            new_translations=[-850.0, -500.0, 1013.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_19_Label')],
            material_path=Sdf.Path('/World/Looks/Death'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_20_Label'],
            new_translations=[-1275.0, -500.0, 1013.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_20_Label')],
            material_path=Sdf.Path('/World/Looks/Temperance'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_21_Label'],
            new_translations=[-1275.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_21_Label')],
            material_path=Sdf.Path('/World/Looks/World'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_22_Label'],
            new_translations=[-1275.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_22_Label')],
            material_path=Sdf.Path('/World/Looks/Sagittarius'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Band_Units')],
            material_path=Sdf.Path('/World/Looks/Band_Units'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Cylinder_Units')],
            material_path=Sdf.Path('/World/Looks/Band_Units'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')


        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Planet_Sun')],
            material_path=Sdf.Path('/World/Looks/_1910_Sun_19'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_1'],
            new_translations=[425.0, 0.0, 663.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[3.9, 6.75, 0.05])
            # old_translations=[1852.223442450999, 5.399999999999998, -4.7331654313260715e-31],
            # old_rotation_eulers=[90.0, 0.0, 0.0],
            # old_rotation_orders=[0, 1, 2],
            # old_scales=[2.75, 4.75, 0.05],
            # usd_context_name='',
            # time_code=0.0)

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_1')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[1]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_2'],
            new_translations=[0.0, 0.0, 663.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[3.9, 6.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_2')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[2]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_3'],
            new_translations=[-425.0, 0.0, 663.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[3.9, 6.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_3')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[3]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_4'],
            new_translations=[0.0, -500.0, 1426.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_4')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[4]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_5'],
            new_translations=[1275.0, -500.0, 1426.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_5')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[5]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_6'],
            new_translations=[350.0, -500.0, 1000.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_6')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[6]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_7'],
            new_translations=[0.0, -500.0, 1000.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_7')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[7]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_8'],
            new_translations=[425.0, -500.0, 663.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_8')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[8]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_9'],
            new_translations=[850.0, -500.0, 1426.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_9')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[9]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_10'],
            new_translations=[-1050.0, -500.0, 1000.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_10')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[10]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_11'],
            new_translations=[0.0, -500.0, 663.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_11')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[11]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_12'],
            new_translations=[700.0, -500.0, 500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_12')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[12]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_13'],
            new_translations=[350.0, -500.0, 500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_13')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[13]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_14'],
            new_translations=[0.0, -500.0, 500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_14')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[14]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_15'],
            new_translations=[-350.0, -500.0, 500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_15')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[15]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_16'],
            new_translations=[-700.0, -500.0, 500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_16')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[16]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_17'],
            new_translations=[-1050.0, -500.0, 500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_17')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[17]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_18'],
            new_translations=[0.0, -500.0, -100.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_18')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[18]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_19'],
            new_translations=[700.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_19')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[19]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_20'],
            new_translations=[350.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_20')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[20]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_21'],
            new_translations=[0.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_21')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[21]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_22'],
            new_translations=[-350.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_22')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[22]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_23'],
            new_translations=[-700.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_23')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[23]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_24'],
            new_translations=[-1050.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_24')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[24]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_25'],
            new_translations=[-1400.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_25')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[25]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

    def _on_one_card(self, layout_mode):
        """Called when the user presses the "Get From Selection" button"""
        # print('Three Card Layout Selected')

        # Camera Functions
        # import omni.usd
        # from pxr import UsdGeom, Gf
        # # Get the current USD stage
        stage = omni.usd.get_context().get_stage()

        # Define the camera path in the USD scene
        camera_path = "/World/Camera"

        # # Create a camera if it doesn't exist
        if not stage.GetPrimAtPath(camera_path):
            camera = UsdGeom.Camera.Define(stage, camera_path)
        else:
            camera = UsdGeom.Camera(stage.GetPrimAtPath(camera_path))

        # # Set camera position (x, y, z)
        new_position = Gf.Vec3d(100, 50, 200)  # Example position in centimeters
        xform = UsdGeom.Xformable(camera)
        # translate_op = xform.AddTranslateOp()
        # translate_op.Set(new_position)

        # # Retrieve the camera position
        # translate_ops = xform.GetOrderedXformOps()
        # if translate_ops:
        #     current_position = translate_ops[0].Get()
        #     print(f"Camera position: {current_position}")
        # else:
        #     print("No translation operation found for the camera.")

        self._on_reset()

        self.count = 0

        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
            csvFile = csv.reader(file)
            self.rows = list(csvFile)
            # print(self.rows[5][3])
            for i in range(80):  # for i in range(1, 14):  # 1..13
                if(self.count == 0): self.Deck_Temp[self.count] = 0
                else:  self.Deck_Temp[self.count] = int(self.rows[self.count][3])
                # print(self.rows[self.count][3])
                # print(self.Deck_Position[self.count])
                # print(self.count)
                self.count += 1

        if layout_mode == 2:
            with open('C:/Terry/NVIDIA_Training/First_Project/Data/Results_Calander.csv', mode='r') as file:
                csvFile2 = csv.reader(file)
                self.rows2 = list(csvFile2)
                self.count = 1
                # print(self.rows[5][3])
                for i in range(654, 655):  # for i in range(1, 14):  # 1..13
                    self.Deck_Temp[self.count] = int(self.rows2[self.SliderDay_Value][i])
                    # print(self.rows[se
                    # print(self.Deck_Position[self.count])
                    # print(self.count)
                    self.count += 1

        self.Spirit_Label.text = str("Spirit : " + str(round(float(self.rows2[self.SliderDay_Value][693]), 2)))
        self.Body_Label.text   = str("Body : " + str(round(float(self.rows2[self.SliderDay_Value][694]), 2)))
        self.Mind_Label.text   = str("Mind : " + str(round(float(self.rows2[self.SliderDay_Value][695]), 2)))

        self.Spirit_cur_Label.text = str("Spirit Cur : " + str(round(float(self.rows2[self.SliderDay_Value][696]), 2)))
        self.Body_cur_Label.text   = str("Body Cur : " + str(round(float(self.rows2[self.SliderDay_Value][697]), 2)))
        self.Mind_cur_Label.text   = str("Mind Cur : " + str(round(float(self.rows2[self.SliderDay_Value][698]), 2)))

        text = self.rows2[self.SliderDay_Value][3]
        parts = text.split('/')
        self.TestMonth = int(parts[0])
        self.TestDay = int(parts[1])
        self.TestYear = int(parts[2])

        # import omni
        # import omni.usd
        # from pxr import Sdf
        # import omni.kit.commands

        tempMind = round(float(self.rows2[self.SliderDay_Value][695]) / 5.0) # self.rows2[5][695] self.SliderDay_Value
        if(tempMind < 0): tempMind = (tempMind / -1) + 11
        else: tempMind += 1
        tempMind = round(float(tempMind))

        omni.kit.commands.execute('ChangeProperty',
            prop_path=Sdf.Path('/World/UI/Frame/Label.omni:ui:Label:text'),
            value=self.rows[tempMind][6],
            prev='Label_Test',
            target_layer=Sdf.Find('file:/C:/Terry/NVIDIA_Training/First_Project/Entanglement%20Tarot.usd'),
            usd_context_name=omni.usd.get_context().get_stage())

        # omni.kit.commands.execute('ChangePropertyCommand',
        #     prop_path=['/World/UI/Frame/Label.text'],
        #     value = "New text value",
        #     prev = "Label",
        #     )

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Calander_Tarot_Name'],
            new_translations=[0, 0.0, 200.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Calander_Tarot_Name')],
            material_path=Sdf.Path('/World/Looks/Sun'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Calander_Tarot_Info'],
            new_translations=[1196.0, 0.0, 754.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[12, 12, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Calander_Tarot_Info')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[1]][9]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Calander_Mind'],
            new_translations=[-1348.0, 0.0, 1361.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[15, 6, 1])

        # 693, 694, 695, Spirit Body Mind
        # 696, 697, 698, Spirit_cur Body_cur Mind_cur

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Calander_Mind')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[tempMind][6]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Calander_Body'],
            new_translations=[-1344.0, 0.0, 753.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[15, 6, 1])

        tempBody = round(float(self.rows2[self.SliderDay_Value][694]) / 5.0) # self.SliderDay_Value
        if(tempBody < 0): tempBody = (tempBody / -1) + 11
        else: tempBody += 1
        tempBody = round(float(tempBody))

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Calander_Body')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[tempBody][7]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Calander_Spirit'],
            new_translations=[-1342.0, 0.0, 141.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[15, 6, 1])

        tempSpirit = round(float(self.rows2[self.SliderDay_Value][693]) / 5.0) # self.SliderDay_Value
        if(tempSpirit < 0): tempSpirit = (tempSpirit / -1) + 11
        else: tempSpirit += 1
        tempSpirit = round(float(tempSpirit))

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Calander_Spirit')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[tempSpirit][8]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Calander_Month'],
            new_translations=[797.0, 0.0, 1869.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[8, 4, 1])

        # tempSpirit = round(float(self.rows2[self.SliderDay_Value][693]) / 5.0) # self.SliderDay_Value
        # if(tempSpirit < 0): tempSpirit = (tempSpirit / -1) + 11
        # else: tempSpirit += 1
        # tempSpirit = round(float(tempSpirit))

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Calander_Month')],
            material_path=Sdf.Path('/World/Looks/Calander_' + self.rows[self.TestMonth + 23][6]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Calander_Day'],
            new_translations=[2.0, 0.0, 1875.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[8, 6, 1])

        # tempSpirit = round(float(self.rows2[self.SliderDay_Value][693]) / 5.0) # self.SliderDay_Value
        # if(tempSpirit < 0): tempSpirit = (tempSpirit / -1) + 11
        # else: tempSpirit += 1
        # tempSpirit = round(float(tempSpirit))

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Calander_Day')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.TestDay + 23][7]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Calander_Year'],
            new_translations=[-812.0, 0.0, 1866.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[8, 6, 1])

        # tempYear = round(float(self.rows2[self.SliderDay_Value][693]) / 5.0) # self.SliderDay_Value
        # if(tempYear < 0): tempYear = (tempYear / -1) + 11
        # else: tempYear += 1
        # tempYear = round(float(tempYear))

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Calander_Year')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[(self.TestYear) + 24][8]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_1'],
            new_translations=[0.0, 0.0, 663.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[11.5, 20.0, 0.05])
            # old_translations=[1852.223442450999, 5.399999999999998, -4.7331654313260715e-31],
            # old_rotation_eulers=[90.0, 0.0, 0.0],
            # old_rotation_orders=[0, 1, 2],
            # old_scales=[2.75, 4.75, 0.05],
            # usd_context_name='',
            # time_code=0.0)

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_1')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[1]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        self.sync_function()

    def sync_function(self):
        result = run_coroutine(self.load_stage_async())


    def _on_collider(self, layout_mode):
        """Called when the user presses the "Get From Selection" button"""
        #print('Collider Layout Selected')

        self._on_reset()

        self.count = 0
        TempFormat = 3
        if(self.SliderLeft_Value1 == 1):
            TempFormat = 4

        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
            csvFile = csv.reader(file)
            self.rows = list(csvFile)
            # print(self.rows[5][3])
            for i in range(80):  # for i in range(1, 14):  # 1..13
                if(self.count == 0): self.Deck_Temp[self.count] = 0
                else:  self.Deck_Temp[self.count] = int(self.rows[self.count][TempFormat])
                # print(self.rows[self.count][3])
                # print(self.Deck_Position[self.count])
                # print(self.count)
                self.count += 1

        if layout_mode == 2:
            with open('C:/Terry/NVIDIA_Training/First_Project/Data/Results_Calander.csv', mode='r') as file:
                csvFile2 = csv.reader(file)
                self.rows2 = list(csvFile2)
                self.count = 1
                # print(self.rows[5][3])
                for i in range(658, 671):  # for i in range(1, 14):  # 1..13
                    self.Deck_Temp[self.count] = int(self.rows2[4][i])
                    # print(self.rows[self.count][3])
                    # print(self.Deck_Position[self.count])
                    # print(self.count)
                    self.count += 1

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_1_Label'],
            new_translations=[0.0, 0.0, 1195.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_1_Label')],
            material_path=Sdf.Path('/World/Looks/Collider_Target'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_2_Label'],
            new_translations=[1300.0, 0.0, 820.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_2_Label')],
            material_path=Sdf.Path('/World/Looks/Emperor'),
            # material_path=Sdf.Path('/World/Looks/_1910_Emperor_4'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_3_Label'],
            new_translations=[1072.0, 0.0, 135.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_3_Label')],
            material_path=Sdf.Path('/World/Looks/Taurus'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_4_Label'],
            new_translations=[645.0, 0.0, -290.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_4_Label')],
            material_path=Sdf.Path('/World/Looks/Lovers'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_5_Label'],
            new_translations=[0.0, 0.0, -452.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_5_Label')],
            material_path=Sdf.Path('/World/Looks/Chariot'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_6_Label'],
            new_translations=[-650.0, 0.0, 1936.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_6_Label')],
            material_path=Sdf.Path('/World/Looks/Temperance'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_7_Label'],
            new_translations=[-1072.0, 0.0, 135.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_7_Label')],
            material_path=Sdf.Path('/World/Looks/Hermit'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_8_Label'],
            new_translations=[-1300.0, 0.0, 820.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_8_Label')],
            material_path=Sdf.Path('/World/Looks/Justice'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_9_Label'],
            new_translations=[-1082.0, 0.0, 1545.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_9_Label')],
            material_path=Sdf.Path('/World/Looks/Death'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_10_Label'],
            new_translations=[-656.0, 0.0, -280.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_10_Label')],
            material_path=Sdf.Path('/World/Looks/Leo'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_11_Label'],
            new_translations=[0.0, 0.0, 2065.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_11_Label')],
            material_path=Sdf.Path('/World/Looks/Devil'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_12_Label'],
            new_translations=[644.0, 0.0, 1936.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_12_Label')],
            material_path=Sdf.Path('/World/Looks/Star'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_13_Label'],
            new_translations=[1082.0, 0.0, 1545.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_13_Label')],
            material_path=Sdf.Path('/World/Looks/High_Priestess'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_14_Label'],
            new_translations=[-425.0, -500.0, 1776.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_14_Label')],
            material_path=Sdf.Path('/World/Looks/Empress'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_15_Label'],
            new_translations=[-425.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_15_Label')],
            material_path=Sdf.Path('/World/Looks/Star'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_16_Label'],
            new_translations=[-850.0, -500.0, 1776.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_16_Label')],
            material_path=Sdf.Path('/World/Looks/Lovers'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_17_Label'],
            new_translations=[-1275.0, -500.0, 1776.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_17_Label')],
            material_path=Sdf.Path('/World/Looks/Chariot'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_18_Label'],
            new_translations=[-850.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_18_Label')],
            material_path=Sdf.Path('/World/Looks/Judgement'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_19_Label'],
            new_translations=[-850.0, -500.0, 1013.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_19_Label')],
            material_path=Sdf.Path('/World/Looks/Death'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_20_Label'],
            new_translations=[-1275.0, -500.0, 1013.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_20_Label')],
            material_path=Sdf.Path('/World/Looks/Temperance'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_21_Label'],
            new_translations=[-1275.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_21_Label')],
            material_path=Sdf.Path('/World/Looks/World'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_21_Label'],
            new_translations=[-1275.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_22_Label')],
            material_path=Sdf.Path('/World/Looks/Sagittarius'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_1'],
            new_translations=[0.0, 0.0, 840.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])
        #     # old_translations=[1852.223442450999, 5.399999999999998, -4.7331654313260715e-31],
            # old_rotation_eulers=[90.0, 0.0, 0.0],
            # old_rotation_orders=[0, 1, 2],
            # old_scales=[2.75, 4.75, 0.05],
            # usd_context_name='',
            # time_code=0.0)

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_1')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[1]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_2'],
            new_translations=[945.0, 0.0, 817.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_2')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[2]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_3'],
            new_translations=[718.0, 0.0, 300.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_3')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[3]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_4'],
            new_translations=[367.0, 0.0, 59.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_4')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[4]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_5'],
            new_translations=[10.0, 0.0, -50.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_5')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[5]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_6'],
            new_translations=[-357.0, 0.0, 75.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_6')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[6]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_7'],
            new_translations=[-670.0, 0.0, 317.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_7')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[7]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_8'],
            new_translations=[-944.0, 0.0, 841.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_8')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[8]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_9'],
            new_translations=[-700.0, 0.0, 1325.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_9')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[9]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_10'],
            new_translations=[-380.0, 0.0, 1536.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_10')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[10]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_11'],
            new_translations=[-6.0, 0.0, 1650.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_11')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[11]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_12'],
            new_translations=[395.0, 0.0, 1533.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_12')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[12]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_13'],
            new_translations=[728.0, 0.0, 1311.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_13')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[13]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_14'],
            new_translations=[0.0, -500.0, 500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_14')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[14]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_15'],
            new_translations=[-350.0, -500.0, 500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_15')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[15]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_16'],
            new_translations=[-700.0, -500.0, 500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_16')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[16]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_17'],
            new_translations=[-1050.0, -500.0, 500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_17')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[17]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_18'],
            new_translations=[1050.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_18')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[18]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_19'],
            new_translations=[700.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_19')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[19]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_20'],
            new_translations=[350.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_20')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[20]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_21'],
            new_translations=[0.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_21')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[21]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_22'],
            new_translations=[-350.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_22')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[22]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_23'],
            new_translations=[-700.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_23')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[23]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_24'],
            new_translations=[-1050.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_24')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[24]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_25'],
            new_translations=[-1400.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_25')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[25]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

    def _on_chakra(self, layout_mode):
        """Called when the user presses the "Get From Selection" button"""
        #print('Chakra Layout Selected')

        self._on_reset()

        self.count = 0

        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
            csvFile = csv.reader(file)
            self.rows = list(csvFile)
            # print(self.rows[5][3])
            TempFormat = 3
            if(self.SliderRight_Value2 == 1):
                TempFormat = 5
            for i in range(80):  # for i in range(1, 14):  # 1..13
                if(self.count == 0): self.Deck_Position[self.count] = 0
                else:  self.Deck_Position[self.count] = int(self.rows[self.count][TempFormat])
                # print(self.rows[self.count][3])
                # print(self.Deck_Position[self.count])
                # print(self.count)
                self.count += 1

        if layout_mode == 2:
            with open('C:/Terry/NVIDIA_Training/First_Project/Data/Results_Calander.csv', mode='r') as file:
                csvFile2 = csv.reader(file)
                self.rows2 = list(csvFile2)
                self.count = 1
                # print(self.rows[5][3])
                for i in range(671, 693):  # for i in range(1, 14):  # 1..13
                    self.Deck_Position[self.count] = int(self.rows2[4][i])
                    # print(self.rows[self.count][3])
                    # print(self.Deck_Position[self.count])
                    # print(self.count)
                    self.count += 1

        # print('Chakra Layout TempFormat: ' + str(TempFormat))
        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_1_Label'],
            new_translations=[1279.0, 0.0, 293.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_1_Label')],
            material_path=Sdf.Path('/World/Looks/Sun'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_2_Label'],
            new_translations=[1279.0, 0.0, 1049.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_2_Label')],
            material_path=Sdf.Path('/World/Looks/Hanged_Man'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_3_Label'],
            new_translations=[1279.0, 0.0, 1818.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_3_Label')],
            material_path=Sdf.Path('/World/Looks/Taurus'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_4_Label'],
            new_translations=[850.0, 0.0, 293.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_4_Label')],
            material_path=Sdf.Path('/World/Looks/Tower'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_5_Label'],
            new_translations=[850.0, 0.0, 1049.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_5_Label')],
            material_path=Sdf.Path('/World/Looks/Hermit'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_6_Label'],
            new_translations=[850.0, 0.0, 1818.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_6_Label')],
            material_path=Sdf.Path('/World/Looks/High_Priestess'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_7_Label'],
            new_translations=[425.0, 0.0, 1818.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_7_Label')],
            material_path=Sdf.Path('/World/Looks/Magician'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_8_Label'],
            new_translations=[425.0, 0.0, 293.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_8_Label')],
            material_path=Sdf.Path('/World/Looks/Devil'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_9_Label'],
            new_translations=[425.0, 0.0, 1049.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_9_Label')],
            material_path=Sdf.Path('/World/Looks/Leo'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_10_Label'],
            new_translations=[0.0, 0.0, 1818.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_10_Label')],
            material_path=Sdf.Path('/World/Looks/Emperor'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_11_Label'],
            new_translations=[0.0, 0.0, 1049.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_11_Label')],
            material_path=Sdf.Path('/World/Looks/Justice'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_12_Label'],
            new_translations=[0.0, 0.0, 293.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_12_Label')],
            material_path=Sdf.Path('/World/Looks/Moon'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_13_Label'],
            new_translations=[-425.0, 0.0, 1049.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_13_Label')],
            material_path=Sdf.Path('/World/Looks/Wheel_Fortune'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_14_Label'],
            new_translations=[-425.0, 0.0, 1818.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_14_Label')],
            material_path=Sdf.Path('/World/Looks/Empress'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_15_Label'],
            new_translations=[-425.0, 0.0, 293.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_15_Label')],
            material_path=Sdf.Path('/World/Looks/Star'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_16_Label'],
            new_translations=[-850.0, 0.0, 1818.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_16_Label')],
            material_path=Sdf.Path('/World/Looks/Lovers'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_17_Label'],
            new_translations=[-1275.0, 0.0, 1818.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_17_Label')],
            material_path=Sdf.Path('/World/Looks/Chariot'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_18_Label'],
            new_translations=[-850.0, 0.0, 293.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_18_Label')],
            material_path=Sdf.Path('/World/Looks/Judgement'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_19_Label'],
            new_translations=[-850.0, 0.0, 1049.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_19_Label')],
            material_path=Sdf.Path('/World/Looks/Death'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_20_Label'],
            new_translations=[-1275.0, 0.0, 1049.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_20_Label')],
            material_path=Sdf.Path('/World/Looks/Temperance'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_21_Label'],
            new_translations=[-1275.0, 0.0, 293.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2.85, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_21_Label')],
            material_path=Sdf.Path('/World/Looks/World'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_22_Label')],
            material_path=Sdf.Path('/World/Looks/Sagittarius'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_1'],
            new_translations=[425.0, 0.0, 1426.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])
        #     # old_translations=[1852.223442450999, 5.399999999999998, -4.7331654313260715e-31],
            # old_rotation_eulers=[90.0, 0.0, 0.0],
            # old_rotation_orders=[0, 1, 2],
            # old_scales=[2.75, 4.75, 0.05],
            # usd_context_name='',
            # time_code=0.0)

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_1')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[1]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='strongerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_2'],
            new_translations=[850.0, 0.0, 1426.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_2')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[2]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='strongerThanDescendants')

        # print('Chakra Layout TempFormat: ' + str(TempFormat))

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_3'],
            new_translations=[-425.0, 0.0, 1426.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_3')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[3]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='strongerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_4'],
            new_translations=[0.0, 0.0, 1430.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_4')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[4]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_5'],
            new_translations=[1275.0, 0.0, 1426.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_5')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[5]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_6'],
            new_translations=[-850.0, 0.0, 1426.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_6')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[6]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_7'],
            new_translations=[-1275.0, 0.0, 1426.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_7')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[7]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_8'],
            new_translations=[425.0, 0.0, 663.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_8')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[8]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_9'],
            new_translations=[850.0, 0.0, 663.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_9')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[9]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_10'],
            new_translations=[-850.0, 0.0, 663.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_10')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[10]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_11'],
            new_translations=[0.0, 0.0, 663.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_11')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[11]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_12'],
            new_translations=[1275.0, 0.0, 663.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_12')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[12]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_13'],
            new_translations=[-425.0, 0.0, 663.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_13')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[13]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_14'],
            new_translations=[-1275.0, 0.0, 663.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_14')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[14]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_15'],
            new_translations=[425.0, 0.0, -100.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_15')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[15]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_16'],
            new_translations=[850.0, 0.0, -100.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_16')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[16]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_17'],
            new_translations=[-425.0, 0.0, -100.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_17')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[17]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_18'],
            new_translations=[0.0, 0.0, -100.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_18')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[18]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_19'],
            new_translations=[1275.0, 0.0, -100.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_19')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[19]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_20'],
            new_translations=[-850.0, 0.0, -100.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_20')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[20]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_21'],
            new_translations=[-1275.0, 0.0, -100.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_21')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[21]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_22'],
            new_translations=[-350.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_22')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[22]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_23'],
            new_translations=[-700.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_23')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[23]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_24'],
            new_translations=[-1050.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_24')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[24]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_25'],
            new_translations=[-1400.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_25')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Position[25]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')


    def _on_reset(self):
        """Called when the user presses the "Get From Selection" button"""
        #print('On Reset Selected')

        # # Get stage.
        # stage = omni.usd.get_context().get_stage()

        # # Get selection.
        # selection = omni.usd.get_context().get_selection()
        # paths = selection.get_selected_prim_paths()

        # for path in paths:
        #     prim = stage.GetPrimAtPath(path)
        #     if prim.IsValid():
        #         # Unbind Material.
        #         UsdShade.MaterialBindingAPI(prim).UnbindAllBindings()

        self.count = 0

        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
            csvFile = csv.reader(file)
            self.rows = list(csvFile)
            # print(self.rows[5][3])
            for i in range(80):  # for i in range(1, 14):  # 1..13
                if(self.count == 0): self.Deck_Position[self.count] = 0
                else:  self.Deck_Position[self.count] = int(self.rows[self.count][3])
                # print(self.rows[self.count][3])
                # print(self.Deck_Position[self.count])
                # print(self.count)
                self.count += 1

        # omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
        #     count=1,
        #     paths=['/World/Card_Background'],
        #     new_translations=[0.0, -250.0, 780.0],
        #     new_rotation_eulers=[90.0, 0.0, 0.0],
        #     new_rotation_orders=[0, 1, 2],
        #     new_scales=[2.75, 4.75, 0.05])

        # omni.kit.commands.execute('BindMaterialCommand',
        #     prim_path=[Sdf.Path('/World/ard_Background')],
        #     material_path=Sdf.Path('/World/Looks/' + "Card_Background"),
        #     # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
        #     strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Calander_Tarot_Name'],
            new_translations=[425.0, -500.0, 1125.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Calander_Tarot_Name')],
            material_path=Sdf.Path('/World/Looks/Sun'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Calander_Tarot_Info'],
            new_translations=[425.0, -500.0, 1125.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Calander_Tarot_Info')],
            material_path=Sdf.Path('/World/Looks/Sun'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Calander_Mind'],
            new_translations=[425.0, -500.0, 1125.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Calander_Mind')],
            material_path=Sdf.Path('/World/Looks/Sun'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Calander_Body'],
            new_translations=[425.0, -500.0, 1125.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Calander_Body')],
            material_path=Sdf.Path('/World/Looks/Sun'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Calander_Spirit'],
            new_translations=[425.0, -500.0, 1125.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Calander_Spirit')],
            material_path=Sdf.Path('/World/Looks/Sun'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_1_Label'],
            new_translations=[425.0, -500.0, 1125.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_1_Label')],
            material_path=Sdf.Path('/World/Looks/Sun'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_2_Label'],
            new_translations=[0.0, -500.0, 1125.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_2_Label')],
            material_path=Sdf.Path('/World/Looks/Hanged_Man'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_3_Label'],
            new_translations=[-425.0, -500.0, 1125.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_3_Label')],
            material_path=Sdf.Path('/World/Looks/Taurus'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_4_Label'],
            new_translations=[850.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_4_Label')],
            material_path=Sdf.Path('/World/Looks/Tower'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_5_Label'],
            new_translations=[850.0, -500.0, 1013.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_5_Label')],
            material_path=Sdf.Path('/World/Looks/Hermit'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_6_Label'],
            new_translations=[850.0, -500.0, 1776.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_6_Label')],
            material_path=Sdf.Path('/World/Looks/High_Priestess'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_7_Label'],
            new_translations=[425.0, -500.0, 1776.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_7_Label')],
            material_path=Sdf.Path('/World/Looks/Magician'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_8_Label'],
            new_translations=[425.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_8_Label')],
            material_path=Sdf.Path('/World/Looks/Devil'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_9_Label'],
            new_translations=[425.0, -500.0, 1013.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_9_Label')],
            material_path=Sdf.Path('/World/Looks/Leo'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_10_Label'],
            new_translations=[0.0, -500.0, 1776.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_10_Label')],
            material_path=Sdf.Path('/World/Looks/Emperor'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_11_Label'],
            new_translations=[0.0, -500.0, 1013.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_11_Label')],
            material_path=Sdf.Path('/World/Looks/Justice'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_12_Label'],
            new_translations=[0.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_12_Label')],
            material_path=Sdf.Path('/World/Looks/Moon'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_13_Label'],
            new_translations=[-425.0, -500.0, 1013.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_13_Label')],
            material_path=Sdf.Path('/World/Looks/Wheel_Fortune'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_14_Label'],
            new_translations=[-425.0, -500.0, 1776.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_14_Label')],
            material_path=Sdf.Path('/World/Looks/Empress'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_15_Label'],
            new_translations=[-425.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_15_Label')],
            material_path=Sdf.Path('/World/Looks/Star'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_16_Label'],
            new_translations=[-850.0, -500.0, 1776.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_16_Label')],
            material_path=Sdf.Path('/World/Looks/Lovers'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_17_Label'],
            new_translations=[-1275.0, -500.0, 1776.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_17_Label')],
            material_path=Sdf.Path('/World/Looks/Chariot'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_18_Label'],
            new_translations=[-850.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_18_Label')],
            material_path=Sdf.Path('/World/Looks/Judgement'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_19_Label'],
            new_translations=[-850.0, -500.0, 1013.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_19_Label')],
            material_path=Sdf.Path('/World/Looks/Death'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_20_Label'],
            new_translations=[-1275.0, -500.0, 1013.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_20_Label')],
            material_path=Sdf.Path('/World/Looks/Temperance'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_21_Label'],
            new_translations=[-1275.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_21_Label')],
            material_path=Sdf.Path('/World/Looks/World'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_22_Label'],
            new_translations=[-1275.0, -500.0, 250.0],
            new_rotation_eulers=[90.0, 0.0, 180.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[4, 2, 1])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_22_Label')],
            material_path=Sdf.Path('/World/Looks/Sagittarius'),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_1'],
            new_translations=[350.0, -500.0, 1500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])
            # old_translations=[1852.223442450999, 5.399999999999998, -4.7331654313260715e-31],
            # old_rotation_eulers=[90.0, 0.0, 0.0],
            # old_rotation_orders=[0, 1, 2],
            # old_scales=[2.75, 4.75, 0.05],
            # usd_context_name='',
            # time_code=0.0)


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_2'],
            new_translations=[0.0, -500.0, 1500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_3'],
            new_translations=[-350.0, -500.0, 1500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_4'],
            new_translations=[1050.0, -500.0, 1000.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_5'],
            new_translations=[700.0, -500.0, 1000.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_6'],
            new_translations=[350.0, -500.0, 1000.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_7'],
            new_translations=[0.0, -500.0, 1000.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_8'],
            new_translations=[-350.0, -500.0, 1000.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_9'],
            new_translations=[-700.0, -500.0, 1000.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_10'],
            new_translations=[-1050.0, -500.0, 1000.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_11'],
            new_translations=[1050.0, -500.0, 500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_12'],
            new_translations=[700.0, -500.0, 500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_13'],
            new_translations=[350.0, -500.0, 500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_14'],
            new_translations=[0.0, -500.0, 500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_15'],
            new_translations=[-350.0, -500.0, 500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_16'],
            new_translations=[-700.0, -500.0, 500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_17'],
            new_translations=[-1050.0, -500.0, 500.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_18'],
            new_translations=[1050.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_19'],
            new_translations=[700.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_20'],
            new_translations=[350.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_21'],
            new_translations=[0.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_22'],
            new_translations=[-350.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_23'],
            new_translations=[-700.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_24'],
            new_translations=[-1050.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])


        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_25'],
            new_translations=[-1400.0, -500.0, 0.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

    def _on_test_deck(self):
        """Called when the user presses the "Get From Selection" button"""
        # print('On Test Deck')

        self.test_deck = np.zeros(80, dtype=int)

        for i in range(80):  # for i in range(1, 14):  # 1..13
             self.test_deck[i] = i

        for i in range(1, 79):  # for i in range(1, 14):  # 1..13
            for t in range(1, 79):
                if(self.test_deck[i] == self.Deck_Temp[t]):
                    self.test_deck[i] = 100

        for i in range(1, 79):  # for i in range(1, 14):  # 1..13
            if(self.test_deck[i] < 100):
                print('Test Deck missing or zero: ' + str(i))
        # print('--- End of Test Deck ---')