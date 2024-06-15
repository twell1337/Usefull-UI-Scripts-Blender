#outliner.hide

bl_info = {
    "name": "Hide/Unhide Objects",
    "author": "Valentin Tselishchev",
    "version": (1, 0, 0),
    "blender": (2, 93, 5),
    "location": "",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "category": "Outliner",
}

import bpy
from bpy.types import Operator, Collection, Object
from bpy.utils import register_class, unregister_class

def get_all_children(col):
    yield col
    for child in col.children:
        yield from get_all_children(child)

class Hide_Selected(Operator):
    hide_param = True
    bl_idname = 'outliner.hide_selected'
    bl_label = 'Hide selected'
    bl_options = {'REGISTER', 'UNDO'}
    
    def hide_set_coll(self, layer_collection, item, hide_param):
        for layer_col in reversed(list(get_all_children(layer_collection))):
            if layer_col.name == item.name:
                layer_col.hide_viewport = hide_param
                break
    
    def execute(self, context):
        if bpy.context.selected_ids:
            for item in bpy.context.selected_ids:
                if type(item) is Collection:
                    layer_collection = context.view_layer.layer_collection
                    self.hide_set_coll(layer_collection, item, self.hide_param)
                elif type(item) is Object:
                    item.hide_set(self.hide_param)
            return {"FINISHED"}
        else:
            return {"CANCELLED"}
        
class Unhide_Selected(Operator):
    hide_param = False
    bl_idname = 'outliner.unhide_selected'
    bl_label = 'Unhide selected'
    bl_options = {'REGISTER', 'UNDO'}
    
    def hide_set_coll(self, layer_collection, item, hide_param):
        for layer_col in reversed(list(get_all_children(layer_collection))):
            if layer_col.name == item.name:
                layer_col.hide_viewport = hide_param
                break
    
    def execute(self, context):
        if bpy.context.selected_ids:
            for item in bpy.context.selected_ids:
                if type(item) is Collection:
                    layer_collection = context.view_layer.layer_collection
                    self.hide_set_coll(layer_collection, item, self.hide_param)
                elif type(item) is Object:
                    item.hide_set(self.hide_param)
            return {"FINISHED"}
        else:
            return {"CANCELLED"}

classes = [
    Hide_Selected,
    Unhide_Selected
]

def register():
    for cls in classes:
        register_class(cls)
    
    
def unregister():
    for cls in classes:
        unregister_class(cls)
    
if __name__ == "__main__":
    register()