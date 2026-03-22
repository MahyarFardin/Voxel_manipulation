world: {  }
table(world): { pose: [0, 0, 0.6], shape: ssBox, size: [1.6, 1.6, 0.08, 0.02], color: [0.3, 0.3, 0.3], contact: 1, logical: {  }, friction: 0.1 }
obj0_base: { pose: [0.225514, 0.456253, 0.675354, -0.821527, 0.340329, -0.175207, 0.422578], mass: 0.8, com: [0.025, 0.0125, 0.0375], inertia: [0.00475, -0.00025, -0.00025, 0.004875, -0.000125, 0.004875], multibody, multibody_fixedBase!, multibody_gravity }
obj0_cube0(obj0_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1 }
obj0_joint1(obj0_cube0): {  }
obj0_cube1(obj0_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0, 0, 0.05] }
obj0_joint2(obj0_cube1): {  }
obj0_cube2(obj0_joint2): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0.05, 0, 0.05] }
obj0_joint3(obj0_cube2): {  }
obj0_cube3(obj0_joint3): { pose: [0, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0.05, 0.05, 0.05] }
obj1_base: { pose: [0.615512, 0.0354933, 0.664993, 0.701011, 0.701011, 0.0927834, 0.0925112], mass: 0.8, com: [0.0125, 0.0375, 0], inertia: [0.005375, 0.000375, 0, 0.004375, 0, 0.00575], multibody, multibody_fixedBase!, multibody_gravity }
obj1_cube0(obj1_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1 }
obj1_joint1(obj1_cube0): {  }
obj1_cube1(obj1_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0.05, 0, 0] }
obj1_joint2(obj1_cube1): {  }
obj1_cube2(obj1_joint2): { pose: [-0.05, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0, 0.05, 0] }
obj1_joint3(obj1_cube2): {  }
obj1_cube3(obj1_joint3): { pose: [0, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 0, 1], contact: 1, position: [0, 0.1, 0] }
obj3_base: { pose: [-0.28059, 0.320324, 0.664995, -0.102692, 0.699737, 0.102325, 0.699538], mass: 0.8, com: [0.025, 0.025, 0], inertia: [0.0045, 0.0045, 0.005], multibody, multibody_fixedBase!, multibody_gravity }
obj3_cube0(obj3_base): { shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1 }
obj3_joint1(obj3_cube0): {  }
obj3_cube1(obj3_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0.05, 0, 0] }
obj3_joint2(obj3_cube1): {  }
obj3_cube2(obj3_joint2): { pose: [-0.05, 0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0, 0.05, 0] }
obj3_joint3(obj3_cube2): {  }
obj3_cube3(obj3_joint3): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0.05, 0.05, 0] }
obj4_base: { pose: [0.422073, 0.578347, 0.665007, -0.0027689, 1.19807e-05, 0.00017836, 0.999996], mass: 0.8, com: [0.05, 4.55365e-17, 0.0125], inertia: [0.004375, 0.005375, 0.005], multibody, multibody_fixedBase!, multibody_gravity }
obj4_cube0(obj4_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1 }
obj4_joint1(obj4_cube0): {  }
obj4_cube1(obj4_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0.05, 0, 0] }
obj4_joint2(obj4_cube1): {  }
obj4_cube2(obj4_joint2): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0.05, 0, 0.05] }
obj4_joint3(obj4_cube2): {  }
obj4_cube3(obj4_joint3): { pose: [0.05, 0, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0.1, 0, 0] }
obj5_base: { pose: [-0.0905892, 0.595429, 0.665021, -0.316018, 0.632401, 0.316442, 0.632508], mass: 0.8, com: [6.07153e-18, 0.025, 0.025], inertia: [0.005, 0.0045, 0.0045], multibody, multibody_fixedBase!, multibody_gravity }
obj5_cube0(obj5_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1 }
obj5_joint1(obj5_cube0): {  }
obj5_cube1(obj5_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0, 0, 0.05] }
obj5_joint2(obj5_cube1): {  }
obj5_cube2(obj5_joint2): { pose: [0, 0.05, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0, 0.05, 0] }
obj5_joint3(obj5_cube2): {  }
obj5_cube3(obj5_joint3): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 0], contact: 1, position: [0, 0.05, 0.05] }
obj6_base: { pose: [0.604158, 0.106902, 0.665004, -0.696489, 0.696492, 0.122103, -0.122038], mass: 0.8, com: [0.025, 3.03577e-18, 0.025], inertia: [0.0045, 0.005, 0.0045], multibody, multibody_fixedBase!, multibody_gravity }
obj6_cube0(obj6_base): { shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1 }
obj6_joint1(obj6_cube0): {  }
obj6_cube1(obj6_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0, 0, 0.05] }
obj6_joint2(obj6_cube1): {  }
obj6_cube2(obj6_joint2): { pose: [0.05, 0, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0.05, 0, 0] }
obj6_joint3(obj6_cube2): {  }
obj6_cube3(obj6_joint3): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 1], contact: 1, position: [0.05, 0, 0.05] }
obj8_base: { pose: [0.34482, 0.650829, 0.665009, 0.207961, 0.207931, 0.675882, 0.675796], mass: 0.8, com: [0.0625, -3.03577e-17, 0.0125], inertia: [0.004375, 6.67869e-19, -0.000375, 0.00575, 1.82146e-19, 0.005375], multibody, multibody_fixedBase!, multibody_gravity }
obj8_cube0(obj8_base): { shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1 }
obj8_joint1(obj8_cube0): {  }
obj8_cube1(obj8_joint1): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0.05, 0, 0] }
obj8_joint2(obj8_cube1): {  }
obj8_cube2(obj8_joint2): { pose: [0.05, 0, 0], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0.1, 0, 0] }
obj8_joint3(obj8_cube2): {  }
obj8_cube3(obj8_joint3): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [1, 1, 1], contact: 1, position: [0.1, 0, 0.05] }
obj9_base: { pose: [-0.639616, 0.116007, 0.664986, -0.53048, -0.530574, 0.467352, 0.467616], mass: 0.8, com: [0.0125, 0.0125, 0.0125], inertia: [0.00475, 0.000125, 0.000125, 0.00475, 0.000125, 0.00475], multibody, multibody_fixedBase!, multibody_gravity }
obj9_cube0(obj9_base): { shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 0], contact: 1 }
obj9_joint1(obj9_cube0): {  }
obj9_cube1(obj9_joint1): { pose: [0, 0, 0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 0], contact: 1, position: [0, 0, 0.05] }
obj9_joint2(obj9_cube1): {  }
obj9_cube2(obj9_joint2): { pose: [0, 0.05, -0.05], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 0], contact: 1, position: [0, 0.05, 0] }
obj9_joint3(obj9_cube2): {  }
obj9_cube3(obj9_joint3): { pose: [0.05, -0.05, 0], shape: box, size: [0.05, 0.05, 0.05], color: [0, 1, 0], contact: 1, position: [0.05, 0, 0] }
cam_dim_0(world): { pose: [0, 0, 5, 6.12323e-17, 1, 0, 0], shape: camera, size: [1], width: 1920, height: 1920 }
cam_dim_1(world): { pose: [0, 5, 1.5, 3.72759e-17, 4.85789e-17, -0.793353, 0.608761], shape: camera, size: [1], width: 1920, height: 1920 }
cam_dim_2(world): { pose: [0, -5, 1.5, -0.608761, 0.793353, 0, 0], shape: camera, size: [], width: 1920, height: 1920 }
cam_dim_3(world): { pose: [5, 0, 1.5, 0.430459, -0.560986, -0.560986, 0.430459], shape: camera, size: [], width: 1920, height: 1920 }
cam_dim_4(world): { pose: [-5, 0, 1.5, -0.430459, 0.560986, -0.560986, 0.430459], shape: camera, size: [], width: 1920, height: 1920 }