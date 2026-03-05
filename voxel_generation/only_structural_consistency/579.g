base {}

cube0 (base) { 
    shape: box, 
    size: [.1, .1, .1], 
    color: [1, 0, 0], 
    X: "t(0 0 0)" 
}
joint1(cube0):{
  joint: rigid,
  pre: "T t(0 0 0)" 
}

cube1(joint1):{ 
  shape: box, 
  size: [0.1, 0.1, 0.1], 
  color: [1, 0, 0],
  position: [0, 0, 0.1],
  X: "t(0 0 0.1)" 
}

joint2(cube1):{
  joint: rigid,
  pre: "T t(0 0 0)" 
}

cube2(joint2):{ 
  shape: box, 
  size: [0.1, 0.1, 0.1], 
  color: [1, 0, 0],
  position: [0.1, 0, 0],
  X: "t(0.1 0 0)" 
}

joint3(cube2):{
  joint: rigid,
  pre: "T t(0.1 0 0)" 
}

cube3(joint3):{ 
  shape: box, 
  size: [0.1, 0.1, 0.1], 
  color: [1, 0, 0],
  position: [0.2, 0, 0],
  X: "t(0.2 0 0)" 
}
