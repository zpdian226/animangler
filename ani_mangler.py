# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****
bl_info = {
    "name": "Animangler",
    "author": "Philip Cote ( cotejrp1 )",
    "version": (1, 0, 0 ),
    "blender": (2, 5, 7),
    "api": 35853,
    "location": "VIEW3D -> TOOLS",
    "description": "Create a shape key for a mesh and move the vertices around randonly",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Animation"}

"""
HOW TO USE:
1.  Select the mesh you want to create mangled shape keys for.
2.  Set the degree of mangling you want.
3.  Press the "Ani-Mangle" button.
4.  Repeat steps 2 and 3 for each mangled shape key you wish to create.
"""

import bpy, random, time
from pdb import set_trace
    
class AnimanglerOperator(bpy.types.Operator):
    '''makes a shape key and pushes the verts around on it to set up for random pulsating animation.'''
    bl_idname = "bpt.ani_mangler"
    bl_label = "Ani-Mangle"
    

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return ob != None and ob.type == 'MESH'

    def execute(self, context):
        
        random.seed( time.time() )
        randomMag = bpy.context.scene.randomMagnitude
        
        ob = context.object
        shapeKey = ob.shape_key_add()
        verts = shapeKey.data
        
        for vert in verts:
            xVal = .01 * random.randrange( -randomMag, randomMag )
            yVal = .01 * random.randrange( -randomMag, randomMag)
            zVal = .01 * random.randrange( -randomMag, randomMag )
            vert.co.x = vert.co.x + xVal
            vert.co.y = vert.co.y + yVal
            vert.co.z = vert.co.z + zVal    
            
        return {'FINISHED'}


class AnimanglerPanel( bpy.types.Panel ):
    
    bl_label = "Animangler"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    
    def draw( self, context ):
        scn = context.scene
        
        layout = self.layout
        col = layout.column()
        col.prop( scn, "randomMagnitude" )
        col.operator( "bpt.ani_mangler" )
        
    
def register():
    bpy.utils.register_class(AnimanglerOperator)
    bpy.utils.register_class( AnimanglerPanel )
    scnType = bpy.types.Scene
    scnType.randomMagnitude = bpy.props.IntProperty( name = "How Much Mangling", 
                                                 default = 5, min = 1, max = 20, 
                            description = "The (+) and (-) number range for a random number to be picked from" )


def unregister():
    bpy.utils.unregister_class(AnimanglerOperator)
    bpy.utils.unregister_class(AnimanglerPanel)


if __name__ == "__main__":
    register()
