bl_info = {
    "name": "Drag HDRI",
    "author": "Valentin Tselishchev",
    "version": (1, 0, 0),
    "blender": (2, 93, 5),
    "location": "View 3D",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "category": "3D View",
}

import bpy
from bpy.types import Operator, PropertyGroup
from bpy.utils import register_class, unregister_class
from bpy.props import FloatProperty, PointerProperty
from math import degrees, pi



class hdri_props(PropertyGroup):
    hdri_rot : FloatProperty()
    
class hdri_rotation(Operator):
    bl_idname = "hdri.rotation"
    bl_label = 'HDRI rotation'

    def invoke(self, context, event):
        self.init_cox_2d = event.mouse_region_x
        self.hdri = context.scene.hdri
        self.start_hdri = self.hdri.hdri_rot
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
    def swap(self, context, event, x, l, u):
        if x > u:
            self.start_hdri = self.hdri.hdri_rot
            self.init_cox_2d = event.mouse_region_x
            return l 
        elif x < l:
            self.start_hdri = self.hdri.hdri_rot
            self.init_cox_2d = event.mouse_region_x
            return u
        else:
            return x

    def modal(self, context, event):
        if event.type == "MOUSEMOVE":
            prev_rot = self.hdri.hdri_rot
            
            pos_value = (event.mouse_region_x - self.init_cox_2d)/200 + self.start_hdri
            self.hdri.hdri_rot = self.swap(context, event, pos_value, -pi, pi)

            context.space_data.shading.studiolight_rotate_z = self.hdri.hdri_rot
            context.area.header_text_set(f"HDRI rotation: {degrees(context.space_data.shading.studiolight_rotate_z):.2f}")
            context.area.tag_redraw()
        elif event.value == "RELEASE" and event.type != "LEFT_ALT" and event.type != "RIGHT_ALT":
            context.area.header_text_set(None)
            return {'FINISHED'}
        
        return {'RUNNING_MODAL'}
    
classes = [
    hdri_props,
    hdri_rotation
]

def register():
    for cls in classes:
        register_class(cls)
        bpy.types.Scene.hdri = PointerProperty(type = hdri_props)
    
def unregister():
    for cls in classes:
        unregister_class(cls)
        del bpy.types.Scene.hdri
    
if __name__ == "__main__":
    register()