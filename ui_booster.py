#alt t
#node_popup
#wm.sticky_uv_editor

bl_info = {
    "name": "UI Booster",
    "author": "Twell",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View 3D",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "category": "Interface",
}

import bpy
from bpy.types import Operator, PropertyGroup
from bpy.utils import register_class, unregister_class
from bpy.props import BoolProperty, PointerProperty, StringProperty, FloatProperty

import bgl
import gpu
from gpu_extras.batch import batch_for_shader


def clamp(x, l, u):
    return l if x < l else u if x > u else x

class FastAreaSplit(Operator):
    bl_idname = "wm.fast_split_area"
    bl_label = "Fast Area Split"
    
    @classmethod
    def poll(self, context):
        return context.area
            
    def invoke(self, context, event):
        if context.window.screen.show_fullscreen is True:
            return {'CANCELLED'}
        self.widgets = []
        args = (self, context)
        self.register_handlers(args, context)
        
        self.align = 'Horizontal'
        context.window_manager.modal_handler_add(self)
        context.area.header_text_set("Area split: " + self.align)
        return {'RUNNING_MODAL'}
    
    def register_handlers(self, args, context):
        self.space_type = type(bpy.context.space_data)
        self.draw_handle = self.space_type.draw_handler_add(self.draw_callback_px,args,"WINDOW","POST_PIXEL")
            
        self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)
        
    def unregister_handlers(self, context):
        context.window_manager.event_timer_remove(self.draw_event)
        self.space_type.draw_handler_remove(self.draw_handle, "WINDOW")
    
    def modal(self, context, event):
        m_x, m_y = event.mouse_x, event.mouse_y
        x1 = clamp(m_x-context.area.x,35,context.area.width-35)
        x2 = clamp(m_x-context.area.x,35,context.area.width-35)
        x3 = context.area.width
        x4 = 0
        y1 = context.area.height
        y2 = clamp(m_y-context.area.y,20,context.area.height-30)
        y3 = clamp(m_y-context.area.y,20,context.area.height-30)
        y4 = 0
        if self.align == 'Vertical':
            self.create_batch([(x1,y4), (x2,y1)])
            self.length = (clamp(m_x-context.area.x,0,context.area.width))/context.area.width
            
        elif self.align == 'Horizontal':
            self.create_batch([(x4,y2), (x3,y3)])
            self.length = (clamp(m_y-context.area.y,0,context.area.height))/context.area.height
                
        if event.value == "RELEASE" and event.type == "V":
            self.create_batch([(x1,y4), (x2,y1)])
            self.align = 'Vertical'
            self.length = (clamp(m_x-context.area.x,0,context.area.width))/context.area.width
            
        elif event.value == "RELEASE" and event.type == "H":
            self.create_batch([(x4,y2), (x3,y3)])
            self.align = 'Horizontal'
            self.length = (clamp(m_y-context.area.y,0,context.area.height))/context.area.height
            
        elif event.type == "LEFTMOUSE":
            self.unregister_handlers(context)
            context.area.header_text_set(None)
            bpy.ops.screen.area_split(direction = self.align.upper(), factor = self.length)
            return {"FINISHED"}
        elif event.type == "ESC":
            self.unregister_handlers(context)
            context.area.header_text_set(None)
            context.area.tag_redraw()
            return {"CANCELLED"}
        context.area.header_text_set("Area split: " + self.align)
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}
    
    def create_batch(self,verts):
        self.shader = gpu.shader.from_builtin("2D_UNIFORM_COLOR")
        self.batch = batch_for_shader(self.shader, "LINE_LOOP", {"pos":verts})
        
    def draw_callback_px(self,op,context):
        bgl.glLineWidth(1)
        self.shader.bind()
        self.shader.uniform_float("color",(0.8, 0.8, 0.8, 0.7))
        self.batch.draw(self.shader)

class EditorProps(PropertyGroup):
    region_node_header : BoolProperty(default = False)
    region_node_ui : BoolProperty(default = False)
    shader_node_type : StringProperty(default = 'OBJECT')

    region_uv_toolbar : BoolProperty(default = False)
    region_uv_ui : BoolProperty(default = False)
    region_type : StringProperty(default = 'UV')

