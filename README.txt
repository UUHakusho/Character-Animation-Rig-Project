Blender and Python Character Animation Rig Project.
For the visuals see: https://uyi30.artstation.com/projects/d0mV3J

This project creates a character animation rig using a script that automatically applies Inverse Kinematic constraints on specified bones of a human Metarig
from Blender's Rigify Add-On, effectively speeding up the rigging process which would be useful in a art pipeline. This script can work on any .blend file with the Human Metarig. The final result includes a 3D model skinned to a functional rig.
Command line input for Windows:
    blender.exe kakashi_metarig.blend --python character_rig.py


1.) All Supplementary files:
character_rig.py = The main python script that applies IK to a rig
start_debug_log.py = Startup script that sets up logging and debugging
kakashi_metarig.blend = Features the created humanoid stylised character model, cel shaded in Blender, and Rigify’s metarig.
character_animation_rig.blend = Final result, the animation rig, result of character_rig.py ran with kakashi_metarig.blend. finalised with weight painting
README.txt 	= this file

2.) System requirements to run project:
- Must have Blender version 2.8+ (along with its system requirements)
- Desired: Python 3.0+ installed
- Desired: Windows 10+ (if using Linux or Mac, the command line input: "blender.exe" becomes "blender")

4.) How to run this project:
- OPTIONAL: to use your systems command prompt to run the following command.
- In the command prompt go to the directory where the supplementary material is stored and execut the command (for Windows):  blender.exe kakashi_metarig.blend --python character_rig.py
- A Blender file should open consisting of a scene, light, camera, plane, the character model, and a armature object with Inverse Kinematic constraints

-IF NOT USING COMMAND PROMPT: Open the kakashi_metarig.blend file in Blender. Go to the Scripting Tab at the near the top of the UI,
 select "New" and open the character_rig.py script, then select the run button and the rig should be ready.
