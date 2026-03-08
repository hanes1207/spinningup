Ref: https://wiki.ros.org/ROS/Tutorials

# How to start?
There will be many workspaces \
For example, we have workspace in `/root/catkin_ws` \
To start, we have to source setup.*sh files to overlay this workspace on top of our environment.
 - `source root/catkin_ws/devel/setup.bash`

To make sure your workspace is properly overlayed by the setup script, make sure ROS_PACKAGE_PATH environment variable includes the directory you're in.
 - `$ echo $ROS_PACKAGE_PATH`
 - `/home/youruser/catkin_ws/src:/opt/ros/noetic/share`

# Navigating the ROS Filesystem
ROS tools, will only find ROS packages that are within the directories listed in your ROS_PACKAGE_PATH. \
To see what is in your ROS_PACKAGE_PATH, type: \
`echo $ROS_PACKAGE_PATH`


### rospack
`rospack find [package_name]` \
e.g. `rospack find roscpp` \
일반 find와 다른점: 
 - rospack find: ROS 패키지 전용 도구입니다. 이 명령어는 아무데나 뒤지는 게 아니라, 아까 우리가 설정한 **$ROS_PACKAGE_PATH**라는 환경 변수를 참고합니다.
 - 일반 find: 리눅스의 표준 find 명령어는 현재 당신이 위치한 디렉토리 내부에서 파일을 찾으려고 시도합니다. \
 `# 루트(/)부터 전체 시스템을 다 뒤져서 'roscpp'라는 이름을 찾아라` \
 `find / -name "roscpp" 2>/dev/null`

### roscd
`roscd <package-or-stack>[/subdir]` \
e.g. `roscd roscpp` \
roscd is part of the rosbash suite. It allows you to change directory (cd) directly to a package or a stack.

### rosls
`rosls <package-or-stack>[/subdir]` \
e.g. `rosls roscpp_tutorials`




# Creating a ROS Package
### Requirements to be considered as catkin package
 - catkin compliant package.xml: provides meta information about the package
 - CMakeLists.txt which uses catkin: catkin metapackage it must have the relevant boilerplate CMakeLists.txt file
 - Each package must have its own folder

e.g. (simplest)
```
my_package/
  CMakeLists.txt
  package.xml
```

### Creating a catkin Package
Change to the source space directory of the catkin workspace you created in the Creating a Workspace for catkin tutorial:
```
# You should have created this in the Creating a Workspace Tutorial
$ cd ~/catkin_ws/src
```

Catkin_create_pkg requires that you give it a package_name and optionally a list of dependencies on which that package depends:
```
# This is an example, do not try to run this
# catkin_create_pkg <package_name> [depend1] [depend2] [depend3]
```

e.g. `catkin_create_pkg beginner_tutorials std_msgs rospy roscpp`

### Building a catkin workspace and sourcing the setup file
Now you need to build the packages in the catkin workspace:
```
$ cd ~/catkin_ws
$ catkin_make
```

To add the workspace to your ROS environment you need to source the generated setup file: \
`. ~/catkin_ws/devel/setup.bash`

### Package dependencies
**First-order dependencies** \
`rospack depends1 beginner_tutorials`

rospack lists the same dependencies that were used as arguments when running catkin_create_pkg. These dependencies for a package are stored in the package.xml file:
```
$ roscd beginner_tutorials
$ cat package.xml
```

**Indirect dependencies** \
rospack recursively determine all nested dependencies \
`$ rospack depends beginner_tutorials`




# Building a ROS Package
### Using catkin_make
```
# Just an example of how CMake generally works
# In a CMake project
$ mkdir build
$ cd build
$ cmake ..
$ make
$ make install  # (optionally)
```

In case of catkin_make,
```
# In a catkin workspace
$ catkin_make
$ catkin_make install  # (optionally)
```

The above commands will build any catkin projects found in the src folder. This follows the recommendations set by REP128. \
If your source code is in a different place, say **my_src** then you would call catkin_make like this:
```
# In a catkin workspace
$ catkin_make --source my_src
$ catkin_make install --source my_src  # (optionally)
```

The **build folder** is the default location of the build space and is where cmake and make are called to configure and build your packages.

The **devel folder** is the default location of the devel space, which is where your executables and libraries go before you install your packages.