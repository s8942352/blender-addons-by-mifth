# BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2
#  of the License.
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
# END GPL LICENSE BLOCK #####


bl_info = {
    "name": "UV Utility",
    "author": "Paul Geraskin",
    "version": (0, 1),
    "blender": (2, 69, 0),
    "location": "View3D > ToolBar",
    "description": "Change Index Of UVMap.",
    "wiki_url": "",
    "tracker_url": "",
    "category": "UV"}


import bpy
from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       )
from bpy.props import *


class UV_IC_Panel():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'


class UV_IC_TexIndex(PropertyGroup):
    bpy.types.Scene.UVTexIndex = IntProperty(
        name="UVIndexToGet",
        description="get UVIndex of selected objects",
        min=1,
        max=8,
             default=1)

    bpy.types.Scene.UVTexGetName = StringProperty(
        name="UVNameToGet",
             description="get new UVName of selected objects",
             default="UVMap")

    bpy.types.Scene.UVTexRenderActive = BoolProperty(
        name="Set Render Active",
        description="Set Render Active...",
        default=False
    )


class UV_IC_Main(UV_IC_Panel, Panel):
    bl_context = "objectmode"
    bl_label = "UV Utility"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):

        layout = self.layout

        scene = context.scene
        ob = context.object

        col = layout.column(align=True)

        row = layout.row(align=True)
        row.operator("uvutil.change_index", text="Drop Active UV Back")

        row = layout.row(align=True)
        col = layout.column()
        col.prop(scene, "UVTexRenderActive")

        row = layout.row(align=True)
        col = layout.column()
        col.operator("uvutil.select_index", text="Select UVTexCoord")
        col.prop(scene, "UVTexIndex", text="UVTexCoord")
        row = layout.row(align=True)
        row = layout.row(align=True)
        col = layout.column()
        col.operator("uvutil.select_name", text="Select UV Name")
        col.prop(scene, "UVTexGetName", text="")
        row = layout.row(align=True)
        col = layout.column()
        col.operator("uvutil.remove_active", text="Remove Active UV")


class UV_IC_ChangeIndex(UV_IC_Panel, Operator):
    bl_idname = "uvutil.change_index"
    bl_label = "Change Index"

    def execute(self, context):
        scene = context.scene

        for theObj in context.selected_objects:
            meshData = theObj.data

            if theObj.type == 'MESH':
                if len(meshData.uv_textures) > meshData.uv_textures.active_index and len(meshData.uv_textures) > 0:
                    # meshData.uv_textures.active_index = 0
                    tmpuvmap = meshData.uv_textures.active
                    tmpuvmap_name = tmpuvmap.name

                    newuvmap = meshData.uv_textures.new()
                    meshData.uv_textures.remove(tmpuvmap)

                    droppedUV = meshData.uv_textures[
                        len(meshData.uv_textures) - 1]
                    droppedUV.name = tmpuvmap_name
                    # droppedUV.active = True
                    # if scene.UVTexRenderActive == True:
                      # droppedUV.active_render = True

        return{'FINISHED'}


class UV_IC_SelectIndex(UV_IC_Panel, Operator):
    bl_idname = "uvutil.select_index"
    bl_label = "Select Index"

    def execute(self, context):
        scene = context.scene

        for theObj in context.selected_objects:
            meshData = theObj.data
            indexNew = scene.UVTexIndex - 1

            if theObj.type == 'MESH':
                if len(meshData.uv_textures) > indexNew and len(meshData.uv_textures) > 0:
                    meshData.uv_textures.active_index = indexNew

                    if scene.UVTexRenderActive:
                        meshData.uv_textures[indexNew].active_render = True

        return{'FINISHED'}


class UV_IC_SelectName(UV_IC_Panel, Operator):
    bl_idname = "uvutil.select_name"
    bl_label = "Select Name"

    def execute(self, context):
        scene = context.scene

        for theObj in context.selected_objects:
            meshData = theObj.data
            uvName = scene.UVTexGetName

            if theObj.type == 'MESH':
                if len(meshData.uv_textures) > 0:
                    uvToGet = meshData.uv_textures.get(uvName)

                    if uvToGet is not None:
                        uvToGet.active = True

                        if scene.UVTexRenderActive:
                            uvToGet.active_render = True

        return{'FINISHED'}


class UV_IC_RemoveActiveUV(UV_IC_Panel, Operator):
    bl_idname = "uvutil.remove_active"
    bl_label = "Remove Active UV"

    def execute(self, context):
        scene = context.scene

        for theObj in context.selected_objects:
            meshData = theObj.data

            if theObj.type == 'MESH':
                if len(meshData.uv_textures) > 0:
                    activeIndex = meshData.uv_textures.active_index

                    if len(meshData.uv_textures) > activeIndex:
                        meshData.uv_textures.remove(
                            meshData.uv_textures[activeIndex])

        return{'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
