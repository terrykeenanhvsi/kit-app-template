__all__ = ["ScatterWindow"]

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
                self.slider1 = ui.UIntSlider(min=1, max=100, step=1)
                self.slider1.model.set_value(50)  # Set initial value
                self.slider1.model.add_value_changed_fn(lambda m: self.on_slider_cut1(self.slider1))

                self.slider2 = ui.UIntSlider(min=1, max=100, step=1)
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
                                       # Button that puts the selection to the string field
                    ui.Button(
                        " 3 ",
                        width=0,
                        height=0,
                        style={"margin": 0},
                         clicked_fn=self._on_three_card,
                        tooltip="Three Card Layout",
                    )
                    ui.Button(
                        " C ",
                        width=0,
                        height=0,
                        style={"margin": 0},
                         clicked_fn=self._on_collider,
                        tooltip="Collider Layout",
                    )
                    ui.Button(
                        " 7 ",
                        width=0,
                        height=0,
                        style={"margin": 0},
                         clicked_fn=self._on_chakra,
                        tooltip="Chakra Layout",
                    )

    def _on_cut_deck(self):
        """Called when the user presses the "Get From Selection" button"""
        self.Stack1Button.visible = True
        self.Stack2Button.visible = True
        self.Stack3Button.visible = True
        pass

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
        print('Slider1 Cut Selected',self.Slider_Value1)


    def on_slider_cut2(self, slider2):
        """Called when the user presses the "Get From Selection" button"""

        self.Slider_Value2 = self.slider2.model.get_value_as_int()
        print('Slider2 Cut Selected', self.Slider_Value2)


    def _on_stack1(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Stack 1 Layout Selected')
        self.Stack1Button.visible = False
        #self._source_prim_model.as_string = ", ".join(get_selection())
        #pass

    def _on_stack2(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Stack 2 Layout Selected')
        self.Stack2Button.visible = False
        #self._source_prim_model.as_string = ", ".join(get_selection())
        #pass

    def _on_stack3(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Stack 3 Layout Selected')
        self.Stack3Button.visible = False
        #self._source_prim_model.as_string = ", ".join(get_selection())
        #pass

    def _on_three_card(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Three Card Layout Selected')
        #self._source_prim_model.as_string = ", ".join(get_selection())
        #pass

    def _on_three_card(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Three Card Layout Selected')
        #self._source_prim_model.as_string = ", ".join(get_selection())
        #pass

    def _on_collider(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Collider Layout Selected')
        #self._source_prim_model.as_string = ", ".join(get_selection())
        #pass

    def _on_chakra(self):
        """Called when the user presses the "Get From Selection" button"""
        print('Chakra Layout Selected')
        #self._source_prim_model.as_string = ", ".join(get_selection())
        #pass

    def _on_scatter(self):
        """Called when the user presses the "Scatter" button"""
        # prim_names = [i.strip() for i in self._source_prim_model.as_string.split(",")]
        # if not prim_names:
        #     prim_names = get_selection()

        # if not prim_names:
        #     pass

        # transforms = scatter(
        #     count=[m.as_int for m in self._scatter_count_models],
        #     distance=[m.as_float for m in self._scatter_distance_models],
        #     randomization=[m.as_float for m in self._scatter_random_models],
        #     id_count=len(prim_names),
        #     seed=self._scatter_seed_model.as_int,
        # )

        # duplicate_prims(
        #     transforms=transforms,
        #     prim_names=prim_names,
        #     target_path=self._scatter_prim_model.as_string,
        #     mode=self._scatter_type_model.get_current_item().as_string
        # )

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

        # Generate 5 unique random integers between 0 and 100
        # self.Deck_Position = np.zeros(78)
        # self.Deck_Cut_Left = np.zeros(78)
        # self.Deck_Cut_Middle = np.zeros(78)
        # self.Deck_Cut_Right = np.zeros(78)
        # self.Deck_Temp = np.zeros(78)

        self.count = 0

        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
            csvFile = csv.reader(file)
            rows = list(csvFile)
            print(rows[5][3])
            for i in range(80):  # for i in range(1, 14):  # 1..13
                if(self.count == 0): self.Deck_Position[self.count] = 0
                else:  self.Deck_Position[self.count] = int(rows[self.count][3])
                # print(rows[self.count][3])
                print(self.Deck_Position[self.count])
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

        # for i in range(0, 80):
        #     print(self.Deck_Temp[i])

        random_numbers = random.sample(range(1, 79), 78)
        #print(random_numbers) # random_numbers[1]][0] rows[self.Deck_Temp[1]][0]),

        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
            csvFile = csv.reader(file)
            rows = list(csvFile)
            print(rows[5][0])
            #for lines in csvFile:
            #   print(lines)

        for i in range(0, 80):
                rows[i][3] = self.Deck_Temp[i]

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_1')],
            material_path=Sdf.Path('/World/Looks/' + rows[self.Deck_Temp[1]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_2')],
            material_path=Sdf.Path('/World/Looks/' + rows[self.Deck_Temp[2]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_3')],
            material_path=Sdf.Path('/World/Looks/' + rows[self.Deck_Temp[3]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_4')],
            material_path=Sdf.Path('/World/Looks/' + rows[self.Deck_Temp[4]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_5')],
            material_path=Sdf.Path('/World/Looks/' + rows[self.Deck_Temp[5]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_6')],
            material_path=Sdf.Path('/World/Looks/' + rows[self.Deck_Temp[6]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_7')],
            material_path=Sdf.Path('/World/Looks/' + rows[self.Deck_Temp[7]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_8')],
            material_path=Sdf.Path('/World/Looks/' + rows[self.Deck_Temp[8]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_9')],
            material_path=Sdf.Path('/World/Looks/' + rows[self.Deck_Temp[9]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_10')],
            material_path=Sdf.Path('/World/Looks/' + rows[self.Deck_Temp[10]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_11')],
            material_path=Sdf.Path('/World/Looks/' + rows[self.Deck_Temp[11]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_12')],
            material_path=Sdf.Path('/World/Looks/' + rows[self.Deck_Temp[12]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_13')],
            material_path=Sdf.Path('/World/Looks/' + rows[self.Deck_Temp[13]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

                    # Data to be written
        data = [
            [rows[0][0], rows[0][1], rows[0][2], rows[0][3]],
            [rows[1][0], rows[1][1], rows[1][2], rows[1][3]],
            [rows[2][0], rows[2][1], rows[2][2], rows[2][3]],
            [rows[3][0], rows[3][1], rows[3][2], rows[3][3]],
            [rows[4][0], rows[4][1], rows[4][2], rows[4][3]],
            [rows[5][0], rows[5][1], rows[5][2], rows[5][3]],
            [rows[6][0], rows[6][1], rows[6][2], rows[6][3]],
            [rows[7][0], rows[7][1], rows[7][2], rows[7][3]],
            [rows[8][0], rows[8][1], rows[8][2], rows[8][3]],
            [rows[9][0], rows[9][1], rows[9][2], rows[9][3]],
            [rows[10][0], rows[10][1], rows[10][2], rows[10][3]],
            [rows[11][0], rows[11][1], rows[11][2], rows[11][3]],
            [rows[12][0], rows[12][1], rows[12][2], rows[12][3]],
            [rows[13][0], rows[13][1], rows[13][2], rows[13][3]],
            [rows[14][0], rows[14][1], rows[14][2], rows[14][3]],
            [rows[15][0], rows[15][1], rows[15][2], rows[15][3]],
            [rows[16][0], rows[16][1], rows[16][2], rows[16][3]],
            [rows[17][0], rows[17][1], rows[17][2], rows[17][3]],
            [rows[18][0], rows[18][1], rows[18][2], rows[18][3]],
            [rows[19][0], rows[19][1], rows[19][2], rows[19][3]],
            [rows[20][0], rows[20][1], rows[20][2], rows[20][3]],
            [rows[21][0], rows[21][1], rows[21][2], rows[21][3]],
            [rows[22][0], rows[22][1], rows[22][2], rows[22][3]],
            [rows[23][0], rows[23][1], rows[23][2], rows[23][3]],
            [rows[24][0], rows[24][1], rows[24][2], rows[24][3]],
            [rows[25][0], rows[25][1], rows[25][2], rows[25][3]],
            [rows[26][0], rows[26][1], rows[26][2], rows[26][3]],
            [rows[27][0], rows[27][1], rows[27][2], rows[27][3]],
            [rows[28][0], rows[28][1], rows[28][2], rows[28][3]],
            [rows[29][0], rows[29][1], rows[29][2], rows[29][3]],
            [rows[30][0], rows[30][1], rows[30][2], rows[30][3]],
            [rows[31][0], rows[31][1], rows[31][2], rows[31][3]],
            [rows[32][0], rows[32][1], rows[32][2], rows[32][3]],
            [rows[33][0], rows[33][1], rows[33][2], rows[33][3]],
            [rows[34][0], rows[34][1], rows[34][2], rows[34][3]],
            [rows[35][0], rows[35][1], rows[35][2], rows[35][3]],
            [rows[36][0], rows[36][1], rows[36][2], rows[36][3]],
            [rows[37][0], rows[37][1], rows[37][2], rows[37][3]],
            [rows[38][0], rows[38][1], rows[38][2], rows[38][3]],
            [rows[39][0], rows[39][1], rows[39][2], rows[39][3]],
            [rows[40][0], rows[40][1], rows[40][2], rows[40][3]],
            [rows[41][0], rows[41][1], rows[41][2], rows[41][3]],
            [rows[42][0], rows[42][1], rows[42][2], rows[42][3]],
            [rows[43][0], rows[43][1], rows[43][2], rows[43][3]],
            [rows[44][0], rows[44][1], rows[44][2], rows[44][3]],
            [rows[45][0], rows[45][1], rows[45][2], rows[45][3]],
            [rows[46][0], rows[46][1], rows[46][2], rows[46][3]],
            [rows[47][0], rows[47][1], rows[47][2], rows[47][3]],
            [rows[48][0], rows[48][1], rows[48][2], rows[48][3]],
            [rows[49][0], rows[49][1], rows[49][2], rows[49][3]],
            [rows[50][0], rows[50][1], rows[50][2], rows[50][3]],
            [rows[51][0], rows[51][1], rows[51][2], rows[51][3]],
            [rows[52][0], rows[52][1], rows[52][2], rows[52][3]],
            [rows[53][0], rows[53][1], rows[53][2], rows[53][3]],
            [rows[54][0], rows[54][1], rows[54][2], rows[54][3]],
            [rows[55][0], rows[55][1], rows[55][2], rows[55][3]],
            [rows[56][0], rows[56][1], rows[56][2], rows[56][3]],
            [rows[57][0], rows[57][1], rows[57][2], rows[57][3]],
            [rows[58][0], rows[58][1], rows[58][2], rows[58][3]],
            [rows[59][0], rows[59][1], rows[59][2], rows[59][3]],
            [rows[60][0], rows[60][1], rows[60][2], rows[60][3]],
            [rows[61][0], rows[61][1], rows[61][2], rows[61][3]],
            [rows[62][0], rows[62][1], rows[62][2], rows[62][3]],
            [rows[63][0], rows[63][1], rows[63][2], rows[63][3]],
            [rows[64][0], rows[64][1], rows[64][2], rows[64][3]],
            [rows[65][0], rows[65][1], rows[65][2], rows[65][3]],
            [rows[66][0], rows[66][1], rows[66][2], rows[66][3]],
            [rows[67][0], rows[67][1], rows[67][2], rows[67][3]],
            [rows[68][0], rows[68][1], rows[68][2], rows[68][3]],
            [rows[69][0], rows[69][1], rows[69][2], rows[69][3]],
            [rows[70][0], rows[70][1], rows[70][2], rows[70][3]],
            [rows[71][0], rows[71][1], rows[71][2], rows[71][3]],
            [rows[72][0], rows[72][1], rows[72][2], rows[72][3]],
            [rows[73][0], rows[73][1], rows[73][2], rows[73][3]],
            [rows[74][0], rows[74][1], rows[74][2], rows[74][3]],
            [rows[75][0], rows[75][1], rows[75][2], rows[75][3]],
            [rows[76][0], rows[76][1], rows[76][2], rows[76][3]],
            [rows[77][0], rows[77][1], rows[77][2], rows[77][3]],
            [rows[78][0], rows[78][1], rows[78][2], rows[78][3]],
            [rows[79][0], rows[79][1], rows[79][2], rows[79][3]]
            ]

        # header = ['name', 'area', 'country_code2', 'country_code3']
        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            #writer.writerow(header)
            writer.writerows(data)
            #for i in range(0, 80):
            #    writer.writerow(rows[i])
