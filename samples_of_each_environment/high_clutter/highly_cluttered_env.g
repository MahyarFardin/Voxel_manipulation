807_base: { pose: [0, 0, 0.05] }
807_cube0(807_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0] }
807_joint1(807_cube0): { joint: rigid }
807_cube1(807_joint1): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], position: [0, 0.1, 0] }
807_joint2(807_joint2_origin): { joint: rigid }
807_cube2(807_joint2): { pose: [0, -0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], position: [0, 0.1, 0.1] }
807_joint3(807_joint3_origin): { joint: rigid }
807_cube3(807_joint3): { pose: [0.1, -0.1, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], position: [0.1, 0.1, 0] }
807_joint2_origin(807_cube1): { pose: [0, 0.1, 0] }
807_joint3_origin(807_cube2): { pose: [0, 0.1, 0] }
57_base: { pose: [0, 0.2, 0.05] }
57_cube0(57_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0] }
57_joint1(57_cube0): { joint: rigid }
57_cube1(57_joint1): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], position: [0, 0, 0.1] }
57_joint2(57_joint2_origin): { joint: rigid }
57_cube2(57_joint2): { pose: [0.1, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], position: [0.1, 0, 0.1] }
57_joint3(57_joint3_origin): { joint: rigid }
57_cube3(57_joint3): { pose: [0.1, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], position: [0.2, 0, 0.1] }
57_joint2_origin(57_cube1): { pose: [0, 0, 0.1] }
57_joint3_origin(57_cube2): { pose: [0, 0, 0.1] }
768_base: { pose: [0, 0.4, 0.05] }
768_cube0(768_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0] }
768_joint1(768_cube0): { joint: rigid }
768_cube1(768_joint1): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], position: [0, 0.1, 0] }
768_joint2(768_joint2_origin): { joint: rigid }
768_cube2(768_joint2): { pose: [0, -0.1, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], position: [0, 0.1, 0.1] }
768_joint3(768_joint3_origin): { joint: rigid }
768_cube3(768_joint3): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], position: [0, 0.2, 0] }
768_joint2_origin(768_cube1): { pose: [0, 0.1, 0] }
768_joint3_origin(768_cube2): { pose: [0, 0.1, 0] }
898_base: { pose: [0.2, 0.4, 0.05] }
898_cube0(898_base): { pose: [0, -0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0] }
898_joint1(898_cube0): { joint: rigid }
898_cube1(898_joint1): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], position: [0, 0.1, 0] }
898_joint2(898_cube1): { joint: rigid }
898_cube2(898_joint2): { pose: [0, 0.1, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], position: [0, 0.2, 0] }
898_joint3(898_cube2): { joint: rigid }
898_cube3(898_joint3): { pose: [0.1, -0.2, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], position: [0.1, 0, 0] }
347_base: { pose: [0.2, 0.6, 0.05] }
347_cube0(347_base): { shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0] }
347_joint1(347_cube0): { joint: rigid }
347_cube1(347_joint1): { pose: [0, 0, 0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], position: [0, 0, 0.1] }
347_joint2(347_cube1): { joint: rigid }
347_cube2(347_joint2): { pose: [0.1, 0, 0], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], position: [0.1, 0, 0.1] }
347_joint3(347_joint3_origin): { joint: rigid }
347_cube3(347_joint3): { pose: [0, 0, -0.1], shape: box, size: [0.1, 0.1, 0.1], color: [1, 0, 0], position: [0.2, 0, 0.1] }
347_joint3_origin(347_cube2): { pose: [0.1, 0, 0.1] }
world: { pose: [0.2, 0.3, 0.1] }
cam_dim_0(world): { pose: [0, 0, 5, 6.12323e-17, 1, 0, 0], shape: camera, size: [], width: 500, height: 500 }
cam_dim_1(world): { pose: [0, 4, 0.1, 4.32978e-17, 4.32978e-17, -0.707107, 0.707107], shape: camera, size: [], width: 500, height: 500 }
cam_dim_2(world): { pose: [0, -4, 0.1, -0.707107, 0.707107, 0, 0], shape: camera, size: [], width: 500, height: 500 }
cam_dim_3(world): { pose: [4, 0, 0.1, 0.5, -0.5, -0.5, 0.5], shape: camera, size: [], width: 500, height: 500 }
cam_dim_4(world): { pose: [-4, 0, 0.1, -0.5, 0.5, -0.5, 0.5], shape: camera, size: [], width: 500, height: 500 }