"""
Creating a character animation rig by applying Inverse Kinematics to a human metarig armature in Blender.
This can be used with any .blend file that features a human metarig from Rigify
Command line input for Windows:
    blender.exe kakashi_metarig.blend --python character_rig.py
"""
import bpy
import logging
from math import radians

LOG = logging.getLogger(__name__)

bl_info = {
    "Head": "Apply Inverse Kinematics to a human metarig",
    "blender": (2, 93, 0),
    "category": "Character Rigging",
}


"""def import_head_model(path):
    
    Import an OBJ model file, as the active object in the 3D viewport. 
    This function was used in section 3.5 - Building a scene
    :param file path:
    :return: object
    
    bpy.ops.import_scene.obj(filepath=path)
    obj = bpy.context.view_layer.objects["Kakashi"]
    bpy.context.view_layer.objects.active = obj
    return obj"""


scene = bpy.data.scenes.new("Scene")


def create_plane():
    """
    Sets up a flat plane in the scene
    """
    LOG.info("Created plane in scene")
    bpy.ops.mesh.primitive_plane_add(size=500)
    bpy.data.objects["Plane"].location[2] = -47


def create_camera():
    """
    Sets up virtual camera and its properties
    see: #https://spltech.co.uk/blender-3d%E2%80%8A-%E2%80%8Ahow-to-create-and-render-a-scene-in-blender-using-python-api/
    """
    LOG.info("Created camera in scene")
    cam_data = bpy.data.cameras.new('Camera')
    camera = bpy.data.objects.new('Camera', cam_data)
    camera.location = (1.839, -287.96, 13.695)
    camera.rotation_euler = ([radians(a) for a in (88, -359, 0.689)])
    camera.scale[0] = 13  # x
    camera.scale[1] = 13  # y
    camera.scale[2] = 13  # z
    bpy.context.collection.objects.link(camera)
    scene.camera = camera


def create_light():
    """
    Sets up the scene's light source and its properties
    see: https://spltech.co.uk/blender-3d%E2%80%8A-%E2%80%8Ahow-to-create-and-render-a-scene-in-blender-using-python-api/
    """
    LOG.info("Created light source in scene")
    light_data = bpy.data.lights.new('Light', type='AREA')
    light = bpy.data.objects.new('Light', light_data)
    bpy.context.collection.objects.link(light)
    light.location = (-42, -50, 104)
    light.data.energy = 800000.0
    light.scale[0] = 22  # x
    light.scale[1] = 22  # y
    light.scale[2] = 22  # z
    light.data.color[0] = 0.383  # r
    light.data.color[1] = 0.393  # g
    light.data.color[2] = 0.7    # b


#  The code below is inspired from: https://ashemclemore.blogspot.com/2019/05/autoik-span-display-block-overflow.html


def ik_bone_names(armature):
    """
    Checks the bones in human metarig armature and adds the shin and forearm bones to a list
    :param armature:
    :return: list of deformable bones that are used for inverse kinematic constraints
    """
    bone_names = []
    for bone in armature.bones:
        if bone.name == 'shin.L':
            bone_names.append(bone.name)
        elif bone.name == 'shin.R':
            bone_names.append(bone.name)
        elif bone.name == 'forearm.L':
            bone_names.append(bone.name)
        elif bone.name == 'forearm.R':
            bone_names.append(bone.name)

    return bone_names


def applyik(armature, armature_pose, ik_bone_names):
    """
    Iterates through bones used for inverse kinematics in the armature
    and applies inverse kinematics by creating a target bone, a pole bone, and IK constraints on each one.
    Forearm bones require the pole bone to be placed behind the model so the arm bones do not face the wrong way
    :param armature:
    :param armature_pose:
    :param ik_bone_names:
    :return:
    """
    LOG.info("Inverse kinematic constraints applied to bones")
    for name in ik_bone_names:
        pole_head_y, pole_tail_y = -10, -20  # pole bone extrude values for the shin bones

        if name == 'forearm.L':
            pole_head_y, pole_tail_y = 10, 20

        elif name == 'forearm.R':
            pole_head_y, pole_tail_y = 10, 20

        ik_bone = armature.bones[name]            # current IK bone's object data
        ik_bone_pose = armature_pose.bones[name]  # for modifying current IK bone's constraints in Pose Mode

        target_name = ik_bone.name + '.targetIK'
        pole_name = ik_bone.name + '.poleIK'

        bpy.context.view_layer.objects.active = bpy.data.objects[armature.name]
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        edit = bpy.context.object.data.edit_bones

        # creates new target bone
        edit.new(target_name)
        edit[target_name].head = ik_bone.tail_local
        edit[target_name].tail = ik_bone.tail_local
        edit[target_name].tail.y += 10        # extrudes target bone in y-axis
        edit[target_name].use_deform = False  # stops the new bone from deforming geometry of model

        # creates new pole bone
        edit.new(pole_name)
        edit[pole_name].head = ik_bone.head_local
        edit[pole_name].tail = ik_bone.head_local
        edit[pole_name].head.y += pole_head_y
        edit[pole_name].tail.y += pole_tail_y
        edit[pole_name].use_deform = False

        # apply IK constraints
        bpy.ops.object.mode_set(mode='POSE')
        ik_bone_pose.constraints.new('IK')
        ik_bone_pose.constraints['IK'].target = bpy.data.objects[armature.name]
        ik_bone_pose.constraints['IK'].subtarget = target_name
        ik_bone_pose.constraints['IK'].pole_target = bpy.data.objects[armature.name]
        ik_bone_pose.constraints['IK'].pole_subtarget = pole_name
        ik_bone_pose.constraints['IK'].chain_count = 2            # Constraint only effects the next parent bone
        ik_bone_pose.constraints['IK'].pole_angle = radians(-90)  # Makes the bone face towards its pole bone

        bpy.ops.object.mode_set(mode="OBJECT")


def check_armature(obj):
    """
    Applies inverse kinematics on the armature object
    if there are deformable bones (shin and forearm bones) used for IK constraints
    :param: object
    :return:
    """
    armature = obj.data       # armature's read-only object data
    armature_pose = obj.pose  # modifies armature in pose mode
    if len(ik_bone_names(armature)) == 0:
        LOG.info("No bones used for inverse kinematics found."
                 "Need to use Rigify human metarig to have forearm and shin bones")
    else:
        applyik(armature, armature_pose, ik_bone_names(armature))


if __name__ == "__main__":
    create_camera()
    create_light()
    create_plane()

    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE':
            LOG.info("Armature called " + obj.name + " found in scene")
            check_armature(obj)