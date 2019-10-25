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
from bpy.types import  Operator,AddonPreferences
from bpy.props import EnumProperty, StringProperty, BoolProperty, IntProperty, CollectionProperty, FloatProperty, FloatVectorProperty, PointerProperty

def save_render_slot(scene):
    user_preferences = bpy.context.preferences
    addon_prefs = user_preferences.addons["render_F12"].preferences
    save = addon_prefs.save
    images = bpy.data.images
    img = images['Render Result']
    slots = img.render_slots
    
    render = bpy.context.scene.render      
    path = bpy.path.abspath(render.filepath)
    ext = render.image_settings.file_format
    index = slots.active_index
    slot = slots[index]
    filepath = path+slot.name+"."+ext
    if save:
    
        bpy.data.images['Render Result'].save_render(filepath=filepath)
        #print(filepath)

def auto_slot_remove():
    
    images = bpy.data.images
    render = images['Render Result']
    slots = render.render_slots
    index = slots.active_index
    slots.active_index -= 1
    #print("dopo:"+str(slots.active_index))

def auto_slot_add():
    
    images = bpy.data.images
    render = images['Render Result']
    slots = render.render_slots
    index = slots.active_index
    n = len(slots)
    if index == n-1:
        slots.new()
    slots.active_index += 1
    #print("prima:"+str(slots.active_index))

class FTwelvePreferences(AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    not_show : BoolProperty(default=False)
    save : BoolProperty(default=False)
    oldpath : StringProperty(default=False)
    
    
    def draw(self, context):
        rd = context.scene.render
        layout = self.layout
        row = layout.row()   
        row.label(text="Set True if you don't want the option window")
        row = layout.row()   
        row.prop(self, "not_show", text="Don't show again" )
        
        row = layout.row()
        row.label(text="Autosave render in default path")
        row = layout.row()
        row.prop(self, "save", text="Autosave" )
        row.prop(rd, "filepath", text="File Path")







    
class RENDER_OT_FTwelve(Operator):
    """Tooltip"""
    bl_idname = "scene.f12_operator"
    bl_label = "Render output tools"
    
    def invoke(self, context, event):
        user_preferences = context.preferences
        addon_prefs = user_preferences.addons["render_F12"].preferences
        if addon_prefs.not_show:
            return self.execute(context) 
        else: 
            return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        
        user_preferences = context.preferences
        addon_prefs = user_preferences.addons["render_F12"].preferences
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        rd = context.scene.render   
  
        row = layout.row()   
        row.prop(addon_prefs, "not_show", text="Don't show again" )
        
        row = layout.row() 
        row.prop(addon_prefs, "save", text="Autosave" )
        
        row = layout.row()
        row.prop(rd, "filepath", text="File Path")
        
        row = layout.row()
        col = row.column()
        col.prop(rd, "resolution_x", text="Resolution X")
        col.prop(rd, "resolution_y", text="Y")
        col.prop(rd, "resolution_percentage", text="%")

    
    def execute(self, context):
        user_preferences = context.preferences
        addon_prefs = user_preferences.addons["render_F12"].preferences
        save = addon_prefs.save
        auto_slot_add()
        rd = context.scene.render 
        
            
        bpy.ops.render.render("INVOKE_DEFAULT",use_viewport=True, write_still=False)
        #print (rd.filepath)
        #rd.filepath = old_path
        #print ("render")        
        #auto_slot_remove()
        
            #print("path:"+path)           
            #addon_prefs.old_path = rd.filepath
            #rd.filepath = path
        return {'FINISHED'}


    
classes = ( FTwelvePreferences,
            
            RENDER_OT_FTwelve,
            

            
            
)

addon_keymaps = []
# kmi_defs entry: (identifier, key, action, CTRL, SHIFT, ALT, props, nice name)
# props entry: (property name, property value)
kmi_defs = (
    (RENDER_OT_FTwelve.bl_idname, 'F12', 'PRESS', False, False, True,
        (), "Screen"),
        )

def register():
    
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    # keymaps
    addon_keymaps.clear()
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Screen',space_type='EMPTY', region_type='WINDOW')
        for (identifier, key, action, CTRL, SHIFT, ALT, props, nicename) in kmi_defs:
            kmi = km.keymap_items.new(identifier, key, action, ctrl=CTRL, shift=SHIFT, alt=ALT)
            if props:
                for prop, value in props:
                    setattr(kmi.properties, prop, value)
            addon_keymaps.append((km, kmi))
            
    bpy.app.handlers.render_complete.append(save_render_slot)
def unregister():
    
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.app.handlers.render_complete.remove(save_render_slot)
if __name__ == "__main__":
    register()
