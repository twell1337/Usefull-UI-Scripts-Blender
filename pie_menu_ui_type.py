#тип экрана 2d редактора
#bpy.context.scene.window_mode
#тип режима редактирования в редакторе картинок
#context.scene.img_edit_mode
bl_info = {
    "name": "Pie UI",
    "author": "Twell",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "View 3D",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "category": "Interface",
}

import bpy
from bpy.types import Operator, Menu, PropertyGroup
from bpy.utils import register_class, unregister_class
from bpy.props import EnumProperty, StringProperty

IMG_EDIT_MODES = [
        ('VIEW', "View", ""),
        ('PAINT', "Paint", ""),
        ('MASK', "Mask", "")]

WINDOW_MODES = [('UV','UV',''),('IMAGE_EDITOR','Image','')]

WINDOW_ANIM_MODES = [
        ('TIMELINE','',''),
        ('SEQUENCE_EDITOR','',''),
        ('DOPESHEET','',''),
        ('NLA_EDITOR','',''),
        ('DRIVERS','',''),
        ('FCURVES','','')
        ]

WINDOW_NODE_MODES = [('ShaderNodeTree','',''),('GeometryNodeTree','','')]

# Изменение режима у Image Editor
class ChangeImageType(Operator):
    bl_idname = 'image.change_image_mode'
    bl_label = 'Change Image Mode'
    img_edit_mode: EnumProperty(name="Image Mode", items=IMG_EDIT_MODES)

    def execute(self, context):
        bpy.context.area.spaces[0].mode = self.img_edit_mode
        bpy.context.scene.img_edit_mode = self.img_edit_mode
        return {'FINISHED'}


class VIEW3D_MT_PIE_image_mode(Menu):
    bl_label = 'Edit Mode'

    @classmethod
    def poll(self, context):
        return context.area and context.area.ui_type in ['IMAGE_EDITOR']

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator('image.change_image_mode', text="View", icon='IMAGE_DATA').img_edit_mode = "VIEW"
        pie.operator('image.change_image_mode', text="Paint", icon='TPAINT_HLT').img_edit_mode = "PAINT"
        pie.operator('image.change_image_mode', text="Mask", icon='MOD_MASK').img_edit_mode = "MASK"


# Изменение типа окна между UV/Image Editor
class ChangeWindowMode(Operator):
    bl_idname = 'image.change_window_mode'
    bl_label = 'Change Image Type'
    window_mode: EnumProperty(name="Image Type", items=WINDOW_MODES)

    def execute(self, context):
        if self.window_mode != bpy.context.area.ui_type:
            bpy.context.scene.window_mode = self.window_mode
            bpy.context.area.ui_type = self.window_mode
        return {'FINISHED'}


class VIEW3D_MT_PIE_uv_image(Menu):
    bl_label = '2d Mode'

    @classmethod
    def poll(self, context):
        return context.area and context.area.ui_type in ['UV', 'IMAGE_EDITOR']

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator('image.change_window_mode', text="Image", icon='IMAGE').window_mode = "IMAGE_EDITOR"
        pie.operator('image.change_window_mode', text="UV", icon='UV').window_mode = "UV"

# Изменение окон анимации
class ChangeAnimWindowMode(Operator):
    bl_idname = 'anim.change_anim_mode'
    bl_label = 'Change Animation Type'
    window_anim_mode: EnumProperty(name="Mode", items=WINDOW_ANIM_MODES)

    def execute(self, context):
        bpy.context.scene.window_anim_mode = self.window_anim_mode
        bpy.context.area.ui_type = self.window_anim_mode
        return {'FINISHED'}


class VIEW3D_MT_PIE_anim(Menu):
    bl_label = 'Anim Mode'

    @classmethod
    def poll(self, context):
        return context.area and context.area.ui_type in [ui_type for ui_type, _, _ in WINDOW_ANIM_MODES]

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator('anim.change_anim_mode', text="Timeline", icon='TIME').window_anim_mode = "TIMELINE"
        pie.operator('anim.change_anim_mode', text="Dopesheet", icon='ACTION').window_anim_mode = "DOPESHEET"
        pie.operator('anim.change_anim_mode', text="Graph", icon='GRAPH').window_anim_mode = "FCURVES"
        pie.operator('anim.change_anim_mode', text="NLA Editor", icon='NLA').window_anim_mode = "NLA_EDITOR"
        pie.operator('anim.change_anim_mode', text="Drivers", icon='DRIVER').window_anim_mode = "DRIVERS"
        pie.operator('anim.change_anim_mode', text="Sequence Editor", icon='SEQUENCE').window_anim_mode = "SEQUENCE_EDITOR"

# Изменение окна нодов
class ChangeNodeMode(Operator):
    bl_idname = 'image.change_node_mode'
    bl_label = 'Change Node Type'
    window_node_mode: EnumProperty(name="Node Mode", items=WINDOW_NODE_MODES)

    def execute(self, context):
        bpy.context.scene.window_node_mode = self.window_node_mode
        bpy.context.area.ui_type = self.window_node_mode
        return {'FINISHED'}


class VIEW3D_MT_PIE_node(Menu):
    bl_label = 'Node Mode'

    @classmethod
    def poll(self, context):
        return context.area and context.area.ui_type in [ui_type for ui_type, _, _ in WINDOW_NODE_MODES]

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator('image.change_node_mode', text="Shader", icon='NODE_MATERIAL').window_node_mode = "ShaderNodeTree"
        pie.operator('image.change_node_mode', text="Geometry", icon='GEOMETRY_NODES').window_node_mode = "GeometryNodeTree"



classes = [
            ChangeImageType,
            VIEW3D_MT_PIE_image_mode,
            ChangeWindowMode,
            VIEW3D_MT_PIE_uv_image,
            ChangeAnimWindowMode,
            VIEW3D_MT_PIE_anim,
            ChangeNodeMode,
            VIEW3D_MT_PIE_node
            ]

def register():
    for elem in classes:
        register_class(elem)
    bpy.types.Scene.window_node_mode = EnumProperty(name="Mode", items=WINDOW_NODE_MODES)
    bpy.types.Scene.window_anim_mode = EnumProperty(name="Mode", items=WINDOW_ANIM_MODES)
    bpy.types.Scene.window_mode = EnumProperty(name="Mode", items=WINDOW_MODES)
    bpy.types.Scene.img_edit_mode = EnumProperty(name="Image Mode", items=IMG_EDIT_MODES)
    

def unregister():
    for elem in classes:
        unregister_class(elem)
    del bpy.types.Scene.window_node_mode
    del bpy.types.Scene.window_anim_mode
    del bpy.types.Scene.window_mode
    del bpy.types.Scene.img_edit_mode

if __name__ == "__main__":
    register()
