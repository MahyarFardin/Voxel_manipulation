world: {  }
table(world): { pose: [0, 0, 0.6], shape: ssBox, size: [1.6, 1.6, 0.08, 0.02], color: [0.3, 0.3, 0.3], contact: 1, logical: {  }, friction: 0.1 }
l_panda_base(table): { joint: rigid, mass: 0.692293, com: [-0.0330523, -0.00282329, 0.0478782], inertia: [0.00324422, -2.42323e-05, -0.000502638, 0.00383394, 9.03806e-06, 0.00410047], multibody, multibody_gravity! }
l_panda_link0(l_panda_base): { shape: mesh, mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/link0.h5> }
l_panda_joint1_origin(l_panda_link0): { pose: [0, 0, 0.333] }
l_panda_joint1(l_panda_joint1_origin): { joint: hingeZ, limits: [-2.8973, 2.8973], q: [-0.000142626], shape: mesh, color: [1, 1, 1, 1], mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/link1.h5>, mass: 0.54041, inertia: [0.00456315, -4.845e-08, 2.96516e-08, 0.00410729, 0.000986596, 0.00188739], mj_actuator_kp: "870.", mj_joint_damping: "100." }
l_panda_joint2_origin(l_panda_joint1): { pose: [0.707107, -0.707107, 0, 0] }
l_panda_joint2(l_panda_joint2_origin): { joint: hingeZ, limits: [-1.7628, 1.7628], q: [-0.5], shape: mesh, color: [1, 1, 1, 1], mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/link2.h5>, mass: 0.5439, inertia: [0.00464633, 9.6386e-08, 7.04772e-08, 0.00190105, -0.0010021, 0.00418737], mj_actuator_kp: "870.", mj_joint_damping: "100." }
l_panda_joint3_origin(l_panda_joint2): { pose: [0, -0.316, 0, 0.707107, 0.707107, 0, 0] }
l_panda_joint3(l_panda_joint3_origin): { joint: hingeZ, limits: [-2.8973, 2.8973], q: [2.03593e-06], shape: mesh, mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/link3.h5>, mass: 0.546829, inertia: [0.00249312, -0.00055264, -0.000819764, 0.0029029, -0.000540692, 0.00252334], mj_actuator_kp: "870.", mj_joint_damping: "100." }
l_panda_joint4_origin(l_panda_joint3): { pose: [0.0825, 0, 0, 0.707107, 0.707107, 0, 0] }
l_panda_joint4(l_panda_joint4_origin): { joint: hingeZ, limits: [-3.0718, -0.0698], q: [-2], shape: mesh, mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/link4.h5>, mass: 0.552034, inertia: [0.0025711, 0.000847668, -0.000560078, 0.0025553, 0.000559278, 0.0029871], mj_actuator_kp: "870.", mj_joint_damping: "100." }
l_panda_joint5_origin(l_panda_joint4): { pose: [-0.0825, 0.384, 0, 0.707107, -0.707107, 0, 0] }
l_panda_joint5(l_panda_joint5_origin): { joint: hingeZ, limits: [-2.8973, 2.8973], q: [-1.5546e-07], shape: mesh, mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/link5.h5>, mass: 0.660949, inertia: [0.00852046, 2.33275e-06, -4.36368e-07, 0.00765386, -0.00177651, 0.00209358], mj_actuator_kp: "120.", mj_joint_damping: "10." }
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
l_panda_finger_joint1(l_panda_finger_joint1_origin): { joint: transY, limits: [0, 0.04], q: [0.0399995], shape: mesh, mesh: </home/hakan/.venvs/robotic_env/lib/python3.12/site-packages/robotic/rai-robotModels/panda/meshes/finger.h5>, mass: 0.0339598, inertia: [1.28954e-05, 3.94979e-10, 2.1346e-10, 1.25171e-05, 2.56044e-06, 3.22803e-06], mj_actuator_kp: "500.", mj_joint_damping: "100.", joint_active! }
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
targetSurface_tile_0: { pose: [-0.0983433, -0.585823, 0.642], shape: ssBox, size: [0.1, 0.1, 0.004, 0.001], color: [1, 0, 0] }
targetSurface_tile_1: { pose: [-0.0983433, -0.485823, 0.642], shape: ssBox, size: [0.1, 0.1, 0.004, 0.001], color: [1, 1, 1] }
obj0_base: { pose: [0.157771, -0.632731, 0.689999, 0.459566, 9.12842e-05, 8.84537e-05, 0.888144], mass: 0.6, com: [2.31296e-18, -0.0333333, 0.0333333], inertia: [0.0146667, 9.25186e-20, 4.62593e-20, 0.0133333, -0.000666667, 0.0133333], multibody, multibody_fixedBase!, multibody_gravity }
obj0_cube0(obj0_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj0_joint1(obj0_cube0): {  }
obj0_cube1(obj0_joint1): { pose: [0, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [0, -0.1, 0] }
obj0_joint2(obj0_cube1): {  }
obj0_cube2(obj0_joint2): { pose: [0, 0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [0, 0, 0.1] }
obj1_base: { pose: [-0.725544, 0.662521, 0.690013, 0.129216, -0.695173, 0.129299, 0.695212], mass: 1.6, com: [-0.0375, -0.075, -0.0375], inertia: [0.05075, -0.0015, -0.00175, 0.0515, 0.0005, 0.03875], multibody, multibody_fixedBase!, multibody_gravity }
obj1_cube0(obj1_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj1_joint1(obj1_cube0): {  }
obj1_cube1(obj1_joint1): { pose: [0, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, -0.1, 0] }
obj1_joint2(obj1_cube1): {  }
obj1_cube2(obj1_joint2): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, -0.1, -0.1] }
obj1_joint3(obj1_cube2): {  }
obj1_cube3(obj1_joint3): { pose: [-0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [-0.1, -0.1, -0.1] }
obj1_joint4(obj1_cube3): {  }
obj1_cube4(obj1_joint4): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [-0.1, -0.1, -0.2] }
obj1_joint5(obj1_cube4): {  }
obj1_cube5(obj1_joint5): { pose: [0.1, 0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0, -0.1] }
obj1_joint6(obj1_cube5): {  }
obj1_cube6(obj1_joint6): { pose: [0, -0.1, 0.2], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, -0.1, 0.1] }
obj1_joint7(obj1_cube6): {  }
obj1_cube7(obj1_joint7): { pose: [-0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [-0.1, -0.1, 0.1] }
obj2_base: { pose: [-0.589005, 0.0565262, 0.690041, 0.78242, -0.0002432, -0.000270331, 0.622751], mass: 0.2, inertia: [0.004, 0.004, 0.004], multibody, multibody_fixedBase!, multibody_gravity }
obj2_cube0(obj2_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj3_base: { pose: [0.225504, 0.0957815, 0.938346, -0.222927, -0.336824, -0.0824352, 0.911075], mass: 1.8, com: [0.0222222, 0.0222222, -0.122222], inertia: [0.0702222, 0.000888889, 0.00111111, 0.0702222, 0.00111111, 0.0422222], multibody, multibody_fixedBase!, multibody_gravity }
obj3_cube0(obj3_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj3_joint1(obj3_cube0): {  }
obj3_cube1(obj3_joint1): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0, -0.1] }
obj3_joint2(obj3_cube1): {  }
obj3_cube2(obj3_joint2): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0, -0.1] }
obj3_joint3(obj3_cube2): {  }
obj3_cube3(obj3_joint3): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0, -0.2] }
obj3_joint4(obj3_cube3): {  }
obj3_cube4(obj3_joint4): { pose: [-0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0, -0.2] }
obj3_joint5(obj3_cube4): {  }
obj3_cube5(obj3_joint5): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0, -0.3] }
obj3_joint6(obj3_cube5): {  }
obj3_cube6(obj3_joint6): { pose: [0, 0, 0.4], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0, 0.1] }
obj3_joint7(obj3_cube6): {  }
obj3_cube7(obj3_joint7): { pose: [0, 0.1, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0.1, 0] }
obj3_joint8(obj3_cube7): {  }
obj3_cube8(obj3_joint8): { pose: [0, 0, -0.3], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0.1, -0.3] }
obj4_base: { pose: [0.683665, 0.418083, 0.69003, 0.766181, -0.000208245, -0.000239373, 0.642625], mass: 0.4, com: [0, 0, 0.05], inertia: [0.009, 0.009, 0.008], multibody, multibody_fixedBase!, multibody_gravity }
obj4_cube0(obj4_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj4_joint1(obj4_cube0): {  }
obj4_cube1(obj4_joint1): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [0, 0, 0.1] }
obj5_base: { pose: [0.345405, -0.254394, 0.689993, -0.0451223, -7.63534e-05, -1.66168e-05, 0.998982], mass: 0.6, com: [1.73472e-17, -0.0666667, 0.0333333], inertia: [0.0146667, 3.46945e-19, -1.73472e-19, 0.0133333, 0.000666667, 0.0133333], multibody, multibody_fixedBase!, multibody_gravity }
obj5_cube0(obj5_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj5_joint1(obj5_cube0): {  }
obj5_cube1(obj5_joint1): { pose: [0, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [0, -0.1, 0] }
obj5_joint2(obj5_cube1): {  }
obj5_cube2(obj5_joint2): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [0, -0.1, 0.1] }
obj7_base: { pose: [-0.311146, 0.210637, 0.69003, 0.0262892, 4.21051e-05, -0.000315274, 0.999654], mass: 0.4, com: [0, 0, 0.05], inertia: [0.009, 0.009, 0.008], multibody, multibody_fixedBase!, multibody_gravity }
obj7_cube0(obj7_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj7_joint1(obj7_cube0): {  }
obj7_cube1(obj7_joint1): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [0, 0, 0.1] }
obj8_base: { pose: [0.689645, -0.595004, 0.690009, 0.701076, 0.701086, 0.0921402, 0.0920902], mass: 1.8, com: [0.0222222, 0.0222222, -0.122222], inertia: [0.0702222, 0.000888889, 0.00111111, 0.0702222, 0.00111111, 0.0422222], multibody, multibody_fixedBase!, multibody_gravity }
obj8_cube0(obj8_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj8_joint1(obj8_cube0): {  }
obj8_cube1(obj8_joint1): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0, -0.1] }
obj8_joint2(obj8_cube1): {  }
obj8_cube2(obj8_joint2): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0, -0.1] }
obj8_joint3(obj8_cube2): {  }
obj8_cube3(obj8_joint3): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0, -0.2] }
obj8_joint4(obj8_cube3): {  }
obj8_cube4(obj8_joint4): { pose: [-0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0, -0.2] }
obj8_joint5(obj8_cube4): {  }
obj8_cube5(obj8_joint5): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0, -0.3] }
obj8_joint6(obj8_cube5): {  }
obj8_cube6(obj8_joint6): { pose: [0, 0, 0.4], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0, 0.1] }
obj8_joint7(obj8_cube6): {  }
obj8_cube7(obj8_joint7): { pose: [0, 0.1, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0.1, 0] }
obj8_joint8(obj8_cube7): {  }
obj8_cube8(obj8_joint8): { pose: [0, 0, -0.3], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0.1, -0.3] }
obj9_base: { pose: [-0.332092, -0.442125, 0.790003, 0.998401, 3.34401e-05, -0.000105048, 0.0565249], mass: 1.8, com: [0.0333333, 0.0666667, -0.0222222], inertia: [0.0511111, -1.0842e-19, 0.000666667, 0.0471111, 0.00133333, 0.048], multibody, multibody_fixedBase!, multibody_gravity }
obj9_cube0(obj9_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj9_joint1(obj9_cube0): {  }
obj9_cube1(obj9_joint1): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0.1, 0] }
obj9_joint2(obj9_cube1): {  }
obj9_cube2(obj9_joint2): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0.1, 0] }
obj9_joint3(obj9_cube2): {  }
obj9_cube3(obj9_joint3): { pose: [0, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0, 0] }
obj9_joint4(obj9_cube3): {  }
obj9_cube4(obj9_joint4): { pose: [-0.1, 0.2, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0.2, 0] }
obj9_joint5(obj9_cube4): {  }
obj9_cube5(obj9_joint5): { pose: [0.1, -0.1, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0.1, -0.1] }
obj9_joint6(obj9_cube5): {  }
obj9_cube6(obj9_joint6): { pose: [-0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0.1, -0.1] }
obj9_joint7(obj9_cube6): {  }
obj9_cube7(obj9_joint7): { pose: [0, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0, -0.1] }
obj9_joint8(obj9_cube7): {  }
obj9_cube8(obj9_joint8): { pose: [0, 0, 0.2], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0, 0.1] }
obj10_base: { pose: [-0.473089, -0.396016, 0.852207, 0.38016, 0.918358, 0.101568, 0.0422068], mass: 1.8, com: [-0.0888889, -0.0222222, 0.0888889], inertia: [0.0528889, -0.00244444, 0.00177778, 0.0515556, -0.00355556, 0.0488889], multibody, multibody_fixedBase!, multibody_gravity }
obj10_cube0(obj10_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj10_joint1(obj10_cube0): {  }
obj10_cube1(obj10_joint1): { pose: [-0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [-0.1, 0, 0] }
obj10_joint2(obj10_cube1): {  }
obj10_cube2(obj10_joint2): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [-0.1, 0, 0.1] }
obj10_joint3(obj10_cube2): {  }
obj10_cube3(obj10_joint3): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [0, 0, 0.1] }
obj10_joint4(obj10_cube3): {  }
obj10_cube4(obj10_joint4): { pose: [-0.1, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [-0.1, 0, 0.2] }
obj10_joint5(obj10_cube4): {  }
obj10_cube5(obj10_joint5): { pose: [0, -0.1, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [-0.1, -0.1, 0.1] }
obj10_joint6(obj10_cube5): {  }
obj10_cube6(obj10_joint6): { pose: [0, 0.2, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [-0.1, 0.1, 0.2] }
obj10_joint7(obj10_cube6): {  }
obj10_cube7(obj10_joint7): { pose: [0, -0.2, -0.2], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [-0.1, -0.1, 0] }
obj10_joint8(obj10_cube7): {  }
obj10_cube8(obj10_joint8): { pose: [-0.1, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 1], contact: 1, position: [-0.2, -0.1, 0.1] }
obj12_base: { pose: [-0.0904992, 0.300136, 0.749025, -0.762351, 0.230492, -0.588112, 0.140776], mass: 1.4, com: [0.0142857, 7.43453e-18, 0.0428571], inertia: [0.0474286, 0.002, 0.000857143, 0.0411429, -0.006, 0.0377143], multibody, multibody_fixedBase!, multibody_gravity }
obj12_cube0(obj12_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj12_joint1(obj12_cube0): {  }
obj12_cube1(obj12_joint1): { pose: [0, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, -0.1, 0] }
obj12_joint2(obj12_cube1): {  }
obj12_cube2(obj12_joint2): { pose: [0, 0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0, 0.1] }
obj12_joint3(obj12_cube2): {  }
obj12_cube3(obj12_joint3): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0.1, 0.1] }
obj12_joint4(obj12_cube3): {  }
obj12_cube4(obj12_joint4): { pose: [0, -0.1, -0.2], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0, -0.1] }
obj12_joint5(obj12_cube4): {  }
obj12_cube5(obj12_joint5): { pose: [0, 0.1, 0.3], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0.1, 0.2] }
obj12_joint6(obj12_cube5): {  }
obj12_cube6(obj12_joint6): { pose: [0.1, -0.2, -0.2], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.1, -0.1, 0] }
obj13_base: { pose: [0.422605, 0.474598, 0.690006, -0.998776, 3.10093e-05, 1.26809e-05, 0.0494669], mass: 1.2, com: [-0.0833333, -0.05, 0.0166667], inertia: [0.0326667, -0.005, 0.00233333, 0.0353333, 0.001, 0.0406667], multibody, multibody_fixedBase!, multibody_gravity }
obj13_cube0(obj13_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj13_joint1(obj13_cube0): {  }
obj13_cube1(obj13_joint1): { pose: [0, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0, -0.1, 0] }
obj13_joint2(obj13_cube1): {  }
obj13_cube2(obj13_joint2): { pose: [-0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [-0.1, -0.1, 0] }
obj13_joint3(obj13_cube2): {  }
obj13_cube3(obj13_joint3): { pose: [-0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [-0.2, -0.1, 0] }
obj13_joint4(obj13_cube3): {  }
obj13_cube4(obj13_joint4): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [-0.2, -0.1, 0.1] }
obj13_joint5(obj13_cube4): {  }
obj13_cube5(obj13_joint5): { pose: [0.2, 0.2, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 1], contact: 1, position: [0, 0.1, 0] }
obj14_base: { pose: [-0.480836, -0.634876, 0.914818, -0.0036785, -0.451951, -0.361557, 0.815477], mass: 1.4, com: [-0.0142857, -0.0428571, -0.0714286], inertia: [0.0422857, 0.000857143, -0.000571429, 0.0325714, 0.000285714, 0.0411429], multibody, multibody_fixedBase!, multibody_gravity }
obj14_cube0(obj14_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj14_joint1(obj14_cube0): {  }
obj14_cube1(obj14_joint1): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [0, 0, -0.1] }
obj14_joint2(obj14_cube1): {  }
obj14_cube2(obj14_joint2): { pose: [0, -0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [0, -0.1, 0] }
obj14_joint3(obj14_cube2): {  }
obj14_cube3(obj14_joint3): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [0, -0.1, -0.1] }
obj14_joint4(obj14_cube3): {  }
obj14_cube4(obj14_joint4): { pose: [-0.1, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [-0.1, 0, -0.1] }
obj14_joint5(obj14_cube4): {  }
obj14_cube5(obj14_joint5): { pose: [0.1, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [0, 0.1, -0.1] }
obj14_joint6(obj14_cube5): {  }
obj14_cube6(obj14_joint6): { pose: [0, -0.3, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1, position: [0, -0.2, -0.1] }
obj15_base: { pose: [0.518038, -0.486132, 0.690001, 0.431156, -0.431165, -0.560454, 0.56044], mass: 0.8, com: [0.05, -8.67362e-19, 0], inertia: [0.016, 0.026, 0.026], multibody, multibody_fixedBase!, multibody_gravity }
obj15_cube0(obj15_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj15_joint1(obj15_cube0): {  }
obj15_cube1(obj15_joint1): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [0.1, 0, 0] }
obj15_joint2(obj15_cube1): {  }
obj15_cube2(obj15_joint2): { pose: [-0.2, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [-0.1, 0, 0] }
obj15_joint3(obj15_cube2): {  }
obj15_cube3(obj15_joint3): { pose: [0.3, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [0.2, 0, 0] }
obj17_base: { pose: [-0.0450188, 0.636789, 0.689982, -0.715472, -0.000169555, -0.000146667, 0.698641], mass: 0.4, com: [0, 0, 0.05], inertia: [0.009, 0.009, 0.008], multibody, multibody_fixedBase!, multibody_gravity }
obj17_cube0(obj17_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], contact: 1 }
obj17_joint1(obj17_cube0): {  }
obj17_cube1(obj17_joint1): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 0], contact: 1, position: [0, 0, 0.1] }