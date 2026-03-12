# msg and srv
**msg:** 
 - Simple text files that describe the fields of a ROS message. 
 - Used to generate source code for messages in different languages.
 - stored in the msg directory of a package.

**srv:** 
 - srv file describes a service.
 - Composed of two parts: a request and a response.
 - stored in srv directory.

# msg
msgs are just simple text files with a field type and field name per line. \
possible field types
 - int8, int16, int32, int64 (plus uint*)
 - float32, float64
 - string
 - time, duration
 - other msg files
 - variable-length array[] and fixed-length array[C]
 - **Header** : contains a timestamp and coordinate frame information that are commonly used in ROS. 

e.g.
```
Header header
string child_frame_id
geometry_msgs/PoseWithCovariance pose
geometry_msgs/TwistWithCovariance twist
```

### How to create msg
```
$ roscd beginner_tutorials
$ mkdir msg
$ echo "int64 num" > msg/Num.msg
```
하면
```
root@7da0021d5679:~/catkin_ws/src/beginner_tutorials# ls
CMakeLists.txt  include  launch  msg  package.xml  src
root@7da0021d5679:~/catkin_ws/src/beginner_tutorials# cd msg
root@7da0021d5679:~/catkin_ws/src/beginner_tutorials/msg# ls
Num.msg
```
이렇게 생김.

msg files가 C++, Python, and other languages의 source code로 변환될 수 있는지 알아보아야 한다.

Open `package.xml`, and make sure these two lines are in it and uncommented:
```
  <build_depend>message_generation</build_depend> # Build time에 필요함
  <exec_depend>message_runtime</exec_depend> # Run time에 필요함
```

`CMakeLists.txt`에서 `find_package` call에 `message_generation`을 추가.
simply add `message_generation` to the list of `COMPONENTS`
```
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)
```

Make sure you export the message runtime dependency.
```
catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES beginner_tutorials
   CATKIN_DEPENDS roscpp rospy std_msgs message_runtime # 이 부분 주석 풀고 message_runtime 추가
#  DEPENDS system_lib
)
```

Find the following block of code:
```
# add_message_files(
#   FILES
#   Message1.msg
#   Message2.msg
# )
```
이거를 주석 풀고
```
add_message_files(
  FILES
  Num.msg
)
```

### 그래서 위에서 뭘 한걸까?
1. catkin_package(...) 함수는 **"이 패키지를 다른 패키지가 가져다 쓸 때, 어떤 것들이 반드시 함께 설치되어 있어야 하는가?"** 를 정의하는 아주 중요한 부분

    왜 message_runtime이 필요한가요?
    - 우리가 만든 Num.msg를 빌드하면, catkin은 이 파일을 기반으로 C++이나 Python 코드를 자동으로 생성합니다.
    - message_generation: 메시지 파일을 컴파일(생성)할 때 필요합니다.
    - message_runtime: 생성된 메시지를 프로그램이 실행될 때 실제로 불러와서 사용하기 위해 필요합니다.

    왜 CATKIN_DEPENDS에는 message_generation이 없어도 될까?
    - catkin_package()의 CATKIN_DEPENDS는 **"내 패키지를 가져다 쓰는 '다른' 패키지에게 필요한 것이 무엇인가?"** 를 정의하는 곳입니다.
    - message_generation (빌드용 도구): 메시지 파일(.msg)을 읽어서 C++/Python 코드로 **번역(생성)** 할 때만 필요한 도구입니다. 일단 번역이 끝나면 더 이상 필요 없습니다.
    - message_runtime (실행용 라이브러리): 번역된 메시지 코드가 실제로 프로그램 안에서 돌아갈 때 필요한 최소한의 라이브러리입니다.

2. 메시지를 제대로 사용하려면 CMakeLists.txt에서 다음 세 곳을 모두 확인해야 한다.
 - `find package`: `message_generation`이 포함되어야 한다.
 - `add_message_files` & `generate_messages`: 주석을 풀고 파일을 지정해야 합니다.
 - `catkin_package`: 방금 질문하신 `message_runtime`을 추가하는 부분입니다.

`message_generation` vs `generate_messages` 
 - message_generation (패키지 이름) \
    정체: ROS 패키지 중 하나입니다. \
    용도: find_package()에서 찾거나 package.xml에 적을 때 사용합니다. "메시지를 만들어내는 기능을 가진 도구 상자"를 가져오는 행위입니다.

 - generate_messages (CMake 함수/명령어) \
    정체: 실제로 메시지 생성을 수행하라는 **명령(Action)**입니다. \
    용도: CMakeLists.txt 안에서 호출합니다. "아까 가져온 도구 상자를 열어서, 진짜로 코드를 뽑아내(Generate)!"라고 명령하는 것입니다.