class AnimationEditorPopup(Operator):
    bl_idname = "wm.sticky_animation_editor"
    bl_label = "Sticky Animation Editor"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(self, context):
        return context.area and context.area.ui_type in ['VIEW_3D']

    def invoke(self, context, event):
        self.editor_props = context.scene.editor_props
        scene = context.scene
        active_area = context.area
        
        if context.window.screen.show_fullscreen is True:
            self.report({'WARNING'},
                        "Sticky Editor: Fullscreen mode is not supported!")
            return {'FINISHED'}

        areas = context.screen.areas
        active_area_x = active_area.x
        active_area_y = active_area.y

        # Split active 3D View area
        propo = 0.2
        bpy.ops.screen.area_split(direction='HORIZONTAL', factor=propo)
        
        # Open Editor
        for area in reversed(context.screen.areas):
            if area.ui_type == 'VIEW_3D':
                anim_area = area
                break

        anim_area.ui_type = 'TIMELINE'

        # Создается окно таймлайна и закрывается таймлайн на предыдущем окне
        context = bpy.context.copy()
        bpy.ops.screen.area_dupli({'area': anim_area}, 'INVOKE_DEFAULT')
        windows = bpy.context.window_manager.windows

        # Получаем доступ к текущей области таймлайна, если она есть
        timeline_area = None
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.ui_type == 'TIMELINE':
                    override = {'window': window, 'screen': screen, 'area': area}
                    bpy.ops.screen.area_close(override)
                    return {'FINISHED'} 
        
        return {'FINISHED'} 

class ShaderEditorPopup(Operator):
    bl_idname = "wm.sticky_shader_editor"
    bl_label = "Sticky Shader Editor"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(self, context):
        return context.area and context.area.ui_type in ['ShaderNodeTree', 'VIEW_3D']

    def invoke(self, context, event):
        self.editor_props = context.scene.editor_props
        scene = context.scene
        active_area = context.area
        
        if context.window.screen.show_fullscreen is True:
            self.report({'WARNING'},
                        "Sticky Editor: Fullscreen mode is not supported!")
            return {'FINISHED'}

        areas = context.screen.areas
        active_area_x = active_area.x
        active_area_y = active_area.y
        # active_area_width = active_area.width

        # Close existing Editor
        if active_area.ui_type == 'ShaderNodeTree':
            for area in areas:
                if area.ui_type == 'VIEW_3D':
                    area_x = area.x
                    area_y = area.y
                    # area_width = area.width

                    # Areas in one horizontal space
                    if area_x < active_area_x:
                        if active_area_y == area_y:
                            # Save Editor area settings
                            self.editor_props.region_node_header = active_area.spaces[0].show_region_header
                            self.editor_props.region_node_ui = active_area.spaces[0].show_region_ui
                            self.editor_props.shader_node_type = active_area.spaces[0].shader_type
                            # Close Editor area
                            bpy.ops.screen.area_close({"area": active_area})
                            return {'FINISHED'}
                        else:
                            self.report({'WARNING'},"Sticky Editor: Shader Editor should be at the bottom of 3D view!")
                            return {'FINISHED'}
            self.report({'WARNING'},"Sticky Editor: Failed to figure out current layout!")
            return {'FINISHED'}
        elif active_area.ui_type == 'VIEW_3D':
            for area in areas:
                if area.ui_type == 'ShaderNodeTree':
                    area_x = area.x
                    area_y = area.y
                    # area_width = area.width

                    # Areas in one horizontal space
                    if active_area_x < area_x:
                        if active_area_y == area_y:
                            # Save Editor area settings
                            self.editor_props.region_node_header = area.spaces[0].show_region_header
                            self.editor_props.region_node_ui = area.spaces[0].show_region_ui
                            self.editor_props.shader_node_type = area.spaces[0].shader_type
                            # Close Editor area
                            bpy.ops.screen.area_close({"area": area})
                            return {'FINISHED'}
                        else:
                            self.report({'WARNING'},"Sticky Editor: Shader Editor should be at the bottom of 3D view!")
                            return {'FINISHED'}

        # Split active 3D View area
        propo = 0.6
        bpy.ops.screen.area_split(direction='VERTICAL', factor=propo)
        
        # Open Editor
        for area in reversed(context.screen.areas):
            if area.ui_type == 'VIEW_3D':
                shader_area = area
                break

        shader_area.ui_type = 'ShaderNodeTree'
        shader_space = shader_area.spaces[0]
        shader_space.show_region_header = self.editor_props.region_node_header
        shader_space.show_region_ui = self.editor_props.region_node_ui
        shader_space.shader_type = self.editor_props.shader_node_type
        
        return {'FINISHED'} 

