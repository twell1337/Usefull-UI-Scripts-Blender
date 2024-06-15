bl_info = {
    "name": "Sculpt XYZ pie menu",
    "author": "Valentin Tselishchev",
    "version": (1, 0, 0),
    "blender": (2, 93, 5),
    "location": "View 3D",
    "description": "Pie-menu symmetry axis",
    "warning": "",
    "wiki_url": "",
    "category": "Sculpt",
}

import bpy
from bpy.types import Menu
from bpy.utils import register_class, unregister_class

    
class VIEW3D_MT_PIE_mirror_axis(Menu):
    bl_label = 'Mirror Axis'
    
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.prop(context.object, "use_mesh_mirror_x")
        pie.prop(context.object, "use_mesh_mirror_z")
        pie.prop(context.object, "use_mesh_mirror_y")



def register():
    register_class(VIEW3D_MT_PIE_mirror_axis)
    
    
def unregister():
    unregister_class(VIEW3D_MT_PIE_mirror_axis)
    
if __name__ == "__main__":
    register()