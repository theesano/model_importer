import Blender
armature = Blender.Object.Get('armature')
arm_data = armature.getData()

print("=== BONE DATA ===")
for bone in arm_data.bones.values():
    print("\nBone:", bone.name)
    print("  Head:", bone.head['ARMATURESPACE'])
    print("  Tail:", bone.tail['ARMATURESPACE'])
    print("  Matrix:")
    for row in bone.matrix['ARMATURESPACE']:
        print("   ", [round(v, 4) for v in row])
    if bone.parent:
        print("  Parent:", bone.parent.name)