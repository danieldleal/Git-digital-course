# -*- coding: utf-8 -*-
__title__ = "Room finishes"
__doc__ = """Version = 1.0
Date    = 25.01.2023
_____________________________________________________________________
Description:
Script to auto-name determine finishes in Room_Schedule
This is a script was based on EF template, provided by Erik Frits on GitHub.
_____________________________________________________________________
How-to:
-> Click on the button
-> Change Settings(optional)
-> Make a change
_____________________________________________________________________
Updates:
- [25.01.2023] - 1.0 (Day 1)
- [04.03.2023] - 1.1
- [24.05.2023] - 1.2 
_____________________________________________________________________
To-Do:
- Everything
_____________________________________________________________________
Pseudo-code:
1. Open Revit 2023 -> In Add-In Tab/RevitLookup/SnippetSelection
2. Select a Room -> Snoop Selection -> Parameters (Choose one 'finish') -> Definition (Internal Definition)
3. On the InternalDefinition window see which BuiltInParameter (if is INVALID, search which Parameter will be)
    PARAMETERS ON REVIT:
    3.1. BuiltIn Parameter
    3.2. Project Parameter
    3.3. Shared Parameter
    3.4. Global Parameter
    3.5. Family Parameter
4. 'Room' it's defined as a BultIn Parameter so we gonna use BultInParameter Method
5. For every parameter in Room we have to choose a method. These are the parameters we want to set:
Research in ApiDocs I've found: 
    -> CONSTRAINTS:
        1. - UPPER LIMIT  - ROOM_UPPER_LEVEL
        2. - LIMIT OFFSET - ROOM_LIMIT_OFFSET
        3. - BASE OFFSET  - ROOM_BASE_OFFSET
    -> IDENTITY DATA:
        1.- NUMBER - ROOM_NUMBER
        2.- NAME - ROOM_NAME
        3.- DEPARTMENT - ROOM_DEPARTMENT
        4.- BASE FINISH - ROOM_FINISH_BASE
        5.- CEILING FINISH - ROOM_FINISH_CEILING
        6.- WALL FINISH - ROOM_FINISH_WALL
        7.- FLOOR FINISH - ROOM_FINISH_FLOOR
6. Its necessary to set every parameter based on the rooms created;
7. 

_____________________________________________________________________
Author: Daniel Leal (updated and adapted from a Erik Frits script_Parameters)"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================

from Autodesk.Revit.DB import *
from pyrevit import *


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc     = __revit__.ActiveUIDocument.Document
uidoc   = __revit__.ActiveUIDocument
app     = __revit__.Application

# ╔═╗╦  ╔═╗╔═╗╔═╗
# ║  ║  ╠═╣╚═╗╚═╗
# ╚═╝╩═╝╩ ╩╚═╝╚═╝ CLASS
#====================================================================


class NameRooms():
    def __init__(self):
        self.start(title=__title__, version=__doc__)
        

    def get_selected_elements(self):
        """Get Selected Views or let user select Views from a list."""
        selected_elements = get_selected_elements(uidoc)
        selected_rooms = [el for el in selected_elements if type(el) == Room]
        if not selected_rooms:
            forms.alert('No Rooms were selected, \nPlease Try Again', exitscript=True, title=__title__)

        return selected_rooms
    
    def naming_element(self):
        """Function to name selected Views."""
        with ef_Transaction(doc,__title__):
            for room in self.selected_elements:
                with try_except():
                    current_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
                    new_name     = self.prefix + current_name.replace(self.find,self.replace) + self.suffix
                    if new_name and  new_name != current_name:
                        room.Name = new_name

# ╔═╗╔═╗╔╦╗  ╔═╗╔═╗╦═╗╔═╗╔╦╗╔═╗╔╦╗╔═╗╦═╗  ╔╗ ╦ ╦  ╔╗╔╔═╗╔╦╗╔═╗
# ║ ╦║╣  ║   ╠═╝╠═╣╠╦╝╠═╣║║║║╣  ║ ║╣ ╠╦╝  ╠╩╗╚╦╝  ║║║╠═╣║║║║╣
# ╚═╝╚═╝ ╩   ╩  ╩ ╩╩╚═╩ ╩╩ ╩╚═╝ ╩ ╚═╝╩╚═  ╚═╝ ╩   ╝╚╝╩ ╩╩ ╩╚═╝ GET PARAMETER BY NAME
#====================================================================================================
# print('*** Getting Shared Parameters: ***')

# GET PROJECT/SHARED PARAMETER
# sp_text = wall.LookupParameter('sp_text')
# print(sp_text.AsString())

# sp_mat_id = wall.LookupParameter('sp_material').AsElementId()
# sp_mat = doc.GetElement(sp_mat_id)
# print(sp_mat)
# print(sp_mat.Name)

# sp_text = wall.LookupParameter('sp_bool')
# print(sp_text.AsInteger())

# ╔═╗╔═╗╔╦╗  ╔╦╗╦ ╦╔═╗╔═╗  ╔═╗╔═╗╦═╗╔═╗╔╦╗╔═╗╔╦╗╔═╗╦═╗╔═╗
# ║ ╦║╣  ║    ║ ╚╦╝╠═╝║╣   ╠═╝╠═╣╠╦╝╠═╣║║║║╣  ║ ║╣ ╠╦╝╚═╗
# ╚═╝╚═╝ ╩    ╩  ╩ ╩  ╚═╝  ╩  ╩ ╩╩╚═╩ ╩╩ ╩╚═╝ ╩ ╚═╝╩╚═╚═╝ GET TYPE PARAMETERS
#====================================================================================================

room_number = room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
rooms = [room_number, room_name, room_department, room_fin_b, room_fin_c, room_fin_w, room_fin_f]


# ╔═╗╔═╗╔╦╗  ╔═╗╔═╗╦═╗╔═╗╔╦╗╔═╗╔╦╗╔═╗╦═╗  ╦  ╦╔═╗╦  ╦ ╦╔═╗
# ╚═╗║╣  ║   ╠═╝╠═╣╠╦╝╠═╣║║║║╣  ║ ║╣ ╠╦╝  ╚╗╔╝╠═╣║  ║ ║║╣
# ╚═╝╚═╝ ╩   ╩  ╩ ╩╩╚═╩ ╩╩ ╩╚═╝ ╩ ╚═╝╩╚═   ╚╝ ╩ ╩╩═╝╚═╝╚═╝ SET PARAMETER VALUE
#====================================================================================================


t = Transaction(doc, __title__)
t.Start()

BuiltInParameter.SPACE_ASSOC_ROOM_NAME = Bedroom_Example
room_number = 11
room_name = print()
ex_phrase = print('%s %s has been set to %s')
for room in rooms:
    n_room_number     = set(str(room_number))
    n_room_name       = set(str(room_name))
    n_room_department = set(str(room_department))
    n_room_finish_b   = set(str(room_finish_b))
    n_room_finish_c   = set(str(room_finish_c))
    n_room_finish_w   = set(str(room_finish_w))
    n_room_finish_f   = set(str(room_finish_f))

t.Commit()

print('Your new room configurations has been setup. There is your modifications:')
print(ex_phrase%(name_room, number, n_room_number))
print(ex_phrase%(name_room, name, n_room_name))
print(ex_phrase%(name_room, department, n_room_department))
print(ex_phrase%(name_room, basefinish, n_room_finish_b))
print(ex_phrase%(name_room, ceilingfinish, n_room_finish_c))
print(ex_phrase%(name_room, wallfinish, n_room_finish_w))
print(ex_phrase%(name_room, floorfinish, n_room_finish_f))

# GET PARAMETERS
# wall_comments = wall.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
# sp_area       = wall.LookupParameter('sp_area')

# SET PARAMETERS
# t = Transaction(doc, __title__)
# t.Start()

# # wall_comments.Set('That was terrible joke. Comment better jokes under my video.')
# # print(wall_comments.AsString())

# sp_area.Set(555.55)
# sp_bool.Set(1)
# sp_float.Set(25.5)
# sp_int.Set(100)
# sp_length.Set(99.99)
# new_mat_id = ElementId(414)
# sp_mat.Set(new_mat_id)
# sp_text.Set(str(1000))
# print('Setting parameters is complete.')
# t.Commit()

# ╔═╗╦  ╔═╗╔╗ ╔═╗╦    ╔═╗╔═╗╦═╗╔═╗╔╦╗╔═╗╔╦╗╔═╗╦═╗╔═╗
# ║ ╦║  ║ ║╠╩╗╠═╣║    ╠═╝╠═╣╠╦╝╠═╣║║║║╣  ║ ║╣ ╠╦╝╚═╗
# ╚═╝╩═╝╚═╝╚═╝╩ ╩╩═╝  ╩  ╩ ╩╩╚═╩ ╩╩ ╩╚═╝ ╩ ╚═╝╩╚═╚═╝ GLOBAL PARAMETERS
#====================================================================================================
# print('*** GLOBAL PARAMETERS ***')

# GET ALL GLOBAL PARAMETERS
# all_global_parameter_ids = GlobalParametersManager.GetAllGlobalParameters(doc)
#
# t = Transaction(doc,'Changing Global Parameters')
# t.Start()

# PRINT GLOBAL PARAMETERS DATA
# for p_id in all_global_parameter_ids:
    # p = doc.GetElement(p_id)
    # print('Name:          {}'.format(p.Name))
    # print('GetDefinition: {}'.format(p.GetDefinition()))
    # print('GetFormula:    {}'.format(p.GetFormula()))
    # print('GetValue:      {}'.format(p.GetValue().Value))
    # print('-'*50)

    # CHANGE GLOBAL PARAMETER VALUE OR FORMULA
    # new_value = StringParameterValue('New Value')
    # p.SetValue(new_value)
    # p.SetFormula('"New Formula"')

# t.Commit()

# ╔═╗╦ ╦╔═╗╔╦╗╔═╗╔╦╗  ╔╦╗╔═╗╔═╗╦
# ║  ║ ║╚═╗ ║ ║ ║║║║   ║ ║ ║║ ║║
# ╚═╝╚═╝╚═╝ ╩ ╚═╝╩ ╩   ╩ ╚═╝╚═╝╩═╝
#====================================================================================================

# t = Transaction(doc,'Writing ElementIds to Mark parameter of Walls.')
# t.Start()

# SET WALL ELEMENT-ID TO MARK
# all_walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

# for wall in all_walls:
    # wall_mark = wall.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
    # wall_mark.Set(str(wall.Id))
    # print(wall.Id)
# t.Commit()

# print('The script is complete. Comment ⌨ emoji in the comments if you following along.')