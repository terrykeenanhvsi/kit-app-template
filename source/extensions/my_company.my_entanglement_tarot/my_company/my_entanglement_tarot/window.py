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

        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
            csvFile = csv.reader(file)
            rows = list(csvFile)
            print(rows[5])
            for lines in csvFile:
                print(lines)

        # Define the dtype
        dtype = [('name', 'U10'), ('age', 'i4'), ('height', 'f4')]

        # Define the data
        data = [('Alice', 30, 5.6), ('Bob', 25, 5.8), ('Charlie', 35, 5.9)]

        # Create the structured array
        structured_array = np.array(data, dtype=dtype)

        print("Structured Array:\n", structured_array)

        # Data to be written
        data = [
            ['Name', 'Branch', 'Year', 'CGPA'],
            ['Nikhil', 'COE', 2, 9.0],
            ['Sanchit', 'COE', 2, 9.1],
            ['Aditya', 'IT', 2, 9.3],
            ['Sagar', 'SE', 1, 9.5],
            ['Prateek', 'MCE', 3, 7.8],
            ['Sahil', 'EP', 2, 9.1]
            ]

        # header = ['name', 'area', 'country_code2', 'country_code3']
        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data2.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            #writer.writerow(header)
            writer.writerows(data)

        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
            csvFile = csv.DictReader(file)
            for lines in csvFile:
                print(lines)



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
                self._build_source()
                self._build_scatter()
                self._build_axis(0, "X Axis")
                self._build_axis(1, "Y Axis")
                self._build_axis(2, "Z Axis")

                # The Go button
                ui.Button("Scatter", clicked_fn=self._on_scatter)

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
        random_numbers = random.sample(range(1, 79), 78)
        print(random_numbers)

        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
            csvFile = csv.reader(file)
            rows = list(csvFile)
            print(rows[5][0])
            #for lines in csvFile:
            #   print(lines)

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_1')],
            material_path=Sdf.Path('/World/Looks/' + rows[random_numbers[1]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_2')],
            material_path=Sdf.Path('/World/Looks/' + rows[random_numbers[2]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_3')],
            material_path=Sdf.Path('/World/Looks/' + rows[random_numbers[3]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_4')],
            material_path=Sdf.Path('/World/Looks/' + rows[random_numbers[4]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_5')],
            material_path=Sdf.Path('/World/Looks/' + rows[random_numbers[5]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_6')],
            material_path=Sdf.Path('/World/Looks/' + rows[random_numbers[6]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_7')],
            material_path=Sdf.Path('/World/Looks/' + rows[random_numbers[7]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_8')],
            material_path=Sdf.Path('/World/Looks/' + rows[random_numbers[8]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_9')],
            material_path=Sdf.Path('/World/Looks/' + rows[random_numbers[9]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_10')],
            material_path=Sdf.Path('/World/Looks/' + rows[random_numbers[10]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_11')],
            material_path=Sdf.Path('/World/Looks/' + rows[random_numbers[11]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_12')],
            material_path=Sdf.Path('/World/Looks/' + rows[random_numbers[12]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')

        omni.kit.commands.execute('BindMaterialCommand',
            prim_path=[Sdf.Path('/World/Card_Position_13')],
            material_path=Sdf.Path('/World/Looks/' + rows[random_numbers[13]][0]),
            # material_path=Sdf.Path('/World/Looks/_1910_Chariot_7'),
            strength='weakerThanDescendants')