class UVEditorPopup(Operator):
    bl_idname = "wm.sticky_uv_editor"
    bl_label = "Sticky UV Editor"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(self, context):
        return context.area and context.area.ui_type in ['UV', 'IMAGE_EDITOR', 'VIEW_3D', 'PROPERTIES']

    def save_props(self, area):
        space = area.spaces[0]
        self.editor_props.region_uv_toolbar = space.show_region_toolbar
        self.editor_props.region_uv_ui = space.show_region_ui
        self.editor_props.region_type = area.ui_type


    def invoke(self, context, event):
        self.editor_props = context.scene.editor_props
        scene = context.scene
        active_area = context.area
        
        if context.window.screen.show_fullscreen is True:
            self.report({'WARNING'},
                        "Sticky Editor: Fullscreen mode is not supported!")
            return {'FINISHED'}

        areas = context.screen.areas
        active_area_x = active_area.x
        active_area_y = active_area.y
        # active_area_width = active_area.width

        # Close existing Editor
        if active_area.ui_type in ['UV','IMAGE_EDITOR']:
            for area in areas:
                if area.ui_type == 'VIEW_3D':
                    area_x = area.x
                    area_y = area.y

                    # Areas in one horizontal space
                    if area_y == active_area_y:
                        # UV Editor on left
                        if active_area_x < area_x:
                            # Save Editor area settings
                            self.save_props(active_area)
                            # Close Editor area
                            active_area.ui_type = 'PROPERTIES'
                            return {'FINISHED'}

            self.report({'WARNING'},"Sticky Editor: Failed to figure out current layout!")
            return {'FINISHED'}
        elif active_area.ui_type == 'VIEW_3D':
            for area in areas:
                if area.ui_type in ['UV','IMAGE_EDITOR']:
                    area_x = area.x
                    area_y = area.y

                    # Areas in one horizontal space
                    if area_y == active_area_y:
                        # 3D View on left
                        if active_area_x > area_x:
                            # Save Editor area settings
                            self.save_props(area)
                            # Close Editor area
                            area.ui_type = 'PROPERTIES'
                            return {'FINISHED'}
                    else:
                        self.report({'WARNING'},"Sticky Editor: UV Editor should be on par with 3d view!")
                        return {'FINISHED'}
        
        # Open Editor
        for area in reversed(context.screen.areas):
            if area.ui_type == 'PROPERTIES':
                current_area = area
                break

        current_area.ui_type = self.editor_props.region_type
        space = current_area.spaces[0]

        if current_area.ui_type == 'IMAGE_EDITOR':
            space.mode = context.scene.img_edit_mode
        elif current_area.ui_type == 'UV':
            space.show_region_toolbar = self.editor_props.region_uv_toolbar
            space.show_region_ui = self.editor_props.region_uv_ui
        
        return {'FINISHED'} 
    
    
classes = (EditorProps,
AnimationEditorPopup,
ShaderEditorPopup,
UVEditorPopup,
FastAreaSplit
)


def register():
    for cls in classes:
        register_class(cls)
        bpy.types.Scene.editor_props = PointerProperty(type = EditorProps)
    
    
def unregister():
    for cls in classes:
        unregister_class(cls)
    del bpy.types.Scene.editor_props
    
if __name__ == "__main__":
    register()