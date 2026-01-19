from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.ui as ui
from .style import scatter_window_style
from .utils import get_selection
from .combo_box_model import ComboBoxModel
from .scatter import scatter
from .utils import duplicate_prims

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

class ScatterWindow(ui.Window):
    """The class that represents the window"""

    def __init__(self, title: str, delegate=None, **kwargs):
        self.__label_width = LABEL_WIDTH

        super().__init__(title, **kwargs)

        self.Deck_Position = np.zeros(80, dtype=int)
        self.Deck_Cut_Left = np.zeros(80, dtype=int)
        self.Deck_Cut_Middle = np.zeros(80, dtype=int)
        self.Deck_Cut_Right = np.zeros(80, dtype=int)
        self.Deck_Temp = np.zeros(80, dtype=int)
        self.rows = []
        self.count = 0
        self.count_Left = 0
        self.count_Right = 0
        self.count_Temp = 0
        self.Slider_Value = 38
        self.Slider_Value1 = 50
        self.Slider_Value2 = 50
        self.Stack1Button = None
        self.Stack2Button = None
        self.Stack3Button = None
        self.StackCombine = 0
        self.Load_Point = 1

        # Define the data and data types
        data = [('Alice', 25, 55.0), ('Bob', 32, 60.5)]
        dtypes = [('name', 'U10'), ('age', 'i4'), ('weight', 'f4')]

        # Create the structured array
        people = np.array(data, dtype=dtypes)

        # Accessing and modifying structured arrays
        print(people['name']) # Output: ['Alice' 'Bob']
        people['age'] += 1
        print(people['age']) # Output: [26 33]

        # # Generate 5 unique random integers between 0 and 100
        # random_numbers = random.sample(range(1, 79), 78)
        # print(random_numbers)




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

        # Apply the style to all the widgets of this window
        self.frame.style = scatter_window_style
        # Set the function that is called to build widgets when the window is
        # visible
        self.frame.set_build_fn(self._build_fn)

    def _build_fn(self):
        """
        The method that is called to build all the UI once the window is
        visible.
        """
        with ui.ScrollingFrame():
            with ui.VStack(height=0):
                # The Go button
                ui.Button("Shuffle", clicked_fn=self._on_scatter)
                # Create the UIntSlider
                slider = ui.UIntSlider(min=1, max=78, step=1)
                slider.model.set_value(50)  # Set initial value
                slider.model.add_value_changed_fn(lambda m: self.on_slider_changed(slider))
                self._build_Cut_Deck()
                self._build_Card_Layout()
                self._build_source()
                #self._build_scatter()
                #self._build_axis(0, "X Axis")
                #self._build_axis(1, "Y Axis")
                #self._build_axis(2, "Z Axis")


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

   # Callback function for slider value changes
    def on_slider_changed(self, slider):
        self.Slider_Value = slider.model.get_value_as_int()
        print(f"Slider value changed to: {self.Slider_Value}")

    def _build_Cut_Deck(self):
        """Build the widgets of the "Cut Deck" group"""
        with ui.CollapsableFrame("Cut Deck", name="group"):
            with ui.VStack(height=0, spacing=SPACING):
                ui.Button("Cut Three Stacks", clicked_fn=self._on_cut_deck)
                self.slider1 = ui.UIntSlider(min=1, max=78, step=1)
                self.slider1.model.set_value(50)  # Set initial value
                self.slider1.model.add_value_changed_fn(lambda m: self.on_slider_cut1(self.slider1))

                self.slider2 = ui.UIntSlider(min=1, max=78, step=1)
                self.slider2.model.set_value(50)  # Set initial value
                self.slider2.model.add_value_changed_fn(lambda m: self.on_slider_cut2(self.slider2))

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
                ui.Button("Three_Card", clicked_fn=self._on_three_card)
                ui.Button("Collider", clicked_fn=self._on_collider)
                ui.Button("Chakra", clicked_fn=self._on_chakra)


    def _build_source(self):
        """Build the widgets of the "Source" group"""
        with ui.CollapsableFrame("Source", name="group"):
            with ui.VStack(height=0, spacing=SPACING):
                with ui.HStack():
                    ui.Label("Prim", name="attribute_name", width=self.label_width)
                    ui.StringField(model=self._source_prim_model)
                    # Button that puts the selection to the string field
                    ui.Button(
                        " S ",
                        width=0,
                        height=0,
                        style={"margin": 0},
                        clicked_fn=self._on_get_selection,
                        tooltip="Get From Selection",
                    )

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
            print("Load File: ",self.rows[5][3])
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

        print("Left Deck Cut:")
        # Cut the Deck into Left, Middle, Right
        for i in range(self.count_Left):  # for i in range(1, 14):  # 1..13  (// is floor division)
            self.Deck_Cut_Left[i] = self.Deck_Position[i]
            print(self.Deck_Cut_Left[i])
            # print(self.count)

        self.count = 0  # Skip Header

        print("Middle Deck Cut:")
        for i in range(self.count_Middle):  # for i in range(1, 14):  # 1..13
            self.Deck_Cut_Middle[i] = self.Deck_Position[i + self.count_Left]
            print(self.Deck_Cut_Middle[i])
            # print(self.count)

        self.count = 0  # Skip Header

        print("Right Deck Cut:")
        for i in range(self.count_Right):  # for i in range(1, 14):  # 1..13
            self.Deck_Cut_Right[i] = self.Deck_Position[i + self.count_Left + self.count_Middle]
            print(self.Deck_Cut_Right[i])
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
        self.slider2.max = (78 - self.Slider_Value1)
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

        print("Left Deck Cut:")
        # Cut the Deck into Left, Middle, Right
        for i in range(1, self.Slider_Value):  # for i in range(1, 14):  # 1..13
            if(self.count == 0): self.Deck_Cut_Left[self.count] = 0
            else:  self.Deck_Cut_Left[self.count] = self.Deck_Position[self.count]
            print(self.Deck_Cut_Left[self.count])
            # print(self.count)
            self.count += 1

        self.count = 1  # Skip Header

        print("Right Deck Cut:")
        for i in range(self.Slider_Value, 79):  # for i in range(1, 14):  # 1..13
            self.Deck_Cut_Right[self.count] = self.Deck_Position[i]
            print(self.Deck_Cut_Right[self.count])
            # print(self.count)
            self.count += 1

        self.count = random.randint(1, 10)  # Left Right Toggle
        self.count_Left = 1
        self.count_Right = 1
        self.count_Temp = 0

        print("Temp Deck result:")
        for i in range(1, 80):  # for i in range(1, 14):  # 1..13
            if(self.count < 6):
                if(self.Deck_Cut_Left[self.count_Left] != 0):
                    self.Deck_Temp[i] = self.Deck_Cut_Left[self.count_Left]
                    self.count_Left += 1
                else:
                    if(self.Deck_Cut_Right[self.count_Right] != 0):
                        self.Deck_Temp[i] = self.Deck_Cut_Right[self.count_Right]
                        self.count_Right += 1
            if(self.count >= 6):
                if(self.Deck_Cut_Right[self.count_Right] != 0):
                    self.Deck_Temp[i] = self.Deck_Cut_Right[self.count_Right]
                    self.count_Right += 1
                else:
                    if(self.Deck_Cut_Left[self.count_Left] != 0):
                        self.Deck_Temp[i] = self.Deck_Cut_Left[self.count_Left]
                        self.count_Left += 1

            self.count -= 1
            condition = (self.count == 0) or (self.count == 5) # Boolean equation form
            if condition:
                self.count = random.randint(1, 10)

        random_numbers = random.sample(range(1, 79), 78)
        #print(random_numbers) # random_numbers[1]][0] rows[self.Deck_Temp[1]][0]),

        self._on_save_cards()
        print("Scatter Save Cards: ")

        # with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
        #     csvFile = csv.reader(file)
        #     self.rows = list(csvFile)
        #     print(self.rows[5][0])
        #     #for lines in csvFile:
        #     #   print(lines)

        # for i in range(0, 80):
        #         self.rows[i][3] = self.Deck_Temp[i]

        # # Data to be written
        # data = [
        #     [self.rows[0][0], self.rows[0][1], self.rows[0][2], self.rows[0][3]],
        #     [self.rows[1][0], self.rows[1][1], self.rows[1][2], self.rows[1][3]],
        #     [self.rows[2][0], self.rows[2][1], self.rows[2][2], self.rows[2][3]],
        #     [self.rows[3][0], self.rows[3][1], self.rows[3][2], self.rows[3][3]],
        #     [self.rows[4][0], self.rows[4][1], self.rows[4][2], self.rows[4][3]],
        #     [self.rows[5][0], self.rows[5][1], self.rows[5][2], self.rows[5][3]],
        #     [self.rows[6][0], self.rows[6][1], self.rows[6][2], self.rows[6][3]],
        #     [self.rows[7][0], self.rows[7][1], self.rows[7][2], self.rows[7][3]],
        #     [self.rows[8][0], self.rows[8][1], self.rows[8][2], self.rows[8][3]],
        #     [self.rows[9][0], self.rows[9][1], self.rows[9][2], self.rows[9][3]],
        #     [self.rows[10][0], self.rows[10][1], self.rows[10][2], self.rows[10][3]],
        #     [self.rows[11][0], self.rows[11][1], self.rows[11][2], self.rows[11][3]],
        #     [self.rows[12][0], self.rows[12][1], self.rows[12][2], self.rows[12][3]],
        #     [self.rows[13][0], self.rows[13][1], self.rows[13][2], self.rows[13][3]],
        #     [self.rows[14][0], self.rows[14][1], self.rows[14][2], self.rows[14][3]],
        #     [self.rows[15][0], self.rows[15][1], self.rows[15][2], self.rows[15][3]],
        #     [self.rows[16][0], self.rows[16][1], self.rows[16][2], self.rows[16][3]],
        #     [self.rows[17][0], self.rows[17][1], self.rows[17][2], self.rows[17][3]],
        #     [self.rows[18][0], self.rows[18][1], self.rows[18][2], self.rows[18][3]],
        #     [self.rows[19][0], self.rows[19][1], self.rows[19][2], self.rows[19][3]],
        #     [self.rows[20][0], self.rows[20][1], self.rows[20][2], self.rows[20][3]],
        #     [self.rows[21][0], self.rows[21][1], self.rows[21][2], self.rows[21][3]],
        #     [self.rows[22][0], self.rows[22][1], self.rows[22][2], self.rows[22][3]],
        #     [self.rows[23][0], self.rows[23][1], self.rows[23][2], self.rows[23][3]],
        #     [self.rows[24][0], self.rows[24][1], self.rows[24][2], self.rows[24][3]],
        #     [self.rows[25][0], self.rows[25][1], self.rows[25][2], self.rows[25][3]],
        #     [self.rows[26][0], self.rows[26][1], self.rows[26][2], self.rows[26][3]],
        #     [self.rows[27][0], self.rows[27][1], self.rows[27][2], self.rows[27][3]],
        #     [self.rows[28][0], self.rows[28][1], self.rows[28][2], self.rows[28][3]],
        #     [self.rows[29][0], self.rows[29][1], self.rows[29][2], self.rows[29][3]],
        #     [self.rows[30][0], self.rows[30][1], self.rows[30][2], self.rows[30][3]],
        #     [self.rows[31][0], self.rows[31][1], self.rows[31][2], self.rows[31][3]],
        #     [self.rows[32][0], self.rows[32][1], self.rows[32][2], self.rows[32][3]],
        #     [self.rows[33][0], self.rows[33][1], self.rows[33][2], self.rows[33][3]],
        #     [self.rows[34][0], self.rows[34][1], self.rows[34][2], self.rows[34][3]],
        #     [self.rows[35][0], self.rows[35][1], self.rows[35][2], self.rows[35][3]],
        #     [self.rows[36][0], self.rows[36][1], self.rows[36][2], self.rows[36][3]],
        #     [self.rows[37][0], self.rows[37][1], self.rows[37][2], self.rows[37][3]],
        #     [self.rows[38][0], self.rows[38][1], self.rows[38][2], self.rows[38][3]],
        #     [self.rows[39][0], self.rows[39][1], self.rows[39][2], self.rows[39][3]],
        #     [self.rows[40][0], self.rows[40][1], self.rows[40][2], self.rows[40][3]],
        #     [self.rows[41][0], self.rows[41][1], self.rows[41][2], self.rows[41][3]],
        #     [self.rows[42][0], self.rows[42][1], self.rows[42][2], self.rows[42][3]],
        #     [self.rows[43][0], self.rows[43][1], self.rows[43][2], self.rows[43][3]],
        #     [self.rows[44][0], self.rows[44][1], self.rows[44][2], self.rows[44][3]],
        #     [self.rows[45][0], self.rows[45][1], self.rows[45][2], self.rows[45][3]],
        #     [self.rows[46][0], self.rows[46][1], self.rows[46][2], self.rows[46][3]],
        #     [self.rows[47][0], self.rows[47][1], self.rows[47][2], self.rows[47][3]],
        #     [self.rows[48][0], self.rows[48][1], self.rows[48][2], self.rows[48][3]],
        #     [self.rows[49][0], self.rows[49][1], self.rows[49][2], self.rows[49][3]],
        #     [self.rows[50][0], self.rows[50][1], self.rows[50][2], self.rows[50][3]],
        #     [self.rows[51][0], self.rows[51][1], self.rows[51][2], self.rows[51][3]],
        #     [self.rows[52][0], self.rows[52][1], self.rows[52][2], self.rows[52][3]],
        #     [self.rows[53][0], self.rows[53][1], self.rows[53][2], self.rows[53][3]],
        #     [self.rows[54][0], self.rows[54][1], self.rows[54][2], self.rows[54][3]],
        #     [self.rows[55][0], self.rows[55][1], self.rows[55][2], self.rows[55][3]],
        #     [self.rows[56][0], self.rows[56][1], self.rows[56][2], self.rows[56][3]],
        #     [self.rows[57][0], self.rows[57][1], self.rows[57][2], self.rows[57][3]],
        #     [self.rows[58][0], self.rows[58][1], self.rows[58][2], self.rows[58][3]],
        #     [self.rows[59][0], self.rows[59][1], self.rows[59][2], self.rows[59][3]],
        #     [self.rows[60][0], self.rows[60][1], self.rows[60][2], self.rows[60][3]],
        #     [self.rows[61][0], self.rows[61][1], self.rows[61][2], self.rows[61][3]],
        #     [self.rows[62][0], self.rows[62][1], self.rows[62][2], self.rows[62][3]],
        #     [self.rows[63][0], self.rows[63][1], self.rows[63][2], self.rows[63][3]],
        #     [self.rows[64][0], self.rows[64][1], self.rows[64][2], self.rows[64][3]],
        #     [self.rows[65][0], self.rows[65][1], self.rows[65][2], self.rows[65][3]],
        #     [self.rows[66][0], self.rows[66][1], self.rows[66][2], self.rows[66][3]],
        #     [self.rows[67][0], self.rows[67][1], self.rows[67][2], self.rows[67][3]],
        #     [self.rows[68][0], self.rows[68][1], self.rows[68][2], self.rows[68][3]],
        #     [self.rows[69][0], self.rows[69][1], self.rows[69][2], self.rows[69][3]],
        #     [self.rows[70][0], self.rows[70][1], self.rows[70][2], self.rows[70][3]],
        #     [self.rows[71][0], self.rows[71][1], self.rows[71][2], self.rows[71][3]],
        #     [self.rows[72][0], self.rows[72][1], self.rows[72][2], self.rows[72][3]],
        #     [self.rows[73][0], self.rows[73][1], self.rows[73][2], self.rows[73][3]],
        #     [self.rows[74][0], self.rows[74][1], self.rows[74][2], self.rows[74][3]],
        #     [self.rows[75][0], self.rows[75][1], self.rows[75][2], self.rows[75][3]],
        #     [self.rows[76][0], self.rows[76][1], self.rows[76][2], self.rows[76][3]],
        #     [self.rows[77][0], self.rows[77][1], self.rows[77][2], self.rows[77][3]],
        #     [self.rows[78][0], self.rows[78][1], self.rows[78][2], self.rows[78][3]],
        #     [self.rows[79][0], self.rows[79][1], self.rows[79][2], self.rows[79][3]]
        #     ]

        # # header = ['name', 'area', 'country_code2', 'country_code3']
        # with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', 'w', newline='') as f:
        #     writer = csv.writer(f)
        #     #writer.writerow(header)
        #     writer.writerows(data)
        #     #for i in range(0, 80):
        #     #    writer.writerow(rows[i])

        # omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
        #     count=1,
        #     paths=['/World/Card_Position_1'],
        #     new_translations=[1932.8030853521411, 5.399999999999998, -4.7331654313260715e-31],
        #     new_rotation_eulers=[90.0, 0.0, 0.0],
        #     new_rotation_orders=[0, 1, 2],
        #     new_scales=[2.75, 4.75, 0.05],
        #     old_translations=[1852.223442450999, 5.399999999999998, -4.7331654313260715e-31],
        #     old_rotation_eulers=[90.0, 0.0, 0.0],
        #     old_rotation_orders=[0, 1, 2],
        #     old_scales=[2.75, 4.75, 0.05],
        #     usd_context_name='',
        #     time_code=0.0)

    def _on_save_cards(self):
        """Called when the user presses the "Get From Selection" button"""
        print('ON Card Save')
        #for i in range(1, 80):
        #    print("Card Save Input: ", self.Deck_Temp[i])

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

        # Data to be written
        data = [
            [self.rows[0][0], self.rows[0][1], self.rows[0][2], self.rows[0][3]],
            [self.rows[1][0], self.rows[1][1], self.rows[1][2], self.rows[1][3]],
            [self.rows[2][0], self.rows[2][1], self.rows[2][2], self.rows[2][3]],
            [self.rows[3][0], self.rows[3][1], self.rows[3][2], self.rows[3][3]],
            [self.rows[4][0], self.rows[4][1], self.rows[4][2], self.rows[4][3]],
            [self.rows[5][0], self.rows[5][1], self.rows[5][2], self.rows[5][3]],
            [self.rows[6][0], self.rows[6][1], self.rows[6][2], self.rows[6][3]],
            [self.rows[7][0], self.rows[7][1], self.rows[7][2], self.rows[7][3]],
            [self.rows[8][0], self.rows[8][1], self.rows[8][2], self.rows[8][3]],
            [self.rows[9][0], self.rows[9][1], self.rows[9][2], self.rows[9][3]],
            [self.rows[10][0], self.rows[10][1], self.rows[10][2], self.rows[10][3]],
            [self.rows[11][0], self.rows[11][1], self.rows[11][2], self.rows[11][3]],
            [self.rows[12][0], self.rows[12][1], self.rows[12][2], self.rows[12][3]],
            [self.rows[13][0], self.rows[13][1], self.rows[13][2], self.rows[13][3]],
            [self.rows[14][0], self.rows[14][1], self.rows[14][2], self.rows[14][3]],
            [self.rows[15][0], self.rows[15][1], self.rows[15][2], self.rows[15][3]],
            [self.rows[16][0], self.rows[16][1], self.rows[16][2], self.rows[16][3]],
            [self.rows[17][0], self.rows[17][1], self.rows[17][2], self.rows[17][3]],
            [self.rows[18][0], self.rows[18][1], self.rows[18][2], self.rows[18][3]],
            [self.rows[19][0], self.rows[19][1], self.rows[19][2], self.rows[19][3]],
            [self.rows[20][0], self.rows[20][1], self.rows[20][2], self.rows[20][3]],
            [self.rows[21][0], self.rows[21][1], self.rows[21][2], self.rows[21][3]],
            [self.rows[22][0], self.rows[22][1], self.rows[22][2], self.rows[22][3]],
            [self.rows[23][0], self.rows[23][1], self.rows[23][2], self.rows[23][3]],
            [self.rows[24][0], self.rows[24][1], self.rows[24][2], self.rows[24][3]],
            [self.rows[25][0], self.rows[25][1], self.rows[25][2], self.rows[25][3]],
            [self.rows[26][0], self.rows[26][1], self.rows[26][2], self.rows[26][3]],
            [self.rows[27][0], self.rows[27][1], self.rows[27][2], self.rows[27][3]],
            [self.rows[28][0], self.rows[28][1], self.rows[28][2], self.rows[28][3]],
            [self.rows[29][0], self.rows[29][1], self.rows[29][2], self.rows[29][3]],
            [self.rows[30][0], self.rows[30][1], self.rows[30][2], self.rows[30][3]],
            [self.rows[31][0], self.rows[31][1], self.rows[31][2], self.rows[31][3]],
            [self.rows[32][0], self.rows[32][1], self.rows[32][2], self.rows[32][3]],
            [self.rows[33][0], self.rows[33][1], self.rows[33][2], self.rows[33][3]],
            [self.rows[34][0], self.rows[34][1], self.rows[34][2], self.rows[34][3]],
            [self.rows[35][0], self.rows[35][1], self.rows[35][2], self.rows[35][3]],
            [self.rows[36][0], self.rows[36][1], self.rows[36][2], self.rows[36][3]],
            [self.rows[37][0], self.rows[37][1], self.rows[37][2], self.rows[37][3]],
            [self.rows[38][0], self.rows[38][1], self.rows[38][2], self.rows[38][3]],
            [self.rows[39][0], self.rows[39][1], self.rows[39][2], self.rows[39][3]],
            [self.rows[40][0], self.rows[40][1], self.rows[40][2], self.rows[40][3]],
            [self.rows[41][0], self.rows[41][1], self.rows[41][2], self.rows[41][3]],
            [self.rows[42][0], self.rows[42][1], self.rows[42][2], self.rows[42][3]],
            [self.rows[43][0], self.rows[43][1], self.rows[43][2], self.rows[43][3]],
            [self.rows[44][0], self.rows[44][1], self.rows[44][2], self.rows[44][3]],
            [self.rows[45][0], self.rows[45][1], self.rows[45][2], self.rows[45][3]],
            [self.rows[46][0], self.rows[46][1], self.rows[46][2], self.rows[46][3]],
            [self.rows[47][0], self.rows[47][1], self.rows[47][2], self.rows[47][3]],
            [self.rows[48][0], self.rows[48][1], self.rows[48][2], self.rows[48][3]],
            [self.rows[49][0], self.rows[49][1], self.rows[49][2], self.rows[49][3]],
            [self.rows[50][0], self.rows[50][1], self.rows[50][2], self.rows[50][3]],
            [self.rows[51][0], self.rows[51][1], self.rows[51][2], self.rows[51][3]],
            [self.rows[52][0], self.rows[52][1], self.rows[52][2], self.rows[52][3]],
            [self.rows[53][0], self.rows[53][1], self.rows[53][2], self.rows[53][3]],
            [self.rows[54][0], self.rows[54][1], self.rows[54][2], self.rows[54][3]],
            [self.rows[55][0], self.rows[55][1], self.rows[55][2], self.rows[55][3]],
            [self.rows[56][0], self.rows[56][1], self.rows[56][2], self.rows[56][3]],
            [self.rows[57][0], self.rows[57][1], self.rows[57][2], self.rows[57][3]],
            [self.rows[58][0], self.rows[58][1], self.rows[58][2], self.rows[58][3]],
            [self.rows[59][0], self.rows[59][1], self.rows[59][2], self.rows[59][3]],
            [self.rows[60][0], self.rows[60][1], self.rows[60][2], self.rows[60][3]],
            [self.rows[61][0], self.rows[61][1], self.rows[61][2], self.rows[61][3]],
            [self.rows[62][0], self.rows[62][1], self.rows[62][2], self.rows[62][3]],
            [self.rows[63][0], self.rows[63][1], self.rows[63][2], self.rows[63][3]],
            [self.rows[64][0], self.rows[64][1], self.rows[64][2], self.rows[64][3]],
            [self.rows[65][0], self.rows[65][1], self.rows[65][2], self.rows[65][3]],
            [self.rows[66][0], self.rows[66][1], self.rows[66][2], self.rows[66][3]],
            [self.rows[67][0], self.rows[67][1], self.rows[67][2], self.rows[67][3]],
            [self.rows[68][0], self.rows[68][1], self.rows[68][2], self.rows[68][3]],
            [self.rows[69][0], self.rows[69][1], self.rows[69][2], self.rows[69][3]],
            [self.rows[70][0], self.rows[70][1], self.rows[70][2], self.rows[70][3]],
            [self.rows[71][0], self.rows[71][1], self.rows[71][2], self.rows[71][3]],
            [self.rows[72][0], self.rows[72][1], self.rows[72][2], self.rows[72][3]],
            [self.rows[73][0], self.rows[73][1], self.rows[73][2], self.rows[73][3]],
            [self.rows[74][0], self.rows[74][1], self.rows[74][2], self.rows[74][3]],
            [self.rows[75][0], self.rows[75][1], self.rows[75][2], self.rows[75][3]],
            [self.rows[76][0], self.rows[76][1], self.rows[76][2], self.rows[76][3]],
            [self.rows[77][0], self.rows[77][1], self.rows[77][2], self.rows[77][3]],
            [self.rows[78][0], self.rows[78][1], self.rows[78][2], self.rows[78][3]],
            [self.rows[79][0], self.rows[79][1], self.rows[79][2], self.rows[79][3]]
            ]

        # header = ['name', 'area', 'country_code2', 'country_code3']
        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            #writer.writerow(header)
            writer.writerows(data)
            #for i in range(0, 80):
            #    writer.writerow(rows[i])

        #self._on_three_card()

    def _on_three_card(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Three Card Layout Selected')

        # self._apply_transforms(
        #     ['/World/Card_Position_1'],
        #     [{'translation': [200.0, 2.0, 0.0],
        #     'rotation_euler': [90.0, 0.0, 0.0],
        #     'scale': [2.75, 4.75, 0.05]}],
        #     time_code=0.0)

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

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_1'],
            new_translations=[540.0, 0.0, 800.0],
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
            new_translations=[0.0, 0.0, 800.0],
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
            new_translations=[-540.0, 0.0, 800.0],
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
            new_translations=[1050.0, -500.0, 1000.0],
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
            new_translations=[700.0, -500.0, 1000.0],
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
            new_translations=[-350.0, -500.0, 1000.0],
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
            new_translations=[-700.0, -500.0, 1000.0],
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
            new_translations=[1050.0, -500.0, 500.0],
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

    def _on_collider(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Collider Layout Selected')

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

    def _on_chakra(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Chakra Layout Selected')

        self._on_reset()

        self.count = 0

        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
            csvFile = csv.reader(file)
            self.rows = list(csvFile)
            # print(self.rows[5][3])
            for i in range(80):  # for i in range(1, 14):  # 1..13
                if(self.count == 0): self.Deck_Temp[self.count] = 0
                else:  self.Deck_Position[self.count] = int(self.rows[self.count][3])
                # print(self.rows[self.count][3])
                # print(self.Deck_Position[self.count])
                # print(self.count)
                self.count += 1

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_1'],
            new_translations=[335.0, 0.0, 1430.0],
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
            strength='strongerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_2'],
            new_translations=[670.0, 0.0, 1430.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_2')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[2]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='strongerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_3'],
            new_translations=[-335.0, 0.0, 1430.0],
            new_rotation_eulers=[90.0, 0.0, 0.0],
            new_rotation_orders=[0, 1, 2],
            new_scales=[2.75, 4.75, 0.05])

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_3')],
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[3]][0]),
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
            material_path=Sdf.Path('/World/Looks/' + self.rows[self.Deck_Temp[4]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
            count=1,
            paths=['/World/Card_Position_5'],
            new_translations=[1005.0, 0.0, 1430.0],
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
            new_translations=[-670.0, 0.0, 1430.0],
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
            new_translations=[-1005.0, 0.0, 1430.0],
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
            new_translations=[335.0, 0.0, 840.0],
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
            new_translations=[670.0, 0.0, 840.0],
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
            new_translations=[-670.0, 0.0, 840.0],
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
            new_translations=[0.0, 0.0, 840.0],
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
            new_translations=[1005.0, 0.0, 840.0],
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
            new_translations=[-335.0, 0.0, 840.0],
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
            new_translations=[-1005.0, 0.0, 840.0],
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
            new_translations=[335.0, 0.0, 260.0],
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
            new_translations=[670.0, 0.0, 260.0],
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
            new_translations=[-335.0, 0.0, 260.0],
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
            new_translations=[0.0, 0.0, 260.0],
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
            new_translations=[1005.0, 0.0, 260.0],
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
            new_translations=[-670.0, 0.0, 260.0],
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
            new_translations=[-1005.0, 0.0, 260.0],
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


    def _on_reset(self):
        """Called when the user presses the "Get From Selection" button"""
        print('On Reset Selected')

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
