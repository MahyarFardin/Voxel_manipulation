world: {  }
table(world): { pose: [0, 0, 0.6], shape: ssBox, size: [1.6, 1.6, 0.08, 0.02], color: [0.3, 0.3, 0.3], contact: 1, logical: {  }, friction: 0.1 }
l_panda_base(table): { joint: rigid, mass: 0.692293, com: [-0.0330523, -0.00282329, 0.0478782], inertia: [0.00324422, -2.42323e-05, -0.000502638, 0.00383394, 9.03806e-06, 0.00410047], multibody, multibody_gravity! }
l_panda_link0(l_panda_base): { shape: mesh, mesh: </home/mahyar/miniconda3/envs/rai/lib/python3.10/site-packages/robotic/rai-robotModels/panda/meshes/link0.h5> }
l_panda_joint1_origin(l_panda_link0): { pose: [0, 0, 0.333] }
l_panda_joint1(l_panda_joint1_origin): { joint: hingeZ, limits: [-2.8973, 2.8973], shape: mesh, color: [1, 1, 1, 1], mesh: </home/mahyar/miniconda3/envs/rai/lib/python3.10/site-packages/robotic/rai-robotModels/panda/meshes/link1.h5>, mass: 0.54041, inertia: [0.00456315, -4.845e-08, 2.96516e-08, 0.00410729, 0.000986596, 0.00188739], mj_actuator_kp: "870.", mj_joint_damping: "100." }
l_panda_joint2_origin(l_panda_joint1): { pose: [0.707107, -0.707107, 0, 0] }
l_panda_joint2(l_panda_joint2_origin): { joint: hingeZ, limits: [-1.7628, 1.7628], q: [-0.5], shape: mesh, color: [1, 1, 1, 1], mesh: </home/mahyar/miniconda3/envs/rai/lib/python3.10/site-packages/robotic/rai-robotModels/panda/meshes/link2.h5>, mass: 0.5439, inertia: [0.00464633, 9.6386e-08, 7.04772e-08, 0.00190105, -0.0010021, 0.00418737], mj_actuator_kp: "870.", mj_joint_damping: "100." }
l_panda_joint3_origin(l_panda_joint2): { pose: [0, -0.316, 0, 0.707107, 0.707107, 0, 0] }
l_panda_joint3(l_panda_joint3_origin): { joint: hingeZ, limits: [-2.8973, 2.8973], shape: mesh, mesh: </home/mahyar/miniconda3/envs/rai/lib/python3.10/site-packages/robotic/rai-robotModels/panda/meshes/link3.h5>, mass: 0.546829, inertia: [0.00249312, -0.00055264, -0.000819764, 0.0029029, -0.000540692, 0.00252334], mj_actuator_kp: "870.", mj_joint_damping: "100." }
l_panda_joint4_origin(l_panda_joint3): { pose: [0.0825, 0, 0, 0.707107, 0.707107, 0, 0] }
l_panda_joint4(l_panda_joint4_origin): { joint: hingeZ, limits: [-3.0718, -0.0698], q: [-2], shape: mesh, mesh: </home/mahyar/miniconda3/envs/rai/lib/python3.10/site-packages/robotic/rai-robotModels/panda/meshes/link4.h5>, mass: 0.552034, inertia: [0.0025711, 0.000847668, -0.000560078, 0.0025553, 0.000559278, 0.0029871], mj_actuator_kp: "870.", mj_joint_damping: "100." }
l_panda_joint5_origin(l_panda_joint4): { pose: [-0.0825, 0.384, 0, 0.707107, -0.707107, 0, 0] }
l_panda_joint5(l_panda_joint5_origin): { joint: hingeZ, limits: [-2.8973, 2.8973], shape: mesh, mesh: </home/mahyar/miniconda3/envs/rai/lib/python3.10/site-packages/robotic/rai-robotModels/panda/meshes/link5.h5>, mass: 0.660949, inertia: [0.00852046, 2.33275e-06, -4.36368e-07, 0.00765386, -0.00177651, 0.00209358], mj_actuator_kp: "120.", mj_joint_damping: "10." }
l_panda_joint6_origin(l_panda_joint5): { pose: [0.707107, 0.707107, 0, 0] }
l_panda_joint6(l_panda_joint6_origin): { joint: hingeZ, limits: [0.5, 3], q: [2], shape: mesh, mesh: </home/mahyar/miniconda3/envs/rai/lib/python3.10/site-packages/robotic/rai-robotModels/panda/meshes/link6.h5>, mass: 0.499428, inertia: [0.00118765, -3.51984e-05, 0.000162183, 0.00164862, 7.06891e-06, 0.00209456], mj_actuator_kp: "120.", mj_joint_damping: "10." }
l_panda_joint7_origin(l_panda_joint6): { pose: [0.088, 0, 0, 0.707107, 0.707107, 0, 0] }
l_panda_joint7(l_panda_joint7_origin): { joint: hingeZ, limits: [-2.8973, 2.8973], q: [-0.5], shape: mesh, mesh: </home/mahyar/miniconda3/envs/rai/lib/python3.10/site-packages/robotic/rai-robotModels/panda/meshes/link7.h5>, mass: 0.508796, com: [0.00479288, 0.00293982, 0.110288], inertia: [0.0014038, -0.000585639, 3.48366e-05, 0.00139594, 5.49424e-05, 0.00158995], mj_actuator_kp: "120.", mj_joint_damping: "10." }
l_panda_joint8_origin(l_panda_joint7): { pose: [0, 0, 0.107] }
l_panda_joint8(l_panda_joint8_origin): {  }
l_panda_hand_joint_origin(l_panda_joint8): { pose: [0.92388, 0, 0, -0.382683] }
l_panda_hand_joint(l_panda_hand_joint_origin): { shape: mesh, mesh: </home/mahyar/miniconda3/envs/rai/lib/python3.10/site-packages/robotic/rai-robotModels/panda/meshes/hand.h5> }
l_panda_finger_joint1_origin(l_panda_hand_joint): { pose: [0, 0, 0.0584] }
l_panda_finger_joint2_origin(l_panda_hand_joint): { pose: [0, 0, 0.0584] }
l_panda_finger_joint1(l_panda_finger_joint1_origin): { joint: transY, limits: [0, 0.04], q: [0.04], shape: mesh, mesh: </home/mahyar/miniconda3/envs/rai/lib/python3.10/site-packages/robotic/rai-robotModels/panda/meshes/finger.h5>, mass: 0.0339598, inertia: [1.28954e-05, 3.94979e-10, 2.1346e-10, 1.25171e-05, 2.56044e-06, 3.22803e-06], mj_actuator_kp: "500.", mj_joint_damping: "100.", joint_active! }
l_panda_finger_joint2(l_panda_finger_joint2_origin): { joint: transY, joint_scale: -1, limits: [0, 0.04], mimic: "l_panda_finger_joint1", mass: 0.0339598, com: [-7.21322e-07, 0.0122672, 0.0270327], inertia: [1.28954e-05, 3.94979e-10, -2.1346e-10, 1.25171e-05, -2.56044e-06, 3.22803e-06], mj_actuator_kp: "500.", mj_joint_damping: "100." }
l_panda_rightfinger_0(l_panda_finger_joint2): { pose: [0, 0, 0, 1], shape: mesh, mesh: </home/mahyar/miniconda3/envs/rai/lib/python3.10/site-packages/robotic/rai-robotModels/panda/meshes/finger.h5> }
l_panda_coll0(l_panda_link0): { pose: [-0.04, 0, 0.03, 0.707107, 0, 0.707107, 0], shape: capsule, size: [0.1, 0.11], color: [1, 1, 1, 0.1], contact: -2 }
l_panda_coll1(l_panda_joint1): { pose: [0, 0, -0.15], shape: capsule, size: [0.2, 0.08], color: [1, 1, 1, 0.1], contact: -2 }
l_panda_coll3(l_panda_joint3): { pose: [0, 0, -0.15], shape: capsule, size: [0.2, 0.08], color: [1, 1, 1, 0.1], contact: -2 }
l_panda_coll5(l_panda_joint5): { pose: [0, 0.02, -0.2], shape: capsule, size: [0.22, 0.09], color: [1, 1, 1, 0.1], contact: -2 }
l_panda_coll2(l_panda_joint2): { shape: capsule, size: [0.12, 0.12], color: [1, 1, 1, 0.1], contact: -2 }
l_panda_coll4(l_panda_joint4): { shape: capsule, size: [0.12, 0.08], color: [1, 1, 1, 0.1], contact: -2 }
l_panda_coll6(l_panda_joint6): { pose: [0, 0, -0.04], shape: capsule, size: [0.1, 0.07], color: [1, 1, 1, 0.1], contact: -2 }
l_panda_coll7(l_panda_joint7): { pose: [0, 0, 0.01], shape: capsule, size: [0.1, 0.07], color: [1, 1, 1, 0.1], contact: -2 }
l_gripper(l_panda_joint7): { pose: [-2.57788e-17, 0, 0.2105, 2.34326e-17, 0.92388, 0.382683, 5.65713e-17], shape: marker, size: [0.03], color: [0.9, 0.9, 0.9], logical: { is_gripper } }
l_palm(l_panda_hand_joint): { pose: [0.707107, 0.707107, 0, 0], shape: capsule, size: [0.14, 0.07], color: [1, 1, 1, 0.1], contact: -3 }
l_finger1(l_panda_finger_joint1): { pose: [0, 0.008, 0.045], shape: ssBox, size: [0.02, 0.016, 0.02, 0.005], color: [1, 1, 1, 0.1], contact: -2 }
l_finger2(l_panda_finger_joint2): { pose: [0, -0.008, 0.045], shape: ssBox, size: [0.02, 0.016, 0.02, 0.005], color: [1, 1, 1, 0.1], contact: -2 }
cameraTop(world): { pose: [-0.01, -0.2, 1.8, 0.258819, -0.965926, -0, -0], shape: marker, size: [0.1], focalLength: 0.895, width: 640, height: 360, zRange: [0.5, 100] }
cameraWrist(l_panda_joint7): { pose: [0.0566288, -0.0138618, 0.158583, 0.371288, -0.0124238, 0.0272688, -0.928034], shape: camera, size: [0.1], focalLength: 0.895, width: 640, height: 360, zRange: [0.1, 10] }
panda_collCameraWrist(cameraWrist): { pose: [-4.44089e-18, 0, 0.02, 0.707107, 0, 0.707107, 0], shape: capsule, size: [0.05, 0.03], color: [1, 1, 1, 0.2], contact: -3 }
targetSurface: { pose: [0.179601, -0.259183, 0.642] }
targetSurface_tile_0(targetSurface): { pose: [-0.025, -0.025, 0], shape: ssBox, size: [0.05, 0.05, 0.004, 0.001], color: [0, 1, 1] }
targetSurface_tile_1(targetSurface): { pose: [0.025, -0.025, 0], shape: ssBox, size: [0.05, 0.05, 0.004, 0.001], color: [0, 1, 1] }
targetSurface_tile_2(targetSurface): { pose: [-0.025, 0.025, 0], shape: ssBox, size: [0.05, 0.05, 0.004, 0.001], color: [0, 1, 1] }
obj0_base: { pose: [0.124266, 0.307768, 0.675358, 0.297215, 0.582258, -0.717221, 0.241316], mass: 0.8, com: [0.025, 0.0125, 0.0125], inertia: [0.00475, 0.00025, -0.00025, 0.004875, 0.000125, 0.004875], multibody, multibody_fixedBase!, multibody_gravity }
obj0_cube0(obj0_base): { shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1 }
obj0_joint1(obj0_cube0): {  }
obj0_cube1(obj0_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0.05, 0, 0] }
obj0_joint2(obj0_cube1): {  }
obj0_cube2(obj0_joint2): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0.05, 0, 0.05] }
obj0_joint3(obj0_cube2): {  }
obj0_cube3(obj0_joint3): { pose: [-0.05, 0.05, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0, 0.05, 0] }
obj1_base: { pose: [0.664491, 0.127708, 0.66505, 0.428158, -0.000150342, 0.000332251, 0.903704], mass: 0.8, com: [0.025, 0.0125, 0.0125], inertia: [0.00475, 0.00025, -0.00025, 0.004875, 0.000125, 0.004875], multibody, multibody_fixedBase!, multibody_gravity }
obj1_cube0(obj1_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1 }
obj1_joint1(obj1_cube0): {  }
obj1_cube1(obj1_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0.05, 0, 0] }
obj1_joint2(obj1_cube1): {  }
obj1_cube2(obj1_joint2): { pose: [-0.05, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0, 0.05, 0] }
obj1_joint3(obj1_cube2): {  }
obj1_cube3(obj1_joint3): { pose: [0.05, -0.05, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0.05, 0, 0.05] }
obj2_base: { pose: [-0.279101, 0.393693, 0.665066, 0.707611, -0.000106334, -0.00046172, 0.706602], mass: 0.8, com: [0.025, 0.025, 0], inertia: [0.0045, 0.0045, 0.005], multibody, multibody_fixedBase!, multibody_gravity }
obj2_cube0(obj2_base): { shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1 }
obj2_joint1(obj2_cube0): {  }
obj2_cube1(obj2_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0.05, 0, 0] }
obj2_joint2(obj2_cube1): {  }
obj2_cube2(obj2_joint2): { pose: [-0.05, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0, 0.05, 0] }
obj2_joint3(obj2_cube2): {  }
obj2_cube3(obj2_joint3): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0.05, 0.05, 0] }
obj3_base: { pose: [0.451307, 0.443415, 0.675354, -0.771935, 0.319774, -0.210398, 0.507537], mass: 0.8, com: [0.025, 0.0125, 0.0375], inertia: [0.00475, -0.00025, -0.00025, 0.004875, -0.000125, 0.004875], multibody, multibody_fixedBase!, multibody_gravity }
obj3_cube0(obj3_base): { shape: box, size: [0.05, 0.05, 0.05], color: [0, 0, 0], contact: 1 }
obj3_joint1(obj3_cube0): {  }
obj3_cube1(obj3_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 0, 0], contact: 1, position: [0, 0, 0.05] }
obj3_joint2(obj3_cube1): {  }
obj3_cube2(obj3_joint2): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 0, 0], contact: 1, position: [0.05, 0, 0.05] }
obj3_joint3(obj3_cube2): {  }
obj3_cube3(obj3_joint3): { pose: [0, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 0, 0], contact: 1, position: [0.05, 0.05, 0.05] }
obj4_base: { pose: [-0.422462, 0.187929, 0.664996, -0.476917, -0.476757, 0.52215, 0.522123], mass: 0.8, com: [0.0125, -2.81893e-18, 0.0375], inertia: [0.005375, 8.45678e-20, 0.000375, 0.00575, -8.45678e-20, 0.004375], multibody, multibody_fixedBase!, multibody_gravity }
obj4_cube0(obj4_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1 }
obj4_joint1(obj4_cube0): {  }
obj4_cube1(obj4_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0, 0, 0.05] }
obj4_joint2(obj4_cube1): {  }
obj4_cube2(obj4_joint2): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0, 0, 0.1] }
obj4_joint3(obj4_cube2): {  }
obj4_cube3(obj4_joint3): { pose: [0.05, 0, -0.1], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0.05, 0, 0] }
obj6_base: { pose: [0.722055, 0.452888, 0.664997, 0.116334, 0.115977, 0.697436, 0.697566], mass: 0.8, com: [6.07153e-18, 0.0125, 0.05], inertia: [0.005375, 0.005, 0.004375], multibody, multibody_fixedBase!, multibody_gravity }
obj6_cube0(obj6_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1 }
obj6_joint1(obj6_cube0): {  }
obj6_cube1(obj6_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0, 0, 0.05] }
obj6_joint2(obj6_cube1): {  }
obj6_cube2(obj6_joint2): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0, 0, 0.1] }
obj6_joint3(obj6_cube2): {  }
obj6_cube3(obj6_joint3): { pose: [0, 0.05, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0, 0.05, 0.05] }
obj7_base: { pose: [0.315113, 0.621591, 0.665004, 0.208793, 0.000144348, -8.52607e-05, 0.97796], mass: 0.8, com: [0.0375, 0.0125, 0.0125], inertia: [0.00475, -0.000125, -0.000125, 0.00475, 0.000125, 0.00475], multibody, multibody_fixedBase!, multibody_gravity }
obj7_cube0(obj7_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1 }
obj7_joint1(obj7_cube0): {  }
obj7_cube1(obj7_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0.05, 0, 0] }
obj7_joint2(obj7_cube1): {  }
obj7_cube2(obj7_joint2): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0.05, 0, 0.05] }
obj7_joint3(obj7_cube2): {  }
obj7_cube3(obj7_joint3): { pose: [0, 0.05, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0.05, 0.05, 0] }
obj8_base: { pose: [0.345736, 0.326967, 0.665023, -0.505273, 0.494331, 0.50519, 0.495096], mass: 0.8, com: [0.0375, -3.06749e-17, 0.0125], inertia: [0.004375, 2.07322e-19, 0.000375, 0.00575, 2.43706e-19, 0.005375], multibody, multibody_fixedBase!, multibody_gravity }
obj8_cube0(obj8_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1 }
obj8_joint1(obj8_cube0): {  }
obj8_cube1(obj8_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0.05, 0, 0] }
obj8_joint2(obj8_cube1): {  }
obj8_cube2(obj8_joint2): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0.1, 0, 0] }
obj8_joint3(obj8_cube2): {  }
obj8_cube3(obj8_joint3): { pose: [-0.1, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0, 0, 0.05] }
obj9_base: { pose: [-0.257802, 0.685063, 0.665046, 0.74818, -0.000253618, -0.000179842, 0.663496], mass: 0.8, com: [0.0125, 0.025, 0.0125], inertia: [0.004875, -0.00025, 0.000125, 0.00475, 0.00025, 0.004875], multibody, multibody_fixedBase!, multibody_gravity }
obj9_cube0(obj9_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1 }
obj9_joint1(obj9_cube0): {  }
obj9_cube1(obj9_joint1): { pose: [0, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0, 0.05, 0] }
obj9_joint2(obj9_cube1): {  }
obj9_cube2(obj9_joint2): { pose: [0, -0.05, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0, 0, 0.05] }
obj9_joint3(obj9_cube2): {  }
obj9_cube3(obj9_joint3): { pose: [0.05, 0.05, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0.05, 0.05, 0] }
obj10_base: { pose: [-0.459526, 0.572621, 0.664981, -0.581881, 0.40162, 0.58181, 0.402012], mass: 0.8, com: [0.0125, -1.73472e-18, 0.0375], inertia: [0.005375, 5.20417e-20, 0.000375, 0.00575, -5.20417e-20, 0.004375], multibody, multibody_fixedBase!, multibody_gravity }
obj10_cube0(obj10_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1 }
obj10_joint1(obj10_cube0): {  }
obj10_cube1(obj10_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0, 0, 0.05] }
obj10_joint2(obj10_cube1): {  }
obj10_cube2(obj10_joint2): { pose: [0.05, 0, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0.05, 0, 0] }
obj10_joint3(obj10_cube2): {  }
obj10_cube3(obj10_joint3): { pose: [-0.05, 0, 0.1], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0, 0, 0.1] }
obj11_base: { pose: [-0.661422, 0.398927, 0.664972, 0.593813, 0.00023057, 0.000198484, 0.804603], mass: 0.8, com: [1.17511e-17, 0.025, 0.025], inertia: [0.005, 0.0045, 0.0045], multibody, multibody_fixedBase!, multibody_gravity }
obj11_cube0(obj11_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1 }
obj11_joint1(obj11_cube0): {  }
obj11_cube1(obj11_joint1): { pose: [0, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0, 0.05, 0] }
obj11_joint2(obj11_cube1): {  }
obj11_cube2(obj11_joint2): { pose: [0, -0.05, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0, 0, 0.05] }
obj11_joint3(obj11_cube2): {  }
obj11_cube3(obj11_joint3): { pose: [0, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0, 0.05, 0.05] }
obj12_base: { pose: [0.334198, 0.123458, 0.675346, -0.00153834, -0.50103, 0.499056, 0.707043], mass: 0.8, com: [0.0125, 0.025, 0.0125], inertia: [0.004875, -0.00025, 0.000125, 0.00475, 0.00025, 0.004875], multibody, multibody_fixedBase!, multibody_gravity }
obj12_cube0(obj12_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1 }
obj12_joint1(obj12_cube0): {  }
obj12_cube1(obj12_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0, 0, 0.05] }
obj12_joint2(obj12_cube1): {  }
obj12_cube2(obj12_joint2): { pose: [0, 0.05, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0, 0.05, 0] }
obj12_joint3(obj12_cube2): {  }
obj12_cube3(obj12_joint3): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0.05, 0.05, 0] }
obj13_base: { pose: [-0.023913, 0.683476, 0.675362, -0.667394, -0.264832, -0.27656, 0.638721], mass: 0.8, com: [0.0125, 0.0125, 0.0375], inertia: [0.00475, 0.000125, -0.000125, 0.00475, -0.000125, 0.00475], multibody, multibody_fixedBase!, multibody_gravity }
obj13_cube0(obj13_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1 }
obj13_joint1(obj13_cube0): {  }
obj13_cube1(obj13_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0, 0, 0.05] }
obj13_joint2(obj13_cube1): {  }
obj13_cube2(obj13_joint2): { pose: [0, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0, 0.05, 0.05] }
obj13_joint3(obj13_cube2): {  }
obj13_cube3(obj13_joint3): { pose: [0.05, -0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0.05, 0, 0.05] }
obj14_base: { pose: [-0.730779, 0.293291, 0.665003, -0.321097, -5.23127e-05, -0.000134923, 0.947046], mass: 0.8, com: [-1.04083e-17, 0.025, 0.025], inertia: [0.005, 0.0045, 0.0045], multibody, multibody_fixedBase!, multibody_gravity }
obj14_cube0(obj14_base): { shape: box, size: [0.05, 0.05, 0.05], color: [0, 0, 1], contact: 1 }
obj14_joint1(obj14_cube0): {  }
obj14_cube1(obj14_joint1): { pose: [0, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 0, 1], contact: 1, position: [0, 0.05, 0] }
obj14_joint2(obj14_cube1): {  }
obj14_cube2(obj14_joint2): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 0, 1], contact: 1, position: [0, 0.05, 0.05] }
obj14_joint3(obj14_cube2): {  }
obj14_cube3(obj14_joint3): { pose: [0, -0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 0, 1], contact: 1, position: [0, 0, 0.05] }
obj15_base: { pose: [-0.413638, 0.0171043, 0.665, -0.671051, -0.222915, -0.671041, 0.222941], mass: 0.8, com: [-8.67362e-18, 0.025, 0.05], inertia: [0.0055, 1.73472e-19, 1.73472e-19, 0.005, -0.0005, 0.0045], multibody, multibody_fixedBase!, multibody_gravity }
obj15_cube0(obj15_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1 }
obj15_joint1(obj15_cube0): {  }
obj15_cube1(obj15_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0, 0, 0.05] }
obj15_joint2(obj15_cube1): {  }
obj15_cube2(obj15_joint2): { pose: [0, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0, 0.05, 0.05] }
obj15_joint3(obj15_cube2): {  }
obj15_cube3(obj15_joint3): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0, 0.05, 0.1] }
obj16_base: { pose: [0.500697, 0.242736, 0.665001, -0.614554, -0.614446, -0.349899, -0.349786], mass: 0.8, com: [0.0125, 0.0125, 0.025], inertia: [0.004875, 0.000125, 0.00025, 0.004875, -0.00025, 0.00475], multibody, multibody_fixedBase!, multibody_gravity }
obj16_cube0(obj16_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1 }
obj16_joint1(obj16_cube0): {  }
obj16_cube1(obj16_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0.05, 0, 0] }
obj16_joint2(obj16_cube1): {  }
obj16_cube2(obj16_joint2): { pose: [-0.05, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0, 0, 0.05] }
obj16_joint3(obj16_cube2): {  }
obj16_cube3(obj16_joint3): { pose: [0, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0, 0.05, 0.05] }
obj17_base: { pose: [0.718713, 0.353093, 0.674704, -0.0134295, -0.0071736, 0.469706, 0.882692], mass: 0.8, com: [0.0125, 0.0125, 0.0125], inertia: [0.00475, 0.000125, 0.000125, 0.00475, 0.000125, 0.00475], multibody, multibody_fixedBase!, multibody_gravity }
obj17_cube0(obj17_base): { shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 0], contact: 1 }
obj17_joint1(obj17_cube0): {  }
obj17_cube1(obj17_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 0], contact: 1, position: [0, 0, 0.05] }
obj17_joint2(obj17_cube1): {  }
obj17_cube2(obj17_joint2): { pose: [0, 0.05, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 0], contact: 1, position: [0, 0.05, 0] }
obj17_joint3(obj17_cube2): {  }
obj17_cube3(obj17_joint3): { pose: [0.05, -0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 0], contact: 1, position: [0.05, 0, 0] }
obj18_base: { pose: [0.285499, 0.401998, 0.664999, 0.431197, 0.431237, 0.560408, 0.5604], mass: 0.8, com: [0.05, -8.67362e-18, 0.0125], inertia: [0.004375, 0.005375, 0.005], multibody, multibody_fixedBase!, multibody_gravity }
obj18_cube0(obj18_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1 }
obj18_joint1(obj18_cube0): {  }
obj18_cube1(obj18_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0.05, 0, 0] }
obj18_joint2(obj18_cube1): {  }
obj18_cube2(obj18_joint2): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0.05, 0, 0.05] }
obj18_joint3(obj18_cube2): {  }
obj18_cube3(obj18_joint3): { pose: [0.05, 0, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0.1, 0, 0] }
obj20_base: { pose: [0.433641, 0.56631, 0.665002, 0.361748, 0.607548, -0.361746, 0.607588], mass: 0.8, com: [0.0125, 0.0125, 0.0375], inertia: [0.00475, 0.000125, -0.000125, 0.00475, -0.000125, 0.00475], multibody, multibody_fixedBase!, multibody_gravity }
obj20_cube0(obj20_base): { shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 0], contact: 1 }
obj20_joint1(obj20_cube0): {  }
obj20_cube1(obj20_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 0], contact: 1, position: [0, 0, 0.05] }
obj20_joint2(obj20_cube1): {  }
obj20_cube2(obj20_joint2): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 0], contact: 1, position: [0.05, 0, 0.05] }
obj20_joint3(obj20_cube2): {  }
obj20_cube3(obj20_joint3): { pose: [-0.05, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 0], contact: 1, position: [0, 0.05, 0.05] }
obj21_base: { pose: [-0.35461, 0.319435, 0.71498, -0.35137, 0.614139, 0.349661, 0.614093], mass: 0.8, com: [0, 0, 0.075], inertia: [0.0065, 0.0065, 0.004], multibody, multibody_fixedBase!, multibody_gravity }
obj21_cube0(obj21_base): { shape: box, size: [0.05, 0.05, 0.05], color: [0, 0, 0], contact: 1 }
obj21_joint1(obj21_cube0): {  }
obj21_cube1(obj21_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 0, 0], contact: 1, position: [0, 0, 0.05] }
obj21_joint2(obj21_cube1): {  }
obj21_cube2(obj21_joint2): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 0, 0], contact: 1, position: [0, 0, 0.1] }
obj21_joint3(obj21_cube2): {  }
obj21_cube3(obj21_joint3): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 0, 0], contact: 1, position: [0, 0, 0.15] }