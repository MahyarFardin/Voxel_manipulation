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
targetSurface: { pose: [0.17232, -0.292317, 0.642] }
targetSurface_tile_0(targetSurface): { pose: [0, -0.05, 0], shape: ssBox, size: [0.1, 0.1, 0.004, 0.001], color: [0, 1, 0] }
targetSurface_tile_1(targetSurface): { pose: [0, 0.05, 0], shape: ssBox, size: [0.1, 0.1, 0.004, 0.001], color: [0, 1, 0] }
obj0_base: { pose: [-0.426404, 0.554883, 0.690008, 0.733748, -3.98457e-05, 3.38107e-05, 0.679421], mass: 1.2, com: [0.133333, 0.0333333, 0.0166667], inertia: [0.0283333, 0.00133333, 0.000666667, 0.0363333, -0.00133333, 0.0373333], multibody, multibody_fixedBase!, multibody_gravity }
obj0_cube0(obj0_base): { shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1 }
obj0_joint1(obj0_cube0): {  }
obj0_cube1(obj0_joint1): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0, 0] }
obj0_joint2(obj0_cube1): {  }
obj0_cube2(obj0_joint2): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.2, 0, 0] }
obj0_joint3(obj0_cube2): {  }
obj0_cube3(obj0_joint3): { pose: [-0.1, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0.1, 0] }
obj0_joint4(obj0_cube3): {  }
obj0_cube4(obj0_joint4): { pose: [0.2, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.3, 0, 0] }
obj0_joint5(obj0_cube4): {  }
obj0_cube5(obj0_joint5): { pose: [-0.2, 0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0.1, 0.1] }
obj2_base: { pose: [-0.125023, 0.45434, 0.68999, 0.32759, 0.327577, 0.626609, 0.626689], mass: 1.2, com: [0.1, 0.0333333, 0.0833333], inertia: [0.0283333, -0.002, -0.002, 0.0336667, -0.000666667, 0.0346667], multibody, multibody_fixedBase!, multibody_gravity }
obj2_cube0(obj2_base): { shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 1], contact: 1 }
obj2_joint1(obj2_cube0): {  }
obj2_cube1(obj2_joint1): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 1], contact: 1, position: [0, 0, 0.1] }
obj2_joint2(obj2_cube1): {  }
obj2_cube2(obj2_joint2): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 1], contact: 1, position: [0.1, 0, 0.1] }
obj2_joint3(obj2_cube2): {  }
obj2_cube3(obj2_joint3): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 1], contact: 1, position: [0.1, 0.1, 0.1] }
obj2_joint4(obj2_cube3): {  }
obj2_cube4(obj2_joint4): { pose: [0.1, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 1], contact: 1, position: [0.2, 0, 0.1] }
obj2_joint5(obj2_cube4): {  }
obj2_cube5(obj2_joint5): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 0, 1], contact: 1, position: [0.2, 0.1, 0.1] }
obj3_base: { pose: [0.534281, 0.518881, 0.690014, -0.812025, 6.27339e-05, 4.94868e-05, 0.583622], mass: 1.2, com: [0.0666667, 0.0833333, 0.0166667], inertia: [0.0313333, -0.00133333, -0.000666667, 0.0283333, -0.000333333, 0.0323333], multibody, multibody_fixedBase!, multibody_gravity }
obj3_cube0(obj3_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1 }
obj3_joint1(obj3_cube0): {  }
obj3_cube1(obj3_joint1): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0, 0.1, 0] }
obj3_joint2(obj3_cube1): {  }
obj3_cube2(obj3_joint2): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.1, 0.1, 0] }
obj3_joint3(obj3_cube2): {  }
obj3_cube3(obj3_joint3): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.1, 0.2, 0] }
obj3_joint4(obj3_cube3): {  }
obj3_cube4(obj3_joint4): { pose: [0, -0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.1, 0.1, 0.1] }
obj3_joint5(obj3_cube4): {  }
obj3_cube5(obj3_joint5): { pose: [0, -0.1, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 1, 0], contact: 1, position: [0.1, 0, 0] }
obj4_base: { pose: [-0.597429, 0.416114, 0.70708, 0.86229, -0.203557, -0.106505, 0.451306], mass: 1.2, com: [0.05, 0.0666667, 0.0833333], inertia: [0.0323333, -0.002, -0.001, 0.0286667, -0.00133333, 0.0336667], multibody, multibody_fixedBase!, multibody_gravity }
obj4_cube0(obj4_base): { shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1 }
obj4_joint1(obj4_cube0): {  }
obj4_cube1(obj4_joint1): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0, 0.1] }
obj4_joint2(obj4_cube1): {  }
obj4_cube2(obj4_joint2): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0, 0.1] }
obj4_joint3(obj4_cube2): {  }
obj4_cube3(obj4_joint3): { pose: [-0.1, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0, 0.1, 0.1] }
obj4_joint4(obj4_cube3): {  }
obj4_cube4(obj4_joint4): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0.1, 0.1] }
obj4_joint5(obj4_cube4): {  }
obj4_cube5(obj4_joint5): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0.2, 0.1] }
obj5_base: { pose: [-0.347491, 0.486495, 0.798316, -0.247077, -0.618999, 0.208089, 0.715885], mass: 1.2, com: [0.116667, 0.0666667, 0.0666667], inertia: [0.0333333, -0.00266667, -0.00466667, 0.0363333, -0.00266667, 0.0323333], multibody, multibody_fixedBase!, multibody_gravity }
obj5_cube0(obj5_base): { shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1 }
obj5_joint1(obj5_cube0): {  }
obj5_cube1(obj5_joint1): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0, 0] }
obj5_joint2(obj5_cube1): {  }
obj5_cube2(obj5_joint2): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0.1, 0] }
obj5_joint3(obj5_cube2): {  }
obj5_cube3(obj5_joint3): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.1, 0.1, 0.1] }
obj5_joint4(obj5_cube3): {  }
obj5_cube4(obj5_joint4): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.2, 0.1, 0.1] }
obj5_joint5(obj5_cube4): {  }
obj5_cube5(obj5_joint5): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [0, 1, 0], contact: 1, position: [0.2, 0.1, 0.2] }