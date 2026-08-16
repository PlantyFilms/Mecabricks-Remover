bl_info = {
    "name": "MB Remover - Planty",
    "author": "Planty Films",
    "version": (1, 0, 0),
    "blender": (2, 8, 0),
    "description": "A solution for clearing Mecabricks files out of your Blend files.",    
    "category": "Materials",
}



import bpy


TARGET_IMP_NAMES = ["dents-1.png", "dents-2.png", "dirt.jpg", "fingerprints-1.png", "fingerprints-2.png", "scratches.png"]



class ErrorHelper:
    
    def Cleared(self):
        self.report({'INFO'}, "All items have been cleared!")
        
    def Already_Cleared(self):
        self.report({'ERROR'}, "Error: either there's no items to clear, or you've already cleared everything!")



def force_cleanup_materials(self):
    
    processed = False
    
    for mat in list(bpy.data.materials):
        
        if "mb:" in mat.name:
            
            mat.use_fake_user = False
            mat.user_clear() # To clear all users
            
            # To remove it:
            bpy.data.materials.remove(mat)
            
            processed = True
            
        else:
            
            continue
    
    
    return processed



def force_cleanup_nodes(self):
    
    processed = False
    
    for group in list(bpy.data.node_groups):
        
        if "mb_" in group.name:

            group.use_fake_user = False
            group.user_clear()
            
            # To remove it (again):
            bpy.data.node_groups.remove(group)
            
            processed = True
            
        else:
            
            continue

    
    return processed



def force_cleanup_images(self):
    
    processed = False
    
    for img in list(bpy.data.images):
        
        if img.name in TARGET_IMP_NAMES:
            
            img.use_fake_user = False
            img.user_clear()
            
            # To remove it (again):
            bpy.data.images.remove(img)
            
            processed = True
            
        else:
            
            continue

    
    return processed





class Cleaner_Method(bpy.types.Operator):
    bl_label = "Mecabricks Remover"
    bl_idname = "object.cleaner_method"
    
    bl_options = {"REGISTER", "UNDO"} 


    def execute (self, context):
        
        mats_clear = force_cleanup_materials(self)
        nodes_clear = force_cleanup_nodes(self)
        images_clear = force_cleanup_images(self)


        if not mats_clear and not nodes_clear and not images_clear:
            
            ErrorHelper.Already_Cleared(self)
            
            return {"CANCELLED"}
        
 
        bpy.ops.outliner.orphans_purge()


        # If both were true:
        ErrorHelper.Cleared(self)
        
        return {"FINISHED"}



    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 300)

    def draw(self, context):
        
        # To display the popup dialog:
        layout = self.layout
        col = layout.column(align = True)
        
        col.label(text = "This will delete ALL Mecabricks files in this scene.")
        col.label(text = "This action CANNOT be undone later. Are you sure?", icon = "ERROR")





class MBRemover(bpy.types.Panel):
    bl_category = "Mecabricks Remover"
    
    bl_label = "MB Remover"
    bl_idname = "MB_Remover"
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    
    def draw(self, context):
        layout = self.layout
                
        layout.operator("object.cleaner_method", text = "Clear All Mecabricks Files")





classes = (MBRemover, Cleaner_Method)


def register():
        
    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
