# GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####



import bpy

bl_info = {
    "name": "Selection2Collection",
    "author": "CDMJ",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "3D View and Outliner",
    "description": "Hack to enable creating a collection from a selection of obejcts with Ctrl G",
    "warning": "",
    "category": "Material"
}


class OBJECT_OT_selection_to_collection(bpy.types.Operator):
    """Create a new collection from selected objects"""
    bl_idname = "object.selection_to_collection"
    bl_label = "Create New Collection from Selection"
    bl_options = {'REGISTER', 'UNDO'}
    
    collection_name: bpy.props.StringProperty(
        name="Collection Name",
        default="New Collection"
    )
    
    def execute(self, context):
        # Get selected objects
        selected_objects = context.selected_objects
        
        if not selected_objects:
            self.report({'WARNING'}, "No objects selected!")
            return {'CANCELLED'}
        
        # Create new collection
        new_collection = bpy.data.collections.new(self.collection_name)
        
        # Link the new collection to the active scene
        context.scene.collection.children.link(new_collection)
        
        # Add selected objects to the new collection and unlink from other collections
        for obj in selected_objects:
            # Link to the new collection
            new_collection.objects.link(obj)
            # Unlink from other collections
            for coll in obj.users_collection:
                if coll != new_collection:
                    coll.objects.unlink(obj)
        
        self.report({'INFO'}, f"Created collection '{self.collection_name}' with {len(selected_objects)} objects.")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# Register and Unregister the operator
def menu_func(self, context):
    self.layout.operator(OBJECT_OT_selection_to_collection.bl_idname)

addon_keymaps = []

def register():
    bpy.utils.register_class(OBJECT_OT_selection_to_collection)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    bpy.types.OUTLINER_MT_collection.append(menu_func)

    # Add keymap entry for Ctrl+G
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(OBJECT_OT_selection_to_collection.bl_idname, 'G', 'PRESS', ctrl=True)
    addon_keymaps.append((km, kmi))
    
    # Add keymap entry for Ctrl+G in the Outliner
    km_outliner = wm.keyconfigs.addon.keymaps.new(name='Outliner', space_type='OUTLINER')
    kmi_outliner = km_outliner.keymap_items.new(OBJECT_OT_selection_to_collection.bl_idname, 'G', 'PRESS', ctrl=True)
    addon_keymaps.append((km_outliner, kmi_outliner))

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_selection_to_collection)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.types.OUTLINER_MT_collection.remove(menu_func)

    # Remove keymap entries
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