**FILES** 랑 **DEPENDENCIES** 는 그냥 매크로임 \
`find_package`에서 `message_generation`은 진짜 파일인가? \
--> /opt/ros/noetic/share/message_generation 임. (패키지다)

`message_generation`은 `src` folder아래 `msg` folder나 `*.msg` 파일을 인식하는건가?
 - message_generation은 이름 그대로 **'생성기(Engine)'** 일 뿐입니다. 엔진은 스스로 능동적으로 내 프로젝트 폴더를 뒤져서 .msg 파일을 찾아내지 않습니다.
 - add_message_files(...): "내 폴더의 msg 폴더 안에 있는 Num.msg를 빌드 리스트에 등록해라." \
    *add_message_files 함수 내부적으로 **"메시지 파일은 무조건 msg 폴더에 있다"**라 는 규칙이 하드코딩(Default) 된 것은 **ros 표준 디렉토리 레이아웃**이다.
 - generate_messages(...): "등록된 그 파일들을 message_generation 엔진을 사용해서 C++/Python 코드로 변환(생성)해라."

`add_message_files`를 똑같이 적어야 하나? `add_message`라고 쓰면 안돼?
 - 안된다.
 - message_generation 패키지의 역할 (정확히는 '매크로')
    - message_generation 패키지 안에는 **add_message_files.cmake**와 generate_messages.cmake 같은 파일들이 들어있습니다.
    - 우리가 find_package(message_generation ...)을 호출하면, 이 패키지 안에 숨어있던 함수(정확히는 매크로)들이 메모리에 로드(Load) 됩니다.
    - 즉, message_generation 패키지가 이 함수들을 **'제공'** 하고, 우리가 그 함수를 **'호출'** 하는 것입니다.

### `rosmsg show [message type]`으로 확인하기
```
$ rosmsg show beginner_tutorials/Num
>>> int64 num
```
message type consists of two parts:
 - beginner_tutorials -- the package where the message is defined
 - Num -- The name of the msg Num.

If you can't remember which Package
```
$ rosmsg show Num
>>>
[beginner_tutorials/Num]:
int64 num
```




# Recompile
```
$ roscd beginner_tutorials
$ cd ../..
$ catkin_make
$ cd -
```




# srv
srv files are just like msg files, except they contain two parts: a request and a response. \
The two parts are separated by a '---' line

e.g.
```
# A, B are request, Sum is response
int64 A
int64 B
---
int64 Sum
```

### how to create srv
```
$ roscd beginner_tutorials
$ mkdir srv
$ roscp rospy_tutorials AddTwoInts.srv srv/AddTwoInts.srv
```
We need to make sure that the srv files are turned into source code for C++, Python, and other languages.

Need the same changes to `package.xml` for services as for messages, so look above for the additional dependencies required.

`CMakeLists.txt`도 수정해야 한다.
```
## Generate services in the 'srv' folder
add_service_files(
    FILES
    AddTwoInts.srv
)
```

### `rossrv show <service type>`
```
$ rossrv show beginner_tutorials/AddTwoInts
# You will see:

int64 a
int64 b
---
int64 sum
```
AddTwoInts만 치면
```
root@7da0021d5679:~/catkin_ws/src/beginner_tutorials# rossrv show AddTwoInts
[rospy_tutorials/AddTwoInts]:
int64 a
int64 b
---
int64 sum

[beginner_tutorials/AddTwoInts]:
int64 a
int64 b
---
int64 sum
```
처럼 뜨는데, first is the one you just created in the beginner_tutorials package, and the second is the pre-existing one from the rospy_tutorials package.




# About language
Any .msg file in the msg directory will generate code for use in all supported languages. 
 - The C++ message header file will be generated in ~/catkin_ws/devel/include/beginner_tutorials/
 - The Python script will be created in ~/catkin_ws/devel/lib/python2.7/dist-packages/beginner_tutorials/msg. 
 - The lisp file appears in ~/catkin_ws/devel/share/common-lisp/ros/beginner_tutorials/msg/.

Similarly, any .srv files in the srv directory will have generated code in supported languages. 
 - For C++, this will generate header files in the same directory as the message header files. 
 - For Python and Lisp, there will be an 'srv' folder beside the 'msg' folders.