bl_info = {
    "name": "F12",
    "author": "Alfonso Annarumma",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Toolbox",
    "description": "Render Options, autoslot selection, path setting etc..",
    "warning": "",
    "wiki_url": "",
    "category": "Render",
    }


import bpy
from bpy.types import  Operator
from bpy.props import EnumProperty, StringProperty, BoolProperty, IntProperty, CollectionProperty, FloatProperty, FloatVectorProperty, PointerProperty


def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO', field='NONE'):

    def draw(self, context):
        
        user_preferences = context.preferences
        addon_prefs = user_preferences.addons["F12"].preferences
        layout = self.layout
        rd = context.scene.render
        
        row = layout.row()
        row.label(text="Render Options")
  
        row = layout.row()   
        row.prop(addon_prefs, "not_show", text="Don't show again" )
        row.prop(rd, "filepath", text="")
        
        row = layout.row()
        col = row.column(align=True)
        col.prop(rd, "resolution_x", text="Resolution X")
        col.prop(rd, "resolution_y", text="Y")
        col.prop(rd, "resolution_percentage", text="%")
        
        
        row = layout.row()
        row.operator("render.f12_cancel", text= "Cancel")
        row.operator("render.fTwelve", text= "Render")
        
        
        
        
                
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

def auto_slot_remove():
    
    images = bpy.data.images
    render = images['Render Result']
    slots = render.render_slots
    index = slots.active_index
    slots.active_index -= 1
    print("dopo:"+str(slots.active_index))

def auto_slot_add():
    
    images = bpy.data.images
    render = images['Render Result']
    slots = render.render_slots
    index = slots.active_index
    n = len(slots)
    if index == n-1:
        slots.new()
    slots.active_index += 1
    print("prima:"+str(slots.active_index))

class FTwelvePreferences(AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    not_show : BoolProperty(default=False)
    
    
    def draw(self, context):
        layout = self.layout
        
class RENDER_OT_Cancel_FTwelve(Operator):
    """Cancel Button"""
    bl_idname = "render.f12_cancel"
    bl_label = "Cancel Button"
    
        
    def execute(self, context):
        
        
        return {'CANCELLED'}
    
class RENDER_OT_FTwelve(Operator):
    """Tooltip"""
    bl_idname = "render.fTwelve"
    bl_label = "Render output tools"

    def execute(self, context):
        auto_slot_add()
        bpy.ops.render.render(use_viewport=True)    
        auto_slot_remove()
        return {'FINISHED'}

class RENDER_OT_Popup_FTwelve(Operator):
    """Popup For F12 Options"""
    bl_idname = "scene.f12_popup"
    bl_label = "Remove Popup"
    
    field : StringProperty()
    
        
    def execute(self, context):
        #print ("ok")
        ShowMessageBox("Render Options", "RENDER OPTIONS", 'INFO', self.field)
        return {'FINISHED'}
    
classes = ( FTwelvePreferences,
            RENDER_OT_Popup_FTwelve,
            RENDER_OT_FTwelve,
            RENDER_OT_Cancel_FTwelve,

            
            
)

def register():
    
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    deactive()
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
