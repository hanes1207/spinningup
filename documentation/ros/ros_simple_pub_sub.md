# Writing the Publisher Node
"Node" is the ROS term for an executable that is connected to the ROS network. \
Here we'll create the publisher ("talker") node which will continually broadcast a message.

```
$ roscd beginner_tutorials
$ mkdir scripts
$ cd scripts
$ wget https://raw.github.com/ros/ros_tutorials/kinetic-devel/rospy_tutorials/001_talker_listener/talker.py
$ chmod +x talker.py
```

다운받은 코드:
``` python
# Every Python ROS Node will have this declaration at the top. The first line makes sure your script is executed as a Python script.
#!/usr/bin/env python
# license removed for brevity

# import rospy if you are writing a ROS Node. 
import rospy
# The std_msgs.msg import is so that we can reuse the std_msgs/String message type (a simple string container) for publishing.
from std_msgs.msg import String

def talker():
    # This section of code defines the talker's interface to the rest of ROS.

    # declares that your node is publishing to the chatter topic using the message type String.
    # queue_size argument limits the amount of queued messages if any subscriber is not receiving them fast enough.
    pub = rospy.Publisher('chatter', String, queue_size=10)

    # rospy.init_node(NAME, ...), is very important as it tells rospy the name of your node -- until rospy has this information, it cannot start communicating with the ROS Master.
    # anonymous = True ensures that your node has a unique name by adding random numbers to the end of NAME.
    rospy.init_node('talker', anonymous=True)

    # This line creates a Rate object rate.
    rate = rospy.Rate(10) # 10hz

    # have to check is_shutdown() to check if your program should exit (e.g. if there is a Ctrl-C or otherwise).
    while not rospy.is_shutdown():

        hello_str = "hello world %s" % rospy.get_time()

        # loginfo(str), which performs triple-duty: the messages get printed to screen, it gets written to the Node's log file, and it gets written to rosout. rosout is a handy tool for debugging:
        rospy.loginfo(hello_str)

        # publishes a string to our chatter topic
        pub.publish(hello_str)

        # sleeps just long enough to maintain the desired rate through the loop
        # rospy.sleep()도 되지만, 고정된 시간만큼 쉬고, 주기 보정을 해주지 않음
        rate.sleep()

if __name__ == '__main__':
    # catches a rospy.ROSInterruptException exception, which can be thrown by rospy.sleep() and rospy.Rate.sleep() methods when Ctrl-C is pressed or your Node is otherwise shutdown. The reason this exception is raised is so that you don't accidentally continue executing code after the sleep().
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
```

*What it looks like to publish more complicated types? 
 - The general rule of thumb is that constructor args are in the same order as in the .msg file.
    ```
    from beginner_tutorials.msg import Num

    # 순서대로: first, second, label
    msg = Num(10, 20, "hello")
    ```
 - or you can initialize some of the fields and leave the rest with default values:
    ```
    # 가독성, 유연성, 일부 필드만 설정할 수 있는 장점이 있어서 필드 직접 초기화가 더 자주 쓰인다.
    msg = Num()
    msg.first = 10
    msg.second = 20
    msg.label = "hello"
    ```

*왜 예외(InterruptException)을 catch 해야할까? \
try-except로 잡지 않아도 Ctrl+C를 누르면 프로그램은 종료됩니다. 하지만 그렇게 하면 터미널에 지저분한 에러 트레이스백(Traceback) 메시지가 쏟아져 나옵니다. \
--> 프로그램이 **"에러가 나서 죽은 것"** 이 아니라 **"사용자가 의도적으로 종료하여 정상적으로 마무리된 것"** 임을 보장할 수 있습니다.

