# ROS Nodes
Graph concepts:
 - Nodes: A node is an executable that uses ROS to communicate with other nodes.
 - Messages: ROS data type used when subscribing or publishing to a topic.
 - Topics: Nodes can publish messages to a topic as well as subscribe to a topic to receive messages.
 - Master: Name service for ROS (i.e. helps nodes find each other)
 - rosout: ROS equivalent of stdout/stderr
 - roscore: Master + rosout + parameter server (parameter server will be introduced later)

### Nodes
ROS nodes **use a ROS client library** to **communicate with other nodes.** \
Nodes can **publish or subscribe to a Topic.** \
Nodes can also **provide or use a Service.**

### Client Libraries
ROS client libraries allow nodes written in different programming languages to communicate:
 - rospy = python client library \
 - roscpp = c++ client library

### `roscore`
roscore is the first thing you should run when using ROS.

Will see something similar to
```
... logging to ~/.ros/log/9cf88ce4-b14d-11df-8a75-00251148e8cf/roslaunch-machine_name-13039.log
Checking log directory for disk usage. This may take awhile.
Press Ctrl-C to interrupt
Done checking log file disk usage. Usage is <1GB.

started roslaunch server http://machine_name:33919/
ros_comm version 1.4.7

SUMMARY
======

PARAMETERS
 * /rosversion
 * /rosdistro

NODES

auto-starting new master
process[master]: started with pid [13054]
ROS_MASTER_URI=http://machine_name:11311/

setting /run_id to 9cf88ce4-b14d-11df-8a75-00251148e8cf
process[rosout-1]: started with pid [13067]
started core service [/rosout]
```
**If roscore does not initialize, you probably have a network configuration issue.**

If roscore does not initialize and sends a message about lack of permissions, probably the ~/.ros folder is owned by root, change recursively the ownership of that folder with: \
`$ sudo chown -R <your_username> ~/.ros`

### `rosnode`
rosnode displays information about the ROS nodes that are currently running. \
The rosnode list command lists these active nodes: `$ rosnode list` \
You will see: `/rosout`

This showed us that there is **only one node running: rosout**. This is **always running as it collects and logs nodes' debugging output**.

The rosnode info command returns information about a specific node.: `rosnode info /rosout`

### `rosrun [package_name] [node_name]`
rosrun allows you to use the package name to directly run a node within a package (without having to know the package path).

e.g. `rosrun turtlesim turtlesim_node` \
이러면 `rosnode list`치면 `/rosout`이랑 `/turtlesim` 보여야 함.

```
(spinningup) root@7da0021d5679:~# rosrun turtlesim turtlesim_node
QStandardPaths: XDG_RUNTIME_DIR not set, defaulting to '/tmp/runtime-root'
[INFO] [1772974143.695265588]: Starting turtlesim with node name /turtlesim
[INFO] [1772974143.697269921]: Spawning turtle [turtle1] at x=[5.544445], y=[5.544445], theta=[0.000000]
libGL error: No matching fbConfigs or visuals found
libGL error: failed to load driver: swrast
```
이거는 무슨 에러지? - libGL error, 도커 컨테이너는 기본적으로 물리적인 GPU에 직접 접근할 수 없는데, turtlesim은 화면을 그릴 때 3D 가속 기능이 필요해서 발생하는 문제.


node 이름 변경 가능하다 \
`rosrun turtlesim turtlesim_node __name:=my_turtle` 하면 \
`rosnode list`치면 `/rosout`이랑 `/my_turtle` 보여야 함.