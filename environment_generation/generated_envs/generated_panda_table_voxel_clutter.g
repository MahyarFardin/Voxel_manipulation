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
obj0_base: { pose: [-0.588813, -0.604771, 0.690003, -0.731682, -7.55042e-05, -2.54363e-05, 0.681646], mass: 1.6, com: [0.0875, 0.05, 0.0375], inertia: [0.04775, -0.003, 0.00525, 0.0495, 0.003, 0.04975], multibody, multibody_fixedBase!, multibody_gravity }
obj0_cube0(obj0_base): { shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1 }
obj0_joint1(obj0_cube0): {  }
obj0_cube1(obj0_joint1): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [0.1, 0, 0] }
obj0_joint2(obj0_cube1): {  }
obj0_cube2(obj0_joint2): { pose: [-0.1, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [0, 0, 0.1] }
obj0_joint3(obj0_cube2): {  }
obj0_cube3(obj0_joint3): { pose: [0.2, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [0.2, 0, 0] }
obj0_joint4(obj0_cube3): {  }
obj0_cube4(obj0_joint4): { pose: [-0.1, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [0.1, 0.1, 0] }
obj0_joint5(obj0_cube4): {  }
obj0_cube5(obj0_joint5): { pose: [-0.1, -0.1, 0.2], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [0, 0, 0.2] }
obj0_joint6(obj0_cube5): {  }
obj0_cube6(obj0_joint6): { pose: [0.1, 0.2, -0.2], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [0.1, 0.2, 0] }
obj0_joint7(obj0_cube6): {  }
obj0_cube7(obj0_joint7): { pose: [0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [0.2, 0.1, 0] }
obj1_base: { pose: [0.549404, -0.504391, 0.690018, 0.83871, -3.17748e-05, -1.85262e-05, 0.544578], mass: 1.6, com: [0.1, 0.0875, 0], inertia: [0.04175, 0.044, 0.05375], multibody, multibody_fixedBase!, multibody_gravity }
obj1_cube0(obj1_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1 }
obj1_joint1(obj1_cube0): {  }
obj1_cube1(obj1_joint1): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.1, 0, 0] }
obj1_joint2(obj1_cube1): {  }
obj1_cube2(obj1_joint2): { pose: [-0.1, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0.1, 0] }
obj1_joint3(obj1_cube2): {  }
obj1_cube3(obj1_joint3): { pose: [0.2, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.2, 0, 0] }
obj1_joint4(obj1_cube3): {  }
obj1_cube4(obj1_joint4): { pose: [-0.2, 0.2, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0.2, 0] }
obj1_joint5(obj1_cube4): {  }
obj1_cube5(obj1_joint5): { pose: [0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.1, 0.1, 0] }
obj1_joint6(obj1_cube5): {  }
obj1_cube6(obj1_joint6): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.2, 0.1, 0] }
obj1_joint7(obj1_cube6): {  }
obj1_cube7(obj1_joint7): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.2, 0.2, 0] }
obj2_base: { pose: [-0.635751, 0.536523, 0.690002, -0.991821, -1.72406e-05, 3.98643e-05, 0.127637], mass: 1.6, com: [0.05, 0.025, 0.0875], inertia: [0.04475, -1.0842e-19, -0.001, 0.04575, 0.0015, 0.039], multibody, multibody_fixedBase!, multibody_gravity }
obj2_cube0(obj2_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1 }
obj2_joint1(obj2_cube0): {  }
obj2_cube1(obj2_joint1): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0.1, 0, 0] }
obj2_joint2(obj2_cube1): {  }
obj2_cube2(obj2_joint2): { pose: [-0.1, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0, 0, 0.1] }
obj2_joint3(obj2_cube2): {  }
obj2_cube3(obj2_joint3): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0.1, 0, 0.1] }
obj2_joint4(obj2_cube3): {  }
obj2_cube4(obj2_joint4): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0.1, 0.1, 0.1] }
obj2_joint5(obj2_cube4): {  }
obj2_cube5(obj2_joint5): { pose: [-0.1, -0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0, 0, 0.2] }
obj2_joint6(obj2_cube5): {  }
obj2_cube6(obj2_joint6): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0.1, 0, 0.2] }
obj2_joint7(obj2_cube6): {  }
obj2_cube7(obj2_joint7): { pose: [-0.1, 0.1, -0.2], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0, 0.1, 0] }
obj3_base: { pose: [-0.430701, -0.255231, 0.690056, 0.585914, 5.64009e-06, -9.59337e-05, 0.810373], mass: 1.6, com: [0.05, 0.1, 0.0125], inertia: [0.04975, 0.002, 0.001, 0.04175, 0.002, 0.056], multibody, multibody_fixedBase!, multibody_gravity }
obj3_cube0(obj3_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1 }
obj3_joint1(obj3_cube0): {  }
obj3_cube1(obj3_joint1): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0.1, 0] }
obj3_joint2(obj3_cube1): {  }
obj3_cube2(obj3_joint2): { pose: [0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.1, 0, 0] }
obj3_joint3(obj3_cube2): {  }
obj3_cube3(obj3_joint3): { pose: [-0.1, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0, 0.1] }
obj3_joint4(obj3_cube3): {  }
obj3_cube4(obj3_joint4): { pose: [0, 0.2, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0.2, 0] }
obj3_joint5(obj3_cube4): {  }
obj3_cube5(obj3_joint5): { pose: [0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.1, 0.1, 0] }
obj3_joint6(obj3_cube5): {  }
obj3_cube6(obj3_joint6): { pose: [-0.1, 0.2, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0.3, 0] }
obj3_joint7(obj3_cube6): {  }
obj3_cube7(obj3_joint7): { pose: [0.2, -0.2, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.2, 0.1, 0] }
obj4_base: { pose: [-0.573707, 0.181364, 0.690046, 0.911318, -8.1161e-05, -0.000142045, 0.411704], mass: 1.6, com: [0.025, 0.1125, 0.1375], inertia: [0.0535, 0.0005, -0.0045, 0.05075, -0.00325, 0.04075], multibody, multibody_fixedBase!, multibody_gravity }
obj4_cube0(obj4_base): { shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1 }
obj4_joint1(obj4_cube0): {  }
obj4_cube1(obj4_joint1): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, 0.1, 0] }
obj4_joint2(obj4_cube1): {  }
obj4_cube2(obj4_joint2): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, 0.1, 0.1] }
obj4_joint3(obj4_cube2): {  }
obj4_cube3(obj4_joint3): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, 0.1, 0.2] }
obj4_joint4(obj4_cube3): {  }
obj4_cube4(obj4_joint4): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0.1, 0.1, 0.2] }
obj4_joint5(obj4_cube4): {  }
obj4_cube5(obj4_joint5): { pose: [-0.1, 0.1, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, 0.2, 0.1] }
obj4_joint6(obj4_cube5): {  }
obj4_cube6(obj4_joint6): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, 0.2, 0.2] }
obj4_joint7(obj4_cube6): {  }
obj4_cube7(obj4_joint7): { pose: [0.1, -0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0.1, 0.1, 0.3] }
obj6_base: { pose: [-0.545408, -0.216853, 0.790182, 0.100608, -0.0006655, -9.79732e-05, 0.994926], mass: 1.6, com: [0.1, 0.0875, 0], inertia: [0.04175, 0.044, 0.05375], multibody, multibody_fixedBase!, multibody_gravity }
obj6_cube0(obj6_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1 }
obj6_joint1(obj6_cube0): {  }
obj6_cube1(obj6_joint1): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.1, 0, 0] }
obj6_joint2(obj6_cube1): {  }
obj6_cube2(obj6_joint2): { pose: [-0.1, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0.1, 0] }
obj6_joint3(obj6_cube2): {  }
obj6_cube3(obj6_joint3): { pose: [0.2, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.2, 0, 0] }
obj6_joint4(obj6_cube3): {  }
obj6_cube4(obj6_joint4): { pose: [-0.2, 0.2, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0.2, 0] }
obj6_joint5(obj6_cube4): {  }
obj6_cube5(obj6_joint5): { pose: [0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.1, 0.1, 0] }
obj6_joint6(obj6_cube5): {  }
obj6_cube6(obj6_joint6): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.2, 0.1, 0] }
obj6_joint7(obj6_cube6): {  }
obj6_cube7(obj6_joint7): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.2, 0.2, 0] }
goal_7_base: { pose: [-0.267287, 0.431446, 0.697858, 0.811681, 0.0701519, 0.0500941, 0.577705], mass: 1.6, com: [0.1, 0.0875, 0.0375], inertia: [0.0455, -0.006, 0.002, 0.04375, -0.00075, 0.04975], multibody, multibody_fixedBase!, multibody_gravity }
goal_7_cube0(goal_7_base): { shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1 }
goal_7_joint1(goal_7_cube0): {  }
goal_7_cube1(goal_7_joint1): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0.1, 0, 0] }
goal_7_joint2(goal_7_cube1): {  }
goal_7_cube2(goal_7_joint2): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0.1, 0.1, 0] }
goal_7_joint3(goal_7_cube2): {  }
goal_7_cube3(goal_7_joint3): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0.2, 0.1, 0] }
goal_7_joint4(goal_7_cube3): {  }
goal_7_cube4(goal_7_joint4): { pose: [-0.2, -0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0, 0, 0.1] }
goal_7_joint5(goal_7_cube4): {  }
goal_7_cube5(goal_7_joint5): { pose: [0.1, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0.1, 0.1, 0.1] }
goal_7_joint6(goal_7_cube5): {  }
goal_7_cube6(goal_7_joint6): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0.1, 0.2, 0.1] }
goal_7_joint7(goal_7_cube6): {  }
goal_7_cube7(goal_7_joint7): { pose: [0.1, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1], contact: 1, position: [0.2, 0.2, 0] }
obj8_base: { pose: [0.545929, -0.443922, 0.790169, 0.788847, -0.00031215, -0.000383571, 0.61459], mass: 1.6, com: [0.05, 0.1, 0.0125], inertia: [0.04975, 0.002, 0.001, 0.04175, 0.002, 0.056], multibody, multibody_fixedBase!, multibody_gravity }
obj8_cube0(obj8_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1 }
obj8_joint1(obj8_cube0): {  }
obj8_cube1(obj8_joint1): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0.1, 0] }
obj8_joint2(obj8_cube1): {  }
obj8_cube2(obj8_joint2): { pose: [0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.1, 0, 0] }
obj8_joint3(obj8_cube2): {  }
obj8_cube3(obj8_joint3): { pose: [-0.1, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0, 0.1] }
obj8_joint4(obj8_cube3): {  }
obj8_cube4(obj8_joint4): { pose: [0, 0.2, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0.2, 0] }
obj8_joint5(obj8_cube4): {  }
obj8_cube5(obj8_joint5): { pose: [0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.1, 0.1, 0] }
obj8_joint6(obj8_cube5): {  }
obj8_cube6(obj8_joint6): { pose: [-0.1, 0.2, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0.3, 0] }
obj8_joint7(obj8_cube6): {  }
obj8_cube7(obj8_joint7): { pose: [0.2, -0.2, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.2, 0.1, 0] }
goal_pose_9_base: { pose: [0.398828, 0.406184, 0.690058, -0.149085, -0.000126839, 3.71668e-05, 0.988824], mass: 1.6, com: [0.1, 0.0875, 0.0375], inertia: [0.0455, -0.006, 0.002, 0.04375, -0.00075, 0.04975], multibody, multibody_fixedBase!, multibody_gravity }
goal_pose_9_cube0(goal_pose_9_base): { shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1, 0.9] }
goal_pose_9_joint1(goal_pose_9_cube0): {  }
goal_pose_9_cube1(goal_pose_9_joint1): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1, 0.9], position: [0.1, 0, 0] }
goal_pose_9_joint2(goal_pose_9_cube1): {  }
goal_pose_9_cube2(goal_pose_9_joint2): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1, 0.9], position: [0.1, 0.1, 0] }
goal_pose_9_joint3(goal_pose_9_cube2): {  }
goal_pose_9_cube3(goal_pose_9_joint3): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1, 0.9], position: [0.2, 0.1, 0] }
goal_pose_9_joint4(goal_pose_9_cube3): {  }
goal_pose_9_cube4(goal_pose_9_joint4): { pose: [-0.2, -0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1, 0.9], position: [0, 0, 0.1] }
goal_pose_9_joint5(goal_pose_9_cube4): {  }
goal_pose_9_cube5(goal_pose_9_joint5): { pose: [0.1, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1, 0.9], position: [0.1, 0.1, 0.1] }
goal_pose_9_joint6(goal_pose_9_cube5): {  }
goal_pose_9_cube6(goal_pose_9_joint6): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1, 0.9], position: [0.1, 0.2, 0.1] }
goal_pose_9_joint7(goal_pose_9_cube6): {  }
goal_pose_9_cube7(goal_pose_9_joint7): { pose: [0.1, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 1, 0.9], position: [0.2, 0.2, 0] }