*While 문에 while not rospy.is_shutdown()이 있는데 또 try, except를 해줘야하나?
 - while 문이 미처 감지하지 못하는 순간 \
    루프가 돌아가는 도중, 가장 많은 시간을 보내는 곳이 어디일까요? 바로 rate.sleep() 구간입니다. \
    만약 노드가 실행되는 동안 Ctrl+C를 누르면, 프로그램은 지금 rate.sleep()의 **대기 상태(Sleep)** 에 머물러 있을 확률이 99%입니다. \
    while 문의 한계: rate.sleep() 함수 내부에 진입해 있는 동안에는 다음 줄로 넘어가지 못하므로, while 문의 조건식(rospy.is_shutdown())을 재평가할 기회가 없습니다. \
    except의 역할: 이때 rospy 시스템이 강제로 ROSInterruptException을 발생시켜서 sleep() 함수를 탈출시킵니다. 즉, **"루프 조건문이 확인하기 전에 지금 당장 멈춰야 해!"** 라고 예외를 던져서 즉시 루프 밖으로 튕겨 내는 것입니다.
 - try-except가 없으면 생기는 일 \
    만약 try-except 블록이 없다면, rate.sleep()에서 발생한 예외가 talker() 함수 밖으로 전달되고, 파이썬 인터프리터는 이를 **'처리되지 않은 치명적인 에러(Unhandled Exception)'** 로 간주합니다.

Add the following to your CMakeLists.txt. This makes sure the python script gets installed properly, and uses the right python interpreter.
```
catkin_install_python(PROGRAMS scripts/talker.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
```




# Writing the Subscriber Node
```
$ roscd beginner_tutorials/scripts/
$ wget https://raw.github.com/ros/ros_tutorials/kinetic-devel/rospy_tutorials/001_talker_listener/listener.py
$ chmod +x listener.py
```

File content:
```python
#!/usr/bin/env python
import rospy
from std_msgs.msg import String

# listener.py is similar to talker.py, except we've introduced a new callback-based mechanism for subscribing to messages.
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    # declares that your node subscribes to the chatter topic which is of type std_msgs.msgs.String. When new messages are received, callback is invoked with the message as the first argument.
    rospy.Subscriber("chatter", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
```

*rospy.Subscriber는 알아서 받은 정보를 callback함수의 첫번째 인자로 넣는가?
rospy.Subscriber는 데이터를 받았을 때, 그 메시지 객체를 자동으로 callback 함수의 첫 번째 인자로 전달합니다. \
이것이 가능하게 만드는 핵심 원리는 콜백(Callback) 함수 등록 방식에 있습니다.

 - Subscriber의 동작 방식 \
    1. 등록: ROS 시스템에 "나 chatter라는 토픽에서 String 타입 메시지를 기다릴 거야. 메시지가 오면 callback 함수를 실행해줘"라고 등록합니다.
    2. 대기: 시스템이 해당 토픽에서 메시지를 감지합니다.
    3. 호출: 메시지가 들어오면, rospy가 미리 등록된 callback 함수를 찾습니다. 이때 받은 메시지 객체를 자동으로 생성하여 호출하는 함수에 인자로 넘겨줍니다.
 - 함수 인자 이해하기 \
    callback(data)라고 정의하셨죠? \
    여기서 data는 실제로 수신된 메시지 객체(std_msgs/String 타입)가 됩니다. \
    따라서 data.data라고 하면, String 메시지 내부에 포함된 실제 문자열 값에 접근하게 되는 것입니다.

edit the catkin_install_python() call in your CMakeLists.txt so it looks like the following:
```
catkin_install_python(PROGRAMS scripts/talker.py scripts/listener.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
```




# Building your nodes
We use CMake as our build system and, yes, you have to use it even for Python nodes. \
This is to make sure that the autogenerated Python code for messages and services is created.

```
$ cd ~/catkin_ws
$ catkin_make
```




# Examining the Simple Publisher and Subscriber

### Running the Publisher
```
roscore
```

**catkin specific** \
If you are using catkin, make sure you have sourced your workspace's setup.sh file after calling catkin_make but before trying to use your applications:
```
# In your catkin workspace
$ cd ~/catkin_ws
$ source ./devel/setup.bash
```

```
$ rosrun beginner_tutorials talker      (C++)
$ rosrun beginner_tutorials talker.py   (Python)
```

### Running the Subscriber
```
$ rosrun beginner_tutorials listener     (C++)
$ rosrun beginner_tutorials listener.py  (Python) 
```