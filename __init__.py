# RandoGrid created by Midge "Mantissa" Sinnaeve (mantissa.xyz)
# Downloaded form https://github.com/mantissa-/RandoMesh
# Licensed under GPLv3

bl_info = {
    "name": "RandoGrid",
    "author": "Midge \"Mantissa\" Sinnaeve",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "View3D > Tool Shelf > RandoGrid Tab",
    "description": "Create random gridlike lines",
    "wiki_url": "https://github.com/mantissa-/RandoGrid",
    "category": "3D View",
    "warning": "You might have fun"
}


import bpy, bmesh, random
from bpy.props import (IntProperty, FloatProperty, BoolProperty, PointerProperty)
from bpy.types import (Panel, Operator, PropertyGroup)

#------------#
# PROPERTIES #
#------------#

class RandoGridProps(PropertyGroup):
    
    
    int_lines : IntProperty(
        name = "Number of Lines",
        description = "Set the amount of lines to draw in the grid",
        default = 150,
        min = 1,
        soft_max = 1000
        )
        
    int_line_steps : IntProperty(
        name = "Line Steps (Length)",
        description = "Set the amount of times the algorithm step trhough each line",
        default = 25,
        min = 1,
        soft_max = 250
        )
    
    fl_start_offset : FloatProperty(
        name = "Start Offset",
        description = "Maximum starting point offset",
        default = 1.0,
        min = 0,
        soft_max = 10.0
        )
        
    fl_width : FloatProperty(
        name = "Width",
        description = "Starting point spread over width",
        default = 5,
        soft_min = 0,
        soft_max = 10
        )
        
    fl_height : FloatProperty(
        name = "Height",
        description = "Starting point spread over height",
        default = 2.5,
        soft_min = 0,
        soft_max = 10
        )
        
    fl_y_rnd_min : FloatProperty(
        name = "Min",
        description = "Minimum forward movement",
        default = 1,
        soft_max = 10,
        soft_min = 0
        )
        
    fl_y_rnd_max : FloatProperty(
        name = "Max",
        description = "Maximum forward movement",
        default = 2.5,
        soft_min = 0,
        soft_max = 10
        )
        
    fl_x_rnd_min : FloatProperty(
        name = "Min",
        description = "Maximum movement to the left",
        default = -1,
        soft_min = -10,
        max = 0
        )
    
    fl_x_rnd_max : FloatProperty(
        name = "Max",
        description = "Maximum movement to the right",
        default = 1,
        soft_max = 10,
        min = 0
        )
        
    fl_z_rnd_min : FloatProperty(
        name = "Min",
        description = "Maximum movement to the top",
        default = -1,
        soft_min = -10,
        max = 0
        )
    
    fl_z_rnd_max : FloatProperty(
        name = "Max",
        description = "Maximum movement to the bottom",
        default = 1,
        soft_max = 10,
        min = 0
        )

    bool_limit_width : BoolProperty(
        name = "Limit Width",
        description = "Limit the width to the starting size",
        default = True
        )
        
    bool_limit_height : BoolProperty(
        name = "Limit Height",
        description = "Limit the height to the starting size",
        default = True
        )
        
    bool_make_curve : BoolProperty(
        name = "Make Curve",
        description = "Convert the final result to a beveled curve",
        default = True
        )


#----#
# UI #
#----#

class RandoGridPanel(bpy.types.Panel):
    # Creates a Panel in the sidebar
    bl_label = "RandoGrid"
    bl_idname = "OBJECT_PT_RandoGrid"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category = "RandoGrid"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        col = layout.column(align=False)
        row = layout.row(align=False)
        
        
        col.prop(scene.rg_props, "int_lines")
        col.prop(scene.rg_props, "int_line_steps")
        col.separator()
        
        col.prop(scene.rg_props, "fl_start_offset")
        col.prop(scene.rg_props, "fl_width")
        col.prop(scene.rg_props, "fl_height")
        col.separator()
        
        col.prop(scene.rg_props, "bool_limit_width")
        col.prop(scene.rg_props, "bool_limit_height")
        col.separator()
        
        col.label(text= "Length Step Growth")
        sub = col.row(align=True)
        sub.prop(scene.rg_props, "fl_y_rnd_min")
        sub.prop(scene.rg_props, "fl_y_rnd_max")
        col.separator()
        
        col.label(text= "Width Step Growth")
        sub = col.row(align=True)
        sub.prop(scene.rg_props, "fl_x_rnd_min")
        sub.prop(scene.rg_props, "fl_x_rnd_max")
        col.separator()
        
        col.label(text= "Height Step Growth")
        sub = col.row(align=True)
        sub.prop(scene.rg_props, "fl_z_rnd_min")
        sub.prop(scene.rg_props, "fl_z_rnd_max")
        col.separator()
        
        col.prop(scene.rg_props, "bool_make_curve")
        col.separator()

        sub = col.row()
        sub.scale_y = 2.0
        sub.operator("wm.randogrid")



