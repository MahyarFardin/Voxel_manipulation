world: {  }
table(world): { pose: [0, 0, 0.6], shape: ssBox, size: [1.6, 1.6, 0.08, 0.02], color: [0.3, 0.3, 0.3], contact: 1, logical: {  }, friction: 0.1 }
l_panda_base(table): { joint: rigid, mass: 0.692293, com: [-0.0330523, -0.00282329, 0.0478782], inertia: [0.00324422, -2.42323e-05, -0.000502638, 0.00383394, 9.03806e-06, 0.00410047], multibody, multibody_gravity! }
l_panda_link0(l_panda_base): { shape: mesh, mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/link0.h5> }
l_panda_joint1_origin(l_panda_link0): { pose: [0, 0, 0.333] }
l_panda_joint1(l_panda_joint1_origin): { joint: hingeZ, limits: [-2.8973, 2.8973], shape: mesh, color: [1, 1, 1, 1], mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/link1.h5>, mass: 0.54041, inertia: [0.00456315, -4.845e-08, 2.96516e-08, 0.00410729, 0.000986596, 0.00188739], mj_actuator_kp: "870.", mj_joint_damping: "100." }
l_panda_joint2_origin(l_panda_joint1): { pose: [0.707107, -0.707107, 0, 0] }
l_panda_joint2(l_panda_joint2_origin): { joint: hingeZ, limits: [-1.7628, 1.7628], q: [-0.5], shape: mesh, color: [1, 1, 1, 1], mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/link2.h5>, mass: 0.5439, inertia: [0.00464633, 9.6386e-08, 7.04772e-08, 0.00190105, -0.0010021, 0.00418737], mj_actuator_kp: "870.", mj_joint_damping: "100." }
l_panda_joint3_origin(l_panda_joint2): { pose: [0, -0.316, 0, 0.707107, 0.707107, 0, 0] }
l_panda_joint3(l_panda_joint3_origin): { joint: hingeZ, limits: [-2.8973, 2.8973], shape: mesh, mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/link3.h5>, mass: 0.546829, inertia: [0.00249312, -0.00055264, -0.000819764, 0.0029029, -0.000540692, 0.00252334], mj_actuator_kp: "870.", mj_joint_damping: "100." }
l_panda_joint4_origin(l_panda_joint3): { pose: [0.0825, 0, 0, 0.707107, 0.707107, 0, 0] }
l_panda_joint4(l_panda_joint4_origin): { joint: hingeZ, limits: [-3.0718, -0.0698], q: [-2], shape: mesh, mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/link4.h5>, mass: 0.552034, inertia: [0.0025711, 0.000847668, -0.000560078, 0.0025553, 0.000559278, 0.0029871], mj_actuator_kp: "870.", mj_joint_damping: "100." }
l_panda_joint5_origin(l_panda_joint4): { pose: [-0.0825, 0.384, 0, 0.707107, -0.707107, 0, 0] }
l_panda_joint5(l_panda_joint5_origin): { joint: hingeZ, limits: [-2.8973, 2.8973], shape: mesh, mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/link5.h5>, mass: 0.660949, inertia: [0.00852046, 2.33275e-06, -4.36368e-07, 0.00765386, -0.00177651, 0.00209358], mj_actuator_kp: "120.", mj_joint_damping: "10." }
l_panda_joint6_origin(l_panda_joint5): { pose: [0.707107, 0.707107, 0, 0] }
l_panda_joint6(l_panda_joint6_origin): { joint: hingeZ, limits: [0.5, 3], q: [2], shape: mesh, mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/link6.h5>, mass: 0.499428, inertia: [0.00118765, -3.51984e-05, 0.000162183, 0.00164862, 7.06891e-06, 0.00209456], mj_actuator_kp: "120.", mj_joint_damping: "10." }
l_panda_joint7_origin(l_panda_joint6): { pose: [0.088, 0, 0, 0.707107, 0.707107, 0, 0] }
l_panda_joint7(l_panda_joint7_origin): { joint: hingeZ, limits: [-2.8973, 2.8973], q: [-0.5], shape: mesh, mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/link7.h5>, mass: 0.508796, com: [0.00479288, 0.00293982, 0.110288], inertia: [0.0014038, -0.000585639, 3.48366e-05, 0.00139594, 5.49424e-05, 0.00158995], mj_actuator_kp: "120.", mj_joint_damping: "10." }
l_panda_joint8_origin(l_panda_joint7): { pose: [0, 0, 0.107] }
l_panda_joint8(l_panda_joint8_origin): {  }
l_panda_hand_joint_origin(l_panda_joint8): { pose: [0.92388, 0, 0, -0.382683] }
l_panda_hand_joint(l_panda_hand_joint_origin): { shape: mesh, mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/hand.h5> }
l_panda_finger_joint1_origin(l_panda_hand_joint): { pose: [0, 0, 0.0584] }
l_panda_finger_joint2_origin(l_panda_hand_joint): { pose: [0, 0, 0.0584] }
l_panda_finger_joint1(l_panda_finger_joint1_origin): { joint: transY, limits: [0, 0.04], q: [0.04], shape: mesh, mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/finger.h5>, mass: 0.0339598, inertia: [1.28954e-05, 3.94979e-10, 2.1346e-10, 1.25171e-05, 2.56044e-06, 3.22803e-06], mj_actuator_kp: "500.", mj_joint_damping: "100.", joint_active! }
l_panda_finger_joint2(l_panda_finger_joint2_origin): { joint: transY, joint_scale: -1, limits: [0, 0.04], mimic: "l_panda_finger_joint1", mass: 0.0339598, com: [-7.21322e-07, 0.0122672, 0.0270327], inertia: [1.28954e-05, 3.94979e-10, -2.1346e-10, 1.25171e-05, -2.56044e-06, 3.22803e-06], mj_actuator_kp: "500.", mj_joint_damping: "100." }
l_panda_rightfinger_0(l_panda_finger_joint2): { pose: [0, 0, 0, 1], shape: mesh, mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/finger.h5> }
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
targetSurface_tile_0: { pose: [0.681686, -0.397625, 0.642], shape: ssBox, size: [0.1, 0.1, 0.004, 0.001], color: [1, 0, 0] }
targetSurface_tile_1: { pose: [0.581686, -0.397625, 0.642], shape: ssBox, size: [0.1, 0.1, 0.004, 0.001], color: [1, 0, 1] }
targetSurface_tile_2: { pose: [0.481686, -0.397625, 0.642], shape: ssBox, size: [0.1, 0.1, 0.004, 0.001], color: [1, 0, 1] }
targetSurface_tile_3: { pose: [0.681686, -0.497625, 0.642], shape: ssBox, size: [0.1, 0.1, 0.004, 0.001], color: [1, 0, 1] }
targetSurface_tile_4: { pose: [0.681686, -0.297625, 0.642], shape: ssBox, size: [0.1, 0.1, 0.004, 0.001], color: [1, 0, 1] }
obj0_base: { pose: [-0.459911, 0.686172, 0.790009, -0.384832, 0.593212, 0.384846, 0.59321], mass: 1.4, com: [-0.0285714, -0.0571429, -6.14588e-17], inertia: [0.0394286, 0.000285714, -1.91749e-18, 0.0348571, 7.79386e-19, 0.0382857], multibody, multibody_fixedBase!, multibody_gravity }
obj0_cube0(obj0_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj0_joint1(obj0_cube0): {  }
obj0_cube1(obj0_joint1): { pose: [-0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [-0.1, 0, 0] }
obj0_joint2(obj0_cube1): {  }
obj0_cube2(obj0_joint2): { pose: [0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0, -0.1, 0] }
obj0_joint3(obj0_cube2): {  }
obj0_cube3(obj0_joint3): { pose: [0, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0, -0.2, 0] }
obj0_joint4(obj0_cube3): {  }
obj0_cube4(obj0_joint4): { pose: [0, 0.2, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0, 0, -0.1] }
obj0_joint5(obj0_cube4): {  }
obj0_cube5(obj0_joint5): { pose: [0, 0, 0.2], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0, 0, 0.1] }
obj0_joint6(obj0_cube5): {  }
obj0_cube6(obj0_joint6): { pose: [-0.1, -0.1, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [-0.1, -0.1, 0] }
obj1_base: { pose: [-0.00975996, 0.470493, 0.781433, 0.174742, 0.608045, 0.361042, 0.685124], mass: 1, com: [-0.06, -0.02, -0.06], inertia: [0.028, 0.0012, -0.0024, 0.0288, 0.0012, 0.024], multibody, multibody_fixedBase!, multibody_gravity }
obj1_cube0(obj1_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj1_joint1(obj1_cube0): {  }
obj1_cube1(obj1_joint1): { pose: [-0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [-0.1, 0, 0] }
obj1_joint2(obj1_cube1): {  }
obj1_cube2(obj1_joint2): { pose: [0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [0, -0.1, 0] }
obj1_joint3(obj1_cube2): {  }
obj1_cube3(obj1_joint3): { pose: [-0.1, 0.1, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [-0.1, 0, -0.1] }
obj1_joint4(obj1_cube3): {  }
obj1_cube4(obj1_joint4): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [-0.1, 0, -0.2] }
obj2_base: { pose: [0.514313, 0.286572, 0.690208, -0.813309, 0.00063768, 0.000333488, 0.581832], mass: 0.6, com: [-0.0333333, -0.0333333, 0], inertia: [0.0133333, 0.000666667, 0, 0.0133333, 0, 0.0146667], multibody, multibody_fixedBase!, multibody_gravity }
obj2_cube0(obj2_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj2_joint1(obj2_cube0): {  }
obj2_cube1(obj2_joint1): { pose: [-0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [-0.1, 0, 0] }
obj2_joint2(obj2_cube1): {  }
obj2_cube2(obj2_joint2): { pose: [0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, -0.1, 0] }
obj3_base: { pose: [-0.655832, 0.476794, 0.690034, -0.947155, -6.69882e-05, 0.000130292, 0.320775], mass: 0.8, com: [0, -0.05, 0], inertia: [0.018, 0.002, 0, 0.02, 0, 0.022], multibody, multibody_fixedBase!, multibody_gravity }
obj3_cube0(obj3_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj3_joint1(obj3_cube0): {  }
obj3_cube1(obj3_joint1): { pose: [0, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [0, -0.1, 0] }
obj3_joint2(obj3_cube1): {  }
obj3_cube2(obj3_joint2): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [0.1, -0.1, 0] }
obj3_joint3(obj3_cube2): {  }
obj3_cube3(obj3_joint3): { pose: [-0.2, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [-0.1, 0, 0] }
obj5_base: { pose: [0.248737, 0.451736, 0.690021, -0.0937686, -2.57755e-05, 7.39975e-05, 0.995594], mass: 0.8, com: [0.025, 3.16587e-17, 0], inertia: [0.02, 0.0175, 0.0215], multibody, multibody_fixedBase!, multibody_gravity }
obj5_cube0(obj5_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj5_joint1(obj5_cube0): {  }
obj5_cube1(obj5_joint1): { pose: [0, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, -0.1, 0] }
obj5_joint2(obj5_cube1): {  }
obj5_cube2(obj5_joint2): { pose: [0, 0.2, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, 0.1, 0] }
obj5_joint3(obj5_cube2): {  }
obj5_cube3(obj5_joint3): { pose: [0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0.1, 0, 0] }
obj6_base: { pose: [-0.632443, 0.629412, 0.718282, 0.208204, 0.0194811, -0.348225, 0.913789], mass: 0.4, com: [0, 0, 0.05], inertia: [0.009, 0.009, 0.008], multibody, multibody_fixedBase!, multibody_gravity }
obj6_cube0(obj6_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj6_joint1(obj6_cube0): {  }
obj6_cube1(obj6_joint1): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0, 0.1] }
obj9_base: { pose: [0.382949, -0.100679, 0.690031, 0.00563101, 0.00560543, -0.706857, -0.707312], mass: 0.2, inertia: [0.004, 0.004, 0.004], multibody, multibody_fixedBase!, multibody_gravity }
obj9_cube0(obj9_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj11_base: { pose: [-0.416302, 0.256828, 0.740375, 0.0826967, 0.174176, -0.685429, 0.702148], mass: 1, com: [5.84552e-18, 4.39345e-17, -0.1], inertia: [0.024, 0.028, 0.024], multibody, multibody_fixedBase!, multibody_gravity }
obj11_cube0(obj11_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj11_joint1(obj11_cube0): {  }
obj11_cube1(obj11_joint1): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0, 0, -0.1] }
obj11_joint2(obj11_cube1): {  }
obj11_cube2(obj11_joint2): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0.1, 0, -0.1] }
obj11_joint3(obj11_cube2): {  }
obj11_cube3(obj11_joint3): { pose: [-0.2, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [-0.1, 0, -0.1] }
obj11_joint4(obj11_cube3): {  }
obj11_cube4(obj11_joint4): { pose: [0.1, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0, 0, -0.2] }
obj15_base: { pose: [0.302974, 0.0581427, 0.690014, 0.694424, 0.133125, -0.6945, 0.133126], mass: 0.4, com: [0, 0, 0.05], inertia: [0.009, 0.009, 0.008], multibody, multibody_fixedBase!, multibody_gravity }
obj15_cube0(obj15_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj15_joint1(obj15_cube0): {  }
obj15_cube1(obj15_joint1): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0, 0, 0.1] }
obj16_base: { pose: [0.683205, 0.417252, 0.689999, 0.339478, 0.620262, -0.339545, 0.620273], mass: 0.4, com: [0, 0, 0.05], inertia: [0.009, 0.009, 0.008], multibody, multibody_fixedBase!, multibody_gravity }
obj16_cube0(obj16_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj16_joint1(obj16_cube0): {  }
obj16_cube1(obj16_joint1): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0, 0, 0.1] }
obj17_base: { pose: [-0.336338, -0.0119337, 0.690021, 0.425032, 0.424884, -0.565042, -0.565287], mass: 0.6, com: [-0.0333333, 0.0333333, 0], inertia: [0.0133333, -0.000666667, 0, 0.0133333, 0, 0.0146667], multibody, multibody_fixedBase!, multibody_gravity }
obj17_cube0(obj17_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj17_joint1(obj17_cube0): {  }
obj17_cube1(obj17_joint1): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 1], contact: 1, position: [0, 0.1, 0] }
obj17_joint2(obj17_cube1): {  }
obj17_cube2(obj17_joint2): { pose: [-0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 1], contact: 1, position: [-0.1, 0, 0] }
obj18_base: { pose: [0.56941, 0.0637199, 0.781426, 0.883607, 0.365998, 0.11175, 0.269808], mass: 1.4, com: [0.0285714, -0.0285714, -0.0428571], inertia: [0.0382857, 0.00485714, -0.00371429, 0.0422857, 0.00371429, 0.0457143], multibody, multibody_fixedBase!, multibody_gravity }
obj18_cube0(obj18_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj18_joint1(obj18_cube0): {  }
obj18_cube1(obj18_joint1): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, 0, -0.1] }
obj18_joint2(obj18_cube1): {  }
obj18_cube2(obj18_joint2): { pose: [0, -0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, -0.1, 0] }
obj18_joint3(obj18_cube2): {  }
obj18_cube3(obj18_joint3): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0.1, -0.1, 0] }
obj18_joint4(obj18_cube3): {  }
obj18_cube4(obj18_joint4): { pose: [-0.1, 0.2, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, 0.1, -0.1] }
obj18_joint5(obj18_cube4): {  }
obj18_cube5(obj18_joint5): { pose: [-0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [-0.1, 0, -0.1] }
obj18_joint6(obj18_cube5): {  }
obj18_cube6(obj18_joint6): { pose: [0.3, -0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0.2, -0.1, 0] }
obj19_base: { pose: [0.573099, 0.656785, 0.781403, -0.322025, 0.777593, -0.498983, 0.206554], mass: 0.6, com: [4.62593e-18, 0.0333333, 0.0333333], inertia: [0.0146667, -1.85037e-19, 9.25186e-20, 0.0133333, 0.000666667, 0.0133333], multibody, multibody_fixedBase!, multibody_gravity }
obj19_cube0(obj19_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj19_joint1(obj19_cube0): {  }
obj19_cube1(obj19_joint1): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0, 0.1] }
obj19_joint2(obj19_cube1): {  }
obj19_cube2(obj19_joint2): { pose: [0, 0.1, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0.1, 0] }
obj20_base: { pose: [-0.450521, -0.191916, 0.781504, 0.432675, 0.70159, 0.0885796, 0.559212], mass: 1, com: [-0.06, -0.02, -0.06], inertia: [0.028, 0.0012, -0.0024, 0.0288, 0.0012, 0.024], multibody, multibody_fixedBase!, multibody_gravity }
obj20_cube0(obj20_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj20_joint1(obj20_cube0): {  }
obj20_cube1(obj20_joint1): { pose: [-0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [-0.1, 0, 0] }
obj20_joint2(obj20_cube1): {  }
obj20_cube2(obj20_joint2): { pose: [0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [0, -0.1, 0] }
obj20_joint3(obj20_cube2): {  }
obj20_cube3(obj20_joint3): { pose: [-0.1, 0.1, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [-0.1, 0, -0.1] }
obj20_joint4(obj20_cube3): {  }
obj20_cube4(obj20_joint4): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [-0.1, 0, -0.2] }
obj21_base: { pose: [0.659562, 0.237879, 0.690033, -0.000311824, 0.976126, -0.217206, 0.000109341], mass: 0.2, inertia: [0.004, 0.004, 0.004], multibody, multibody_fixedBase!, multibody_gravity }
obj21_cube0(obj21_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj22_base: { pose: [-0.431459, 0.118316, 0.759515, -0.483705, -0.164621, -0.308027, 0.802527], mass: 0.8, com: [0.075, -1.56125e-17, 0.075], inertia: [0.0175, 1.14492e-18, -0.0015, 0.023, 3.1225e-19, 0.0215], multibody, multibody_fixedBase!, multibody_gravity }
obj22_cube0(obj22_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj22_joint1(obj22_cube0): {  }
obj22_cube1(obj22_joint1): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0, 0.1] }
obj22_joint2(obj22_cube1): {  }
obj22_cube2(obj22_joint2): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0, 0.1] }
obj22_joint3(obj22_cube2): {  }
obj22_cube3(obj22_joint3): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.2, 0, 0.1] }
obj23_base: { pose: [0.316939, 0.68216, 0.690014, -0.829006, 0.000113015, 4.19557e-05, 0.55924], mass: 0.4, com: [0.05, 3.46945e-18, 0], inertia: [0.008, 0.009, 0.009], multibody, multibody_fixedBase!, multibody_gravity }
obj23_cube0(obj23_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj23_joint1(obj23_cube0): {  }
obj23_cube1(obj23_joint1): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0, 0] }
obj24_base: { pose: [0.256472, 0.221196, 0.790079, -0.126806, -0.000288039, -3.05399e-05, 0.991928], mass: 1.2, com: [0.05, 0.0333333, -0.0333333], inertia: [0.0293333, -1.6263e-19, -2.1684e-19, 0.0296667, -0.00133333, 0.0296667], multibody, multibody_fixedBase!, multibody_gravity }
obj24_cube0(obj24_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj24_joint1(obj24_cube0): {  }
obj24_cube1(obj24_joint1): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0.1, 0] }
obj24_joint2(obj24_cube1): {  }
obj24_cube2(obj24_joint2): { pose: [0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0, 0] }
obj24_joint3(obj24_cube2): {  }
obj24_cube3(obj24_joint3): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0.1, 0] }
obj24_joint4(obj24_cube3): {  }
obj24_cube4(obj24_joint4): { pose: [0, -0.1, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0, -0.1] }
obj24_joint5(obj24_cube4): {  }
obj24_cube5(obj24_joint5): { pose: [-0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0, -0.1] }
obj26_base: { pose: [0.351605, 0.493571, 0.793731, -0.75987, 0.0255031, 0.0295866, 0.648901], mass: 0.6, com: [0, -0.0333333, 0.0333333], inertia: [0.0146667, 0, 0, 0.0133333, -0.000666667, 0.0133333], multibody, multibody_fixedBase!, multibody_gravity }
obj26_cube0(obj26_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj26_joint1(obj26_cube0): {  }
obj26_cube1(obj26_joint1): { pose: [0, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [0, -0.1, 0] }
obj26_joint2(obj26_cube1): {  }
obj26_cube2(obj26_joint2): { pose: [0, 0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [0, 0, 0.1] }
obj27_base: { pose: [-0.232242, 0.515319, 0.85178, -0.329247, 0.730637, -0.545217, 0.245978], mass: 1.8, com: [0.0111111, 2.50571e-17, 0.0555556], inertia: [0.0484444, 0.002, 0.00511111, 0.0542222, -0.002, 0.0577778], multibody, multibody_fixedBase!, multibody_gravity }
obj27_cube0(obj27_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj27_joint1(obj27_cube0): {  }
obj27_cube1(obj27_joint1): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0, 0] }
obj27_joint2(obj27_cube1): {  }
obj27_cube2(obj27_joint2): { pose: [-0.1, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0, 0.1] }
obj27_joint3(obj27_cube2): {  }
obj27_cube3(obj27_joint3): { pose: [0, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, -0.1, 0.1] }
obj27_joint4(obj27_cube3): {  }
obj27_cube4(obj27_joint4): { pose: [-0.1, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [-0.1, 0, 0.1] }
obj27_joint5(obj27_cube4): {  }
obj27_cube5(obj27_joint5): { pose: [0.1, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0.1, 0.1] }
obj27_joint6(obj27_cube5): {  }
obj27_cube6(obj27_joint6): { pose: [-0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [-0.1, 0.1, 0.1] }
obj27_joint7(obj27_cube6): {  }
obj27_cube7(obj27_joint7): { pose: [0.3, -0.1, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.2, 0, 0] }
obj27_joint8(obj27_cube7): {  }
obj27_cube8(obj27_joint8): { pose: [-0.2, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, -0.1, 0] }
obj31_base: { pose: [0.455311, 0.355652, 0.81905, -0.709128, 0.015204, 0.29085, 0.642115], mass: 1.6, com: [0.05, -0.0625, 0.0375], inertia: [0.0435, -0.003, 0.003, 0.04375, 0.00225, 0.04775], multibody, multibody_fixedBase!, multibody_gravity }
obj31_cube0(obj31_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj31_joint1(obj31_cube0): {  }
obj31_cube1(obj31_joint1): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0.1, 0, 0] }
obj31_joint2(obj31_cube1): {  }
obj31_cube2(obj31_joint2): { pose: [-0.1, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, 0, 0.1] }
obj31_joint3(obj31_cube2): {  }
obj31_cube3(obj31_joint3): { pose: [0, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, -0.1, 0.1] }
obj31_joint4(obj31_cube3): {  }
obj31_cube4(obj31_joint4): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, -0.1, 0] }
obj31_joint5(obj31_cube4): {  }
obj31_cube5(obj31_joint5): { pose: [0.2, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0.2, 0, 0] }
obj31_joint6(obj31_cube5): {  }
obj31_cube6(obj31_joint6): { pose: [-0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0.1, -0.1, 0] }
obj31_joint7(obj31_cube6): {  }
obj31_cube7(obj31_joint7): { pose: [-0.1, -0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, -0.2, 0.1] }
obj32_base: { pose: [-0.448942, 0.441756, 0.863309, -0.161235, 0.20312, -0.142511, 0.955216], mass: 1.4, com: [-0.0285714, -0.0714286, 0.0142857], inertia: [0.0365714, -0.00114286, -0.000571429, 0.0365714, -0.00142857, 0.0417143], multibody, multibody_fixedBase!, multibody_gravity }
obj32_cube0(obj32_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj32_joint1(obj32_cube0): {  }
obj32_cube1(obj32_joint1): { pose: [0, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [0, -0.1, 0] }
obj32_joint2(obj32_cube1): {  }
obj32_cube2(obj32_joint2): { pose: [-0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [-0.1, -0.1, 0] }
obj32_joint3(obj32_cube2): {  }
obj32_cube3(obj32_joint3): { pose: [0, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [-0.1, -0.2, 0] }
obj32_joint4(obj32_cube3): {  }
obj32_cube4(obj32_joint4): { pose: [0, 0.2, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [-0.1, 0, 0] }
obj32_joint5(obj32_cube4): {  }
obj32_cube5(obj32_joint5): { pose: [0.2, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [0.1, -0.1, 0] }
obj32_joint6(obj32_cube5): {  }
obj32_cube6(obj32_joint6): { pose: [-0.1, 0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [0, 0, 0.1] }
obj33_base: { pose: [-0.640833, 0.139117, 0.690697, -0.364301, -0.0063124, -0.00162139, 0.931258], mass: 0.4, com: [0, 0, 0.05], inertia: [0.009, 0.009, 0.008], multibody, multibody_fixedBase!, multibody_gravity }
obj33_cube0(obj33_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj33_joint1(obj33_cube0): {  }
obj33_cube1(obj33_joint1): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [0, 0, 0.1] }
obj34_base: { pose: [-0.2734, 0.345613, 0.90365, -0.0954289, 0.486073, -0.61975, -0.608717], mass: 0.2, inertia: [0.004, 0.004, 0.004], multibody, multibody_fixedBase!, multibody_gravity }
obj34_cube0(obj34_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj36_base: { pose: [0.296082, 0.339856, 0.97908, 0.592535, -0.545509, 0.270705, 0.527296], mass: 1.4, com: [-0.0142857, -0.0428571, -0.0714286], inertia: [0.0422857, 0.000857143, -0.000571429, 0.0325714, 0.000285714, 0.0411429], multibody, multibody_fixedBase!, multibody_gravity }
obj36_cube0(obj36_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj36_joint1(obj36_cube0): {  }
obj36_cube1(obj36_joint1): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [0, 0, -0.1] }
obj36_joint2(obj36_cube1): {  }
obj36_cube2(obj36_joint2): { pose: [0, -0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [0, -0.1, 0] }
obj36_joint3(obj36_cube2): {  }
obj36_cube3(obj36_joint3): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [0, -0.1, -0.1] }
obj36_joint4(obj36_cube3): {  }
obj36_cube4(obj36_joint4): { pose: [-0.1, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [-0.1, 0, -0.1] }
obj36_joint5(obj36_cube4): {  }
obj36_cube5(obj36_joint5): { pose: [0.1, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [0, 0.1, -0.1] }
obj36_joint6(obj36_cube5): {  }
obj36_cube6(obj36_joint6): { pose: [0, -0.3, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [0, -0.2, -0.1] }
obj41_base: { pose: [-0.302358, 0.24029, 0.80614, -0.456482, 0.328439, -0.070596, 0.823874], mass: 0.6, com: [0.0333333, -0.0333333, 0], inertia: [0.0133333, -0.000666667, 0, 0.0133333, 0, 0.0146667], multibody, multibody_fixedBase!, multibody_gravity }
obj41_cube0(obj41_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj41_joint1(obj41_cube0): {  }
obj41_cube1(obj41_joint1): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0, 0] }
obj41_joint2(obj41_cube1): {  }
obj41_cube2(obj41_joint2): { pose: [-0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, -0.1, 0] }
obj43_base: { pose: [-0.029536, 0.331492, 0.815423, -0.0269856, -0.568888, 0.777194, 0.267596], mass: 1.4, com: [0.0285714, -0.0285714, -0.0428571], inertia: [0.0382857, 0.00485714, -0.00371429, 0.0422857, 0.00371429, 0.0457143], multibody, multibody_fixedBase!, multibody_gravity }
obj43_cube0(obj43_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj43_joint1(obj43_cube0): {  }
obj43_cube1(obj43_joint1): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, 0, -0.1] }
obj43_joint2(obj43_cube1): {  }
obj43_cube2(obj43_joint2): { pose: [0, -0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, -0.1, 0] }
obj43_joint3(obj43_cube2): {  }
obj43_cube3(obj43_joint3): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0.1, -0.1, 0] }
obj43_joint4(obj43_cube3): {  }
obj43_cube4(obj43_joint4): { pose: [-0.1, 0.2, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, 0.1, -0.1] }
obj43_joint5(obj43_cube4): {  }
obj43_cube5(obj43_joint5): { pose: [-0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [-0.1, 0, -0.1] }
obj43_joint6(obj43_cube5): {  }
obj43_cube6(obj43_joint6): { pose: [0.3, -0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0.2, -0.1, 0] }
obj44_base: { pose: [-0.627801, 0.368083, 0.93726, -0.593211, 0.29656, 0.0428238, 0.747208], mass: 1.6, com: [0.075, 0.0625, -0.0125], inertia: [0.0415, -0.0025, -0.0015, 0.04475, -0.00125, 0.04275], multibody, multibody_fixedBase!, multibody_gravity }
obj44_cube0(obj44_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj44_joint1(obj44_cube0): {  }
obj44_cube1(obj44_joint1): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [0.1, 0, 0] }
obj44_joint2(obj44_cube1): {  }
obj44_cube2(obj44_joint2): { pose: [-0.1, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [0, 0.1, 0] }
obj44_joint3(obj44_cube2): {  }
obj44_cube3(obj44_joint3): { pose: [0, -0.1, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [0, 0, -0.1] }
obj44_joint4(obj44_cube3): {  }
obj44_cube4(obj44_joint4): { pose: [0.1, 0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [0.1, 0.1, 0] }
obj44_joint5(obj44_cube4): {  }
obj44_cube5(obj44_joint5): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [0.1, 0.1, -0.1] }
obj44_joint6(obj44_cube5): {  }
obj44_cube6(obj44_joint6): { pose: [0.1, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [0.2, 0.1, 0] }
obj44_joint7(obj44_cube6): {  }
obj44_cube7(obj44_joint7): { pose: [-0.1, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [0.1, 0.1, 0.1] }
obj45_base: { pose: [0.291727, 0.509688, 0.992264, -0.995781, 0.035857, 0.0196839, 0.0821389], mass: 0.4, com: [0.05, -5.20417e-18, 0], inertia: [0.008, 0.009, 0.009], multibody, multibody_fixedBase!, multibody_gravity }
obj45_cube0(obj45_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj45_joint1(obj45_cube0): {  }
obj45_cube1(obj45_joint1): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0, 0] }
obj46_base: { pose: [-0.167113, 0.165732, 0.719681, -0.564218, 0.733525, -0.260198, -0.275492], mass: 0.4, com: [-1.04083e-17, -0.05, 0], inertia: [0.009, 0.008, 0.009], multibody, multibody_fixedBase!, multibody_gravity }
obj46_cube0(obj46_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj46_joint1(obj46_cube0): {  }
obj46_cube1(obj46_joint1): { pose: [0, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 1], contact: 1, position: [0, -0.1, 0] }