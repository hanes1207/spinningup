# rqt_console

### rqt_console 
rqt_console attaches to ROS's logging framework to display output from nodes

`rosrun rqt_console rqt_console`

e.g.
 - `rosrun turtlesim turtlesim_node`을 키고 \
    logger level을 'warn'으로 하고 \
    `rostopic pub /turtle1/cmd_vel geometry_msgs/Twist -r 1 -- '{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0,y: 0.0,z: 0.0}}'`으로 계속 벽에 박으면 \
    console에 뭐가 메시지가 계속 쌓인다.

### rqt_logger_level
rqt_logger_level allows us to change the verbosity level (DEBUG, WARN, INFO, and ERROR) of nodes as they run.

`rosrun rqt_logger_level rqt_logger_level`

Log level priortization \
```
Fatal
Error
Warn
Info
Debug
```
By setting the logger level, you will get all messages of that priority level or higher.




# roslaunch
starting many nodes at once

### `roslaunch [package] [filename.launch]`
Have to use launch file.

*왜 https://wiki.ros.org/ROS/Tutorials/UsingRqtconsoleRoslaunch 여기서 \
roscd beginner_tutorials 이거 안먹을까?
 - workspace catkin_ws에서 작업하고 있기 때문
 - `cd ~/catkin_ws`
 - `source devel/setup.bash`를 해줘야 한다.

```
roscd beginner_tutorials
mkdir launch
cd launch
```

*launch file --> launch file을 저장하는 디렉토리의 이름이 launch일 필요가 없고, 디렉토리일 필요도 없음.
*roslaunch command automatically looks into the passed package and detects available launch files.

`touch turtlemimic.launch`하고 아래 붙여넣기
```
# start the launch file with the launch tag, so that the file is identified as a launch file.
<launch>

# Here we start two groups with a namespace tag of turtlesim1 and turtlesim2 with a turtlesim node with a name of sim.
# Why same name sim? --> 하나의 node에 거북이를 2개 만드는게 아니라, 두 개의 노드에 거북이를 각각 spawn
# This allows us to start two simulators without having name conflicts.
  <group ns="turtlesim1">
    <node pkg="turtlesim" name="sim" type="turtlesim_node"/>
  </group>

  <group ns="turtlesim2">
    <node pkg="turtlesim" name="sim" type="turtlesim_node"/>
  </group>

# Start the mimic node with the topics input and output renamed to turtlesim1 and turtlesim2. This renaming will cause turtlesim2 to mimic turtlesim1.
  <node pkg="turtlesim" name="mimic" type="mimic">
    <remap from="input" to="turtlesim1/turtle1"/>
    <remap from="output" to="turtlesim2/turtle1"/>
  </node>

# Closes the xml tag for the launch file.
</launch>
```

`roslaunch beginner_tutorials turtlemimic.launch` to launch the file

`rostopic pub /turtlesim1/turtle1/cmd_vel geometry_msgs/Twist -r 1 -- '[2.0, 0.0, 0.0]' '[0.0, 0.0, -1.8]'` 으로 실행하기

`rqt` 한 다음에 main window에서 select Plugins > Introspection > Node Graph: 하거나 \
`rqt_graph`하기




# Appendix 1: `name="sim"`은 뭘까?
`<node pkg="turtlesim" name="sim" type="turtlesim_node"/>`우리가 turtlesim node pkg안에서 turtlesim_node를 실행시킨거는 알겠는데, sim은 뭐지? 나중에 어떻게 쓰는거지?
 
프로그램(실행 파일)이 **'뭐냐'** 를 묻는 게 type="turtlesim_node"라면, 지금 내 시스템에서    **'이름이 뭐냐'** 를 묻는 게 name="sim"입니다.

`rosnode list`를 치면 
```
root@7da0021d5679:~# rosnode list
/mimic
/rosout
/rostopic_35874_1773238914750
/rqt_gui_py_node_36798
/rqt_gui_py_node_74547
/turtlesim
/turtlesim1/sim
/turtlesim2/sim
```
가 나오는데 여기서 turtlesim1 이랑 turtlesim2은 namespace이고, sim은 프로그램의 별명이다.

비유하자면 **"네임스페이스는 폴더(디렉토리)"** 이고, **"노드 이름은 파일 이름"** 입니다.

| 구분 | 역할 | 특징 |
|---|---|---|
| 네임스페이스 (Namespace) | **공간(방)** 을 나눔 | "이름 충돌을 방지하고, 그룹별로 설정을 적용하기 좋음" |
| 노드 이름 (Name) | 개체를 식별 | 시스템 내에서 특정 프로그램을 가리키는 고유 ID |

**왜 이걸 따로 쓸까?** \
네임스페이스와 노드 이름을 분리해서 쓰면 재사용성이 폭발적으로 좋아집니다.

예시: turtlesim이라는 똑같은 노드(파일명 sim)를 100번 실행한다고 가정해 봅시다. \
이름을 일일이 sim1, sim2, sim3...으로 바꿔야 한다면 얼마나 힘들까요? \
하지만 네임스페이스를 쓰면 **"1번방의 sim", "2번방의 sim"**처럼 폴더만 바꿔서 똑같은 코드를 그대로 실행할 수 있습니다.

하지만, "네임스페이스"와 "노드 이름"은 물리적인 파일 시스템상의 폴더나 파일이 절대 아니다.
ROS에서의 네임스페이스와 노드 이름은 **'논리적인 주소 체계'** 일 뿐입니다.

ROS의 파라미터 서버와 노드 목록은 하드디스크에 파일로 저장되는 것이 아니라, **ROS Master(또는 로봇 시스템의 메모리)** 에 올라가 있는 **데이터 구조(그래프 형태)** 입니다.

우리가 이를 '폴더'나 '경로'라고 부르는 이유는, 주소를 표현하는 방식이 파일 시스템과 똑같기 때문입니다.
/turtlesim1/sim → /(루트) 아래 turtlesim1이라는 공간 속에 sim이라는 존재가 있다.

정리하자면 하나의 노드는 하나의 프로그램만 실행시킬 수 있고, turtlesim_node라고 부르기 귀찮으니까 sim으로 별명을 붙여서 부르는거다.
 - turtlesim_node_1234567890123 (시스템이 자동으로 붙이는 긴 이름)
 - sim (내가 붙인 짧은 별명)

더 중요한 이유: "다중 실행"
 - 같은 turtlesim_node 프로그램을 두 번 실행하고 싶을 때, 이름을 다르게(혹은 네임스페이스를 다르게) 붙여주지 않으면 서로 충돌이 나서 하나가 죽어버립니다.
 - 별명(name) 또는 네임스페이스(ns)가 없다면: \
    노드 A(turtlesim_node) 실행
    노드 B(turtlesim_node) 실행 → "이미 같은 이름의 노드가 있는데? 그럼 A 죽이고 내가 들어간다!" (시스템 충돌)