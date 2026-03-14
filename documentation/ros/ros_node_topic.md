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




# ROS Topic
rostopic and rqt_plot

### Turtle keyboard teleoperation
Need something to drive the turtle around with. \
In a new terminal: \
`rosrun turtlesim turtle_teleop_key`

turtlesim_node & turtle_teleop_key --> Nodes are communicating with each other over a ROS Topic.

**turtle_teleop_key is publishing the key strokes on a topic \
turtlesim subscribes to the same topic**

### rqt_graph
rqt_graph creates a dynamic graph of what's going on in the system \
Install:
```
$ sudo apt-get install ros-<distro>-rqt
$ sudo apt-get install ros-<distro>-rqt-common-plugins
```

### rostopic
Allows you to get information about ROS topics. \
Available sub-commands for rostopic:
```
$ rostopic -h
 # rostopic bw     display bandwidth used by topic
 # rostopic echo   print messages to screen
 # rostopic hz     display publishing rate of topic    
 # rostopic list   print information about active topics
 # rostopic pub    publish data to topic
 # rostopic type   print topic type
```

 - `rostopic echo [topic]` \
    Command velocity data published by the turtle_teleop_key node. \
    e.g. `rostopic echo /turtle1/cmd_vel`
 
 - `rostopic list` \
    Returns a list of all topics currently subscribed to and published. \
    Verbose option: `rostopic list -v`

### ROS Messages
Communication on topics happens by sending ROS messages between nodes. \
Publisher and subscriber must send and receive the same type of message. \
The type of the message sent on a topic can be determined using rostopic type. \

 - `rostopic type [topic]`
    ```
    Try:
        $ rostopic type /turtle1/cmd_vel
    You should get:
        geometry_msgs/Twist
    ```

 - `rosmsg show [type]` \
    We can look at the details of the message using rosmsg:
    ```
    $ rosmsg show geometry_msgs/Twist
    Then we get:
        geometry_msgs/Vector3 linear
            float64 x
            float64 y
            float64 z
        geometry_msgs/Vector3 angular
            float64 x
            float64 y
            float64 z
    ```

 - `rostopic pub [topic] [msg_type] [args]` \
    Publishes data on to a topic currently advertised. \
    e.g. `rostopic pub -1 /turtle1/cmd_vel geometry_msgs/Twist -- '[2.0, 0.0, 0.0]' '[0.0, 0.0, 1.8]'` \
    Here, `rostopic` stands for 'This command will publish messages to a given topic' \
    and `-1` means rostopic will publish one message then exit \
    `--` (double-dash) tells the option parser that none of the following arguments is an option. This is required in cases where your arguments have a leading dash -, like negative numbers.

    **Turtle requires a steady stream of commands at 1 Hz to keep moving.** \
    `rostopic pub -r`: publish a steady stream of commands \
    e.g. `rostopic pub /turtle1/cmd_vel geometry_msgs/Twist -r 1 -- '[2.0, 0.0, 0.0]' '[0.0, 0.0, -1.8]'`

 - `rostopic hz [topic]` \
    Reports the rate at which data is published.
    ```
    $ rostopic hz /turtle1/pose
        You will see:
            subscribed to [/turtle1/pose]
            average rate: 59.354
                    min: 0.005s max: 0.027s std dev: 0.00284s window: 58
            average rate: 59.459
                    min: 0.005s max: 0.027s std dev: 0.00271s window: 118
            average rate: 59.539
                    min: 0.004s max: 0.030s std dev: 0.00339s window: 177
            average rate: 59.492
                    min: 0.004s max: 0.030s std dev: 0.00380s window: 237
            average rate: 59.463
                    min: 0.004s max: 0.030s std dev: 0.00380s window: 290
    ```

 - `rostopic type /turtle1/cmd_vel | rosmsg show` \
    rostopic type in conjunction with rosmsg show to get in depth information about a topic.

### `rqt_plot`
 - `rosrun rqt_plot rqt_plot` (Starting rqt_plot)\
    rqt_plot displays a scrolling time plot of the data published on topics.

    When the new window pop up, a text box in the upper left corner gives you the ability to add any topic to the plot.




# ROS Services and Params