#----------#
# OPERATOR #
#----------#

class RandoGrid(bpy.types.Operator):
    # RandoGrid Operator
    bl_idname = "wm.randogrid"
    bl_label = "CREATE RANDOM GRIDLINES"
    
    def execute(self, context):

        rgp = bpy.context.scene.rg_props

        iters = rgp.int_lines
        steps = rgp.int_line_steps

        y_start = rgp.fl_start_offset
        x_width = rgp.fl_width
        z_width = rgp.fl_height

        y_rnd = [rgp.fl_y_rnd_min, rgp.fl_y_rnd_max]
        x_rnd = [rgp.fl_x_rnd_min, rgp.fl_x_rnd_max]
        z_rnd = [rgp.fl_z_rnd_min, rgp.fl_z_rnd_max]

        limit_x = rgp.bool_limit_width
        limit_z = rgp.bool_limit_height

        ctoc = rgp.bool_make_curve
        
        
        me = bpy.data.meshes.new('GridLines') # create new mesh datablock
        bm = bmesh.new()   # create empty bmesh
        bm.from_mesh(me)   # fill from mesh

        for j in range(iters):
            x_max = x_width/2
            z_max = z_width/2
            
            # set random starting point
            x_pos = random.uniform(-x_max, x_max)
            y_pos = random.uniform(-y_start, y_start)
            z_pos = random.uniform(-z_max, z_max)

            new_vert = bm.verts.new((x_pos, y_pos, z_pos))

            for i in range(steps):
                old_vert = new_vert
                
                sel = random.choice([True, False])
                
                y_add = random.uniform(y_rnd[0], y_rnd[1])
                
                x_add = random.uniform(x_rnd[0], x_rnd[1])
                z_add = random.uniform(z_rnd[0], z_rnd[1])
                
                if i % 2 == 0: # add random length
                    y_pos += y_add
                    
                else:
                    if sel: # add to x
                        if limit_x: 
                            if x_pos + x_add > x_max or x_pos + x_add < -x_max:
                                x_pos -= x_add
                            else:
                                x_pos += x_add
                        else:
                            x_pos += x_add
                            
                    else: # add to z
                        if limit_z:
                            if z_pos + z_add > z_max or z_pos + z_add < -z_max:
                                z_pos -= z_add
                            else:
                                z_pos += z_add  
                        else:
                            z_pos += z_add
                  
                new_vert = bm.verts.new((x_pos, y_pos, z_pos))
                
                bm.edges.new((old_vert, new_vert))


        bm.to_mesh(me) # write bmesh to mesh
        bm.free()  # free bmesh

        bpy.ops.object.select_all(action='DESELECT')

        ob = bpy.data.objects.new('GridLines.000',me)
        bpy.context.scene.collection.objects.link(ob)
        ob.select_set(state=True)
        bpy.context.view_layer.objects.active = ob

        if ctoc:    
            bpy.ops.object.convert(target='CURVE')
            bpy.context.object.data.bevel_depth = 0.01
            
        return {'FINISHED'}

#----------#
# REGISTER #
#----------#

def register():
    bpy.utils.register_class(RandoGridPanel)
    bpy.utils.register_class(RandoGrid)
    bpy.utils.register_class(RandoGridProps)
    bpy.types.Scene.rg_props = PointerProperty(type=RandoGridProps)

def unregister():
    bpy.utils.unregister_class(RandoGridPanel)
    bpy.utils.unregister_class(RandoGrid)
    bpy.utils.unregister_class(RandoGridProps)
    del bpy.types.Scene.rg_props

if __name__ == "__main__":
    register()
