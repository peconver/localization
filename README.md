# Getting data
## Create workspace

``` 
WORKSPACE=~/robot_ws
source /opt/ros/$ROS_DISTRO/setup.bash
mkdir -p $WORKSPACE/src
```


## Add library for sicks scanners

- Download repository and follow install instructions: https://github.com/SICKAG/sick_scan2.git
- Change hostname

``` 
SCANNER=sick_tim_7xx
gedit $WORKSPACE/src/sick_scan2/config/$SCANNER.yaml
```

## Integrating more lidars
- copy repository sick_scan2
```
REPO2=sick_scan2b
mkdir $WORKSPACE/src/sick_scan2b
cp -r $WORKSPACE/src/sick_scan2/. $WORKSPACE/src/$REPO2
```

- change "sick_scan2" for $REPO2 in following files
```
gedit $WORKSPACE/src/$REPO2/package.xml
gedit $WORKSPACE/src/$REPO2/CMakeLists.txt
```

- change name of topics:
    - scan
    - cloud
    - imu
   
in

``` 
gedit $WORKSPACE/src/$REPO2/driver/sick_scan_common.cpp
```

- change frame_id and hostname
```
gedit $WORKSPACE/src/$REPO2/config/$SCANNER.yaml
FRAME_ID2=cloud2
```

## Odometry recording  

Example is in package odometry
- "read_wheels.py" is for reading the values and publishing them
- "string2odom" is for creating message type Odometry

TODO: Add angle to position calculation
  
## Run it
In first terminal
```
source $WORKSPACE/install/setup.bash
ros2 launch sick_scan2 $SCANNER.launch.py
```
In second terminal
```
source $WORKSPACE/install/setup.bash
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 world cloud
```
In third terminal
```
source $WORKSPACE/install/setup.bash
ros2 launch $REPO2 $SCANNER.launch.py
```
In fourth terminal
```
source $WORKSPACE/install/setup.bash
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 world $FRAME_ID2
```
In fifth terminal
```
source $WORKSPACE/install/setup.bash
rviz2 $WORKSPACE/install/$REPO2/share/sick_scan2/launch/rviz/$SCANNER.rviz
```


In sixth terminal
```
source $WORKSPACE/install/setup.bash
ros2 run odometry read_wheels
```

In seventh terminal
```
source $WORKSPACE/install/setup.bash
ros2 run odometry string2odom
```


## Vizualization in RViZ
After transforms were set
https://www.youtube.com/watch?v=dVZwsiCPyi4

## TODO
- Set appropriate transforms
- Create Odometry message in node where values of wheels are read
- Create launch file for running the whole thing