### ROS Services
another way that nodes can communicate with each other. Services allow nodes to send a request and receive a response.

 - `rosservice` \
    rosservice can attach to ROS's client/service framework with services.
    ```
    rosservice list         print information about active services
    rosservice call         call the service with the provided args
    rosservice type         print service type
    rosservice find         find services by service type
    rosservice uri          print service ROSRPC uri
    ```

 - `rosservice list` \
    shows us that the turtlesim node provides nine service

 - `rosservice type [service]` \
    e.g.
    ```
    $ rosservice type /clear
    # Then we get >>> std_srvs/Empty
    ```
    `/clear` service is empty. \
        - service call takes no argument \
        - sends no data when making a request and receives no data when receiving a response.

 - `rossrv show [type]` \
    e.g.
    ```
    $ rosservice type /spawn | rossrv show
    # Then we get
        float32 x
        float32 y
        float32 theta
        string name
        ---
        string name
    ```

 - `rosservice call [service] [args]` \
    e.g.
    ```
    rosservice call /clear
    ```
    It just clears the background of the turtlesim_node.

    ```
    # Spawn a new turtle at a given location and orientation. The name field is optional.
    $ rosservice call /spawn 2 2 0.2 ""
    # service call returns with the name of the newly created turtle
        name: turtle2
    ```

 - `rosparam` \
    Allows you to store and manipulate data on the ROS Parameter Server. \
    Store integers, floats, boolean, dictionaries, and lists. \
    Uses the YAML markup language for syntax.
    ```
    rosparam set            set parameter
    rosparam get            get parameter
    rosparam load           load parameters from file
    rosparam dump           dump parameters to file
    rosparam delete         delete parameter
    rosparam list           list parameter names
    ```

 - `rosparam list` \
    turtlesim node has three parameters on the param server for background color.

 - `rosparam set [param_name]` \
    e.g.
    ```
    $ rosparam set /turtlesim/background_r 150
    $ rosservice call /clear # 해줘야지 색상이 적용됌
    ```

 - `rosparam get [param_name]` \
    Get the values of parameters on the param server.

 - `rosparam get / ` \
    Show contents of the entire Parameter Server. \
    e.g.
    ```
    $ rosparam get /
    # This is what we will see
        rosdistro: 'noetic

            '
        roslaunch:
            uris:
                host_nxt__43407: http://nxt:43407/
        rosversion: '1.15.5

            '
        run_id: 7ef687d8-9ab7-11ea-b692-fcaa1494dbf9
        turtlesim:
            background_b: 255
            background_g: 86
            background_r: 69
    ```

 - `rosparam dump [file_name] [namespace]` \
    e.g.
    ```
    # We write all the parameters to the file params.yaml
    $ rosparam dump params.yaml

    # rosparam dump params.yaml /my_node 처럼 실행하면, /my_node 아래에 있는 파라미터들만 골라서 저장한다.
    $ rosparam dump params.yaml /turtlesim
    ```

 - `rosparam load [file_name] [namespace]` \
    load는 YAML 파일에 적힌 내용을 읽어서 **파라미터 서버에 값을 기록(Set)** 하는 과정입니다. \
    `rosparam load params.yaml copy_turtle`을 실행하면, YAML 파일 내부의 모든 파라미터 키(key) 앞에 /copy_turtle/이라는 접두사가 붙는다.
    e.g.
    ```
    root@7da0021d5679:~/practice# cat params.yaml 
    background_b: 255
    background_g: 86
    background_r: 150

    root@7da0021d5679:~/practice# rosparam load params.yaml copy_turtle

    root@7da0021d5679:~/practice# rosparam dump params.yaml
    root@7da0021d5679:~/practice# cat params.yaml 
    copy_turtle:
        background_b: 255
        background_g: 86
        background_r: 150
    rosdistro: 'noetic

        '
    roslaunch:
        uris:
            host_7da0021d5679__41965: http://7da0021d5679:41965/
    rosversion: '1.17.4

        '
    run_id: dcd6c9f0-1c5f-11f1-84e9-0242ac110002
    turtlesim:
        background_b: 255
        background_g: 86
        background_r: 150
    ```




# Appendix 1: Service랑 Pub/Sub 구조의 차이가 무엇인가?
| 구분 | Topic (Pub/Sub) | Service (Srv) |
|---|---|---|
| 통신 방향 | 단방향 (One-way) | 양방향 (Two-way) |
| 핵심 구조 | Publisher & Subscriber | Client & Server |
| 데이터 흐름 | 지속적 스트리밍 (Continuous) | 요청 시 1회 처리 (Event-based) |
| 비유 | "라디오 방송, 게시판" | "전화 통화, 식당 주문" |
| 응답(Response) | 없음 (보내기만 함) | 있음 (결과값을 반환함) |
| 주 사용처 | "센서 데이터, 상태 모니터링 등" | "특정 동작 명령, 환경 설정 등" |
| 동기/비동기 | 비동기 (Asynchronous) | 동기 (Synchronous) |




# Appendix 2: Parameter가 load 되는 방법
파라미터 서버(Parameter Server)는 일종의 정적 저장소.

`rosparam set`: 서버에 있는 값을 바꿀 뿐입니다. \
 - 노드의 동작: 보통 노드는 시작될 때(Init) 파라미터 서버에서 값을 딱 한 번 읽어와서 자기 변수에 저장합니다. \
 - 문제 발생: 서버의 값이 바뀌어도 노드는 이미 로컬 변수에 저장된 옛날 값을 계속 사용합니다.

`/clear` 서비스의 역할 \
turtlesim 노드는 배경색 파라미터(background_r, g, b)를 매 순간 감시하지 않는다. \
대신, `/clear` 서비스가 호출되는 시점에 **"아, 지금 파라미터 서버에 가서 색상 값을 다시 읽어와야겠다!"** 라고 설계되어 있다.

노드에 따른 params를 업데이트 하는 방식
| 방식 | 설명 |
|---|---|
| 재시작 (Restart) | 가장 일반적입니다. 노드를 껐다 켜면 새로 시작하면서 값을 다시 읽습니다. |
| 특정 서비스 호출 | turtlesim의 /clear처럼 특정 트리거가 발생할 때 다시 읽도록 설계된 경우입니다. |
| Dynamic Reconfigure | rqt_reconfigure를 사용하여 노드를 재시작하지 않고도 실시간으로 값을 반영하는 방식입니다. (가장 세련된 방법!) |