world: {  }
table(world): { pose: [0, 0, 0.6], shape: ssBox, size: [1.6, 1.6, 0.08, 0.02], color: [0.3, 0.3, 0.3], contact: 1, logical: {  }, friction: 0.1 }
obj0_base: { pose: [0.22285, 0.464133, 0.675371, -0.799179, 0.331483, -0.191789, 0.463302], mass: 0.8, com: [0.025, 0.0125, 0.0375], inertia: [0.00475, -0.00025, -0.00025, 0.004875, -0.000125, 0.004875], multibody, multibody_fixedBase!, multibody_gravity }
obj0_cube0(obj0_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1 }
obj0_joint1(obj0_cube0): {  }
obj0_cube1(obj0_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0, 0, 0.05] }
obj0_joint2(obj0_cube1): {  }
obj0_cube2(obj0_joint2): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0.05, 0, 0.05] }
obj0_joint3(obj0_cube2): {  }
obj0_cube3(obj0_joint3): { pose: [0, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0.05, 0.05, 0.05] }
obj1_base: { pose: [0.615514, 0.0354655, 0.665011, 0.700756, 0.701241, 0.0928159, 0.0926678], mass: 0.8, com: [0.0125, 0.0375, 0], inertia: [0.005375, 0.000375, 0, 0.004375, 0, 0.00575], multibody, multibody_fixedBase!, multibody_gravity }
obj1_cube0(obj1_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1 }
obj1_joint1(obj1_cube0): {  }
obj1_cube1(obj1_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0.05, 0, 0] }
obj1_joint2(obj1_cube1): {  }
obj1_cube2(obj1_joint2): { pose: [-0.05, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0, 0.05, 0] }
obj1_joint3(obj1_cube2): {  }
obj1_cube3(obj1_joint3): { pose: [0, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0, 0.1, 0] }
obj3_base: { pose: [-0.280603, 0.321637, 0.665016, -0.116058, 0.697387, 0.116677, 0.697544], mass: 0.8, com: [0.025, 0.025, 0], inertia: [0.0045, 0.0045, 0.005], multibody, multibody_fixedBase!, multibody_gravity }
obj3_cube0(obj3_base): { shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1 }
obj3_joint1(obj3_cube0): {  }
obj3_cube1(obj3_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0.05, 0, 0] }
obj3_joint2(obj3_cube1): {  }
obj3_cube2(obj3_joint2): { pose: [-0.05, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0, 0.05, 0] }
obj3_joint3(obj3_cube2): {  }
obj3_cube3(obj3_joint3): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0.05, 0.05, 0] }
obj4_base: { pose: [0.422058, 0.578298, 0.66503, -0.00272182, -0.000118346, -0.000259772, 0.999996], mass: 0.8, com: [0.05, 4.55365e-17, 0.0125], inertia: [0.004375, 0.005375, 0.005], multibody, multibody_fixedBase!, multibody_gravity }
obj4_cube0(obj4_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1 }
obj4_joint1(obj4_cube0): {  }
obj4_cube1(obj4_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0.05, 0, 0] }
obj4_joint2(obj4_cube1): {  }
obj4_cube2(obj4_joint2): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0.05, 0, 0.05] }
obj4_joint3(obj4_cube2): {  }
obj4_cube3(obj4_joint3): { pose: [0.05, 0, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0.1, 0, 0] }
obj5_base: { pose: [-0.0905798, 0.595385, 0.665013, -0.316375, 0.6323, 0.316105, 0.632599], mass: 0.8, com: [6.07153e-18, 0.025, 0.025], inertia: [0.005, 0.0045, 0.0045], multibody, multibody_fixedBase!, multibody_gravity }
obj5_cube0(obj5_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1 }
obj5_joint1(obj5_cube0): {  }
obj5_cube1(obj5_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0, 0, 0.05] }
obj5_joint2(obj5_cube1): {  }
obj5_cube2(obj5_joint2): { pose: [0, 0.05, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0, 0.05, 0] }
obj5_joint3(obj5_cube2): {  }
obj5_cube3(obj5_joint3): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0, 0.05, 0.05] }
obj6_base: { pose: [0.475067, 0.0673609, 0.665, -0.0360259, -0.036029, 0.706188, 0.706189], mass: 0.8, com: [0.025, 3.03577e-18, 0.025], inertia: [0.0045, 0.005, 0.0045], multibody, multibody_fixedBase!, multibody_gravity }
obj6_cube0(obj6_base): { shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1 }
obj6_joint1(obj6_cube0): {  }
obj6_cube1(obj6_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0, 0, 0.05] }
obj6_joint2(obj6_cube1): {  }
obj6_cube2(obj6_joint2): { pose: [0.05, 0, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0.05, 0, 0] }
obj6_joint3(obj6_cube2): {  }
obj6_cube3(obj6_joint3): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0.05, 0, 0.05] }
obj8_base: { pose: [0.344403, 0.650717, 0.665011, 0.209163, 0.209103, 0.675484, 0.675461], mass: 0.8, com: [0.0625, -3.03577e-17, 0.0125], inertia: [0.004375, 6.67869e-19, -0.000375, 0.00575, 1.82146e-19, 0.005375], multibody, multibody_fixedBase!, multibody_gravity }
obj8_cube0(obj8_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1 }
obj8_joint1(obj8_cube0): {  }
obj8_cube1(obj8_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0.05, 0, 0] }
obj8_joint2(obj8_cube1): {  }
obj8_cube2(obj8_joint2): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0.1, 0, 0] }
obj8_joint3(obj8_cube2): {  }
obj8_cube3(obj8_joint3): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0.1, 0, 0.05] }
obj9_base: { pose: [-0.480726, 0.668018, 0.665001, 0.156498, 0.156568, 0.689621, 0.689505], mass: 0.8, com: [0.05, 2.77556e-17, 0.0125], inertia: [0.004375, 0.005375, 0.005], multibody, multibody_fixedBase!, multibody_gravity }
obj9_cube0(obj9_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1 }
obj9_joint1(obj9_cube0): {  }
obj9_cube1(obj9_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0.05, 0, 0] }
obj9_joint2(obj9_cube1): {  }
obj9_cube2(obj9_joint2): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0.05, 0, 0.05] }
obj9_joint3(obj9_cube2): {  }
obj9_cube3(obj9_joint3): { pose: [0.05, 0, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0.1, 0, 0] }
obj10_base: { pose: [0.602116, 0.259665, 0.665034, -0.448092, -0.448497, 0.546943, 0.546734], mass: 0.8, com: [0.05, 0.0125, 0], inertia: [0.004375, 0.005, 0.005375], multibody, multibody_fixedBase!, multibody_gravity }
obj10_cube0(obj10_base): { shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1 }
obj10_joint1(obj10_cube0): {  }
obj10_cube1(obj10_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0.05, 0, 0] }
obj10_joint2(obj10_cube1): {  }
obj10_cube2(obj10_joint2): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0.1, 0, 0] }
obj10_joint3(obj10_cube2): {  }
obj10_cube3(obj10_joint3): { pose: [-0.05, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0.05, 0.05, 0] }
obj11_base: { pose: [0.265911, 0.307537, 0.669408, -0.138012, -0.168701, 0.754723, 0.618778], mass: 0.8, com: [2.60209e-18, 0.0375, 0.0375], inertia: [0.00575, -2.60209e-20, -2.60209e-20, 0.005375, -0.000375, 0.004375], multibody, multibody_fixedBase!, multibody_gravity }
obj11_cube0(obj11_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1 }
obj11_joint1(obj11_cube0): {  }
obj11_cube1(obj11_joint1): { pose: [0, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0, 0.05, 0] }
obj11_joint2(obj11_cube1): {  }
obj11_cube2(obj11_joint2): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0, 0.05, 0.05] }
obj11_joint3(obj11_cube2): {  }
obj11_cube3(obj11_joint3): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0, 0.05, 0.1] }
obj12_base: { pose: [-0.455396, 0.410201, 0.664989, -0.612368, 0.353522, 0.612275, 0.353762], mass: 0.8, com: [5.20417e-18, 0.0375, 0.0375], inertia: [0.00575, -1.9082e-19, -5.20417e-20, 0.004375, -0.000375, 0.005375], multibody, multibody_fixedBase!, multibody_gravity }
obj12_cube0(obj12_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1 }
obj12_joint1(obj12_cube0): {  }
obj12_cube1(obj12_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0, 0, 0.05] }
obj12_joint2(obj12_cube1): {  }
obj12_cube2(obj12_joint2): { pose: [0, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0, 0.05, 0.05] }
obj12_joint3(obj12_cube2): {  }
obj12_cube3(obj12_joint3): { pose: [0, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 0], contact: 1, position: [0, 0.1, 0.05] }
obj13_base: { pose: [0.154366, 0.589282, 0.675331, 0.331349, -0.357001, 0.137267, 0.862506], mass: 0.8, com: [0.0125, 0.0125, 0.0375], inertia: [0.00475, 0.000125, -0.000125, 0.00475, -0.000125, 0.00475], multibody, multibody_fixedBase!, multibody_gravity }
obj13_cube0(obj13_base): { shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 0], contact: 1 }
obj13_joint1(obj13_cube0): {  }
obj13_cube1(obj13_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 0], contact: 1, position: [0, 0, 0.05] }
obj13_joint2(obj13_cube1): {  }
obj13_cube2(obj13_joint2): { pose: [0, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 0], contact: 1, position: [0, 0.05, 0.05] }
obj13_joint3(obj13_cube2): {  }
obj13_cube3(obj13_joint3): { pose: [0.05, -0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 0], contact: 1, position: [0.05, 0, 0.05] }
obj14_base: { pose: [-0.704478, 0.510229, 0.665029, -0.195149, -0.195489, 0.679601, 0.679591], mass: 0.8, com: [0.0375, 1.36609e-17, 0.0375], inertia: [0.005375, -1.36609e-19, -0.000375, 0.00575, -1.36609e-19, 0.004375], multibody, multibody_fixedBase!, multibody_gravity }
obj14_cube0(obj14_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1 }
obj14_joint1(obj14_cube0): {  }
obj14_cube1(obj14_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0.05, 0, 0] }
obj14_joint2(obj14_cube1): {  }
obj14_cube2(obj14_joint2): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0.05, 0, 0.05] }
obj14_joint3(obj14_cube2): {  }
obj14_cube3(obj14_joint3): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0.05, 0, 0.1] }
obj16_base: { pose: [-0.0894421, 0.258738, 0.715031, 0.707068, -0.000792801, 0.707144, 0.00143781], mass: 0.8, com: [0.0375, 0.0125, 0.0125], inertia: [0.00475, -0.000125, -0.000125, 0.00475, 0.000125, 0.00475], multibody, multibody_fixedBase!, multibody_gravity }
obj16_cube0(obj16_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1 }
obj16_joint1(obj16_cube0): {  }
obj16_cube1(obj16_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0.05, 0, 0] }
obj16_joint2(obj16_cube1): {  }
obj16_cube2(obj16_joint2): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0.05, 0, 0.05] }
obj16_joint3(obj16_cube2): {  }
obj16_cube3(obj16_joint3): { pose: [0, 0.05, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0.05, 0.05, 0] }
obj18_base: { pose: [-0.13659, 0.383357, 0.665007, 0.430556, 0.43073, 0.560865, 0.560824], mass: 0.8, com: [0.0375, 0.0125, 0.0125], inertia: [0.00475, -0.000125, -0.000125, 0.00475, 0.000125, 0.00475], multibody, multibody_fixedBase!, multibody_gravity }
obj18_cube0(obj18_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1 }
obj18_joint1(obj18_cube0): {  }
obj18_cube1(obj18_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0.05, 0, 0] }
obj18_joint2(obj18_cube1): {  }
obj18_cube2(obj18_joint2): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0.05, 0, 0.05] }
obj18_joint3(obj18_cube2): {  }
obj18_cube3(obj18_joint3): { pose: [0, 0.05, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0.05, 0.05, 0] }
cam_dim_0(world): { pose: [0, 0, 5, 6.12323e-17, 1, 0, 0], shape: camera, size: [1], width: 1920, height: 1920 }
cam_dim_1(world): { pose: [0, 5, 1.5, 3.72759e-17, 4.85789e-17, -0.793353, 0.608761], shape: camera, size: [1], width: 1920, height: 1920 }
cam_dim_2(world): { pose: [0, -5, 1.5, -0.608761, 0.793353, 0, 0], shape: camera, size: [], width: 1920, height: 1920 }
cam_dim_3(world): { pose: [5, 0, 1.5, 0.430459, -0.560986, -0.560986, 0.430459], shape: camera, size: [], width: 1920, height: 1920 }
cam_dim_4(world): { pose: [-5, 0, 1.5, -0.430459, 0.560986, -0.560986, 0.430459], shape: camera, size: [], width: 1920, height: 1920 }