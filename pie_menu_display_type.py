bl_info = {
    "name": "Pie Menu Display Type",
    "author": "Twell",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "View 3D",
    "description": "VIEW3D_MT_PIE_display_type",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}

import bpy
from bpy.types import Operator, Menu
from bpy.utils import register_class, unregister_class
from bpy.props import EnumProperty

class ChangeDisplayType(Operator):
    bl_idname = 'selected_objects.change_display_type'
    bl_label = 'Change Display Type'
    bl_options = {'REGISTER', 'UNDO'}

    disp_type: EnumProperty(
        items=[
            ('SOLID', 'SOLID', 'Display as Solid'),
            ('TEXTURED', 'TEXTURED', 'Display as Textured'),
            ('BOUNDS', 'BOUNDS', 'Display Bounds'),
            ('WIRE', 'WIRE', 'Display as Wire'),
            ('WIREFRAME', 'Wireframe', 'Display Wireframe'),
            ('INFRONT', 'Infront', 'Display In Front'),
        ],
        name="Display Type",
        default='SOLID'
    )
    
    def selected_object_check(self, context):
        if bpy.context.object.select_get():
            sel_object = bpy.context.object
        else:
            sel_object = bpy.context.selected_objects[0]
        return sel_object

    def execute(self, context):
        if self.disp_type == 'WIREFRAME':
            check_object = self.selected_object_check(context)
            not_current_wire = not check_object.show_wire
            for obj in context.selected_objects:
                obj.show_wire = not_current_wire
            return {'FINISHED'}
        elif self.disp_type == 'INFRONT':
            check_object = self.selected_object_check(context)
            not_current_infront = not check_object.show_in_front
            for obj in context.selected_objects:
                obj.show_in_front = not_current_infront
            return {'FINISHED'}
        for obj in context.selected_objects:
            obj.display_type = self.disp_type          
        return {'FINISHED'}


class VIEW3D_MT_PIE_display_type(Menu):
    bl_label = 'Display Types'

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.area.type == 'VIEW_3D' and len(context.selected_objects)
    
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator('selected_objects.change_display_type', text="SOLID").disp_type = "SOLID"
        pie.operator('selected_objects.change_display_type', text="TEXTURED").disp_type = "TEXTURED"
        pie.operator('selected_objects.change_display_type', text="BOUNDS").disp_type = "BOUNDS"
        pie.operator('selected_objects.change_display_type', text="WIRE").disp_type = "WIRE"
        pie.operator('selected_objects.change_display_type', text="Wireframe").disp_type = "WIREFRAME"
        pie.operator('selected_objects.change_display_type', text="Infront").disp_type = "INFRONT"

classes = (
    ChangeDisplayType,
    VIEW3D_MT_PIE_display_type
)

def register():
    for Class in classes:
        register_class(Class)
    
    
def unregister():
    for Class in reversed(classes):
        unregister_class(Class)
    
if __name__ == "__main__":
    register()
