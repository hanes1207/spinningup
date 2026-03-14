# Writing a Service Node
```
$ roscd beginner_tutorials
```

Create the scripts/add_two_ints_server.py file within the beginner_tutorials package and paste the following inside it:
```python
#!/usr/bin/env python

from __future__ import print_function

from beginner_tutorials.srv import AddTwoInts,AddTwoIntsResponse
import rospy

def handle_add_two_ints(req):
    print("Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b)))
    return AddTwoIntsResponse(req.a + req.b)

def add_two_ints_server():
    # We declare our node using init_node() and then declare our service:
    rospy.init_node('add_two_ints_server')

    # declares a new service named add_two_ints with the AddTwoInts service type. All requests are passed to handle_add_two_ints function.
    # handle_add_two_ints is called with instances of AddTwoIntsRequest and returns instances of AddTwoIntsResponse.
    s = rospy.Service('add_two_ints', AddTwoInts, handle_add_two_ints)
    print("Ready to add two ints.")

    # rospy.spin() keeps your code from exiting until the service is shutdown.
    rospy.spin()

if __name__ == "__main__":
    add_two_ints_server()
```

*난 AddTwoIntsRequest랑 AddTwoIntsResponse 인스턴스를 위한 코드를 작성한 기억이 없는데?
 - 자동 생성의 마법: gencpp & genpy \
    당신이 AddTwoInts.srv라는 파일을 만들고 빌드(catkin_make)를 하는 순간, ROS의 빌드 도구는 내부적으로 다음과 같은 과정을 거칩니다.
    1. 파일 분석: srv/AddTwoInts.srv 파일을 읽어서 어떤 필드(예: int64 a, int64 b)가 있는지 확인합니다.
    2. 코드 자동 생성: 이 필드 정보를 바탕으로 파이썬(또는 C++) 소스 코드를 생성합니다.
        AddTwoIntsRequest: 요청할 때 보낼 데이터를 담는 그릇 (a, b)
        AddTwoIntsResponse: 응답으로 받을 데이터를 담는 그릇 (sum)
    3. 파일 배치: 이 코드들을 devel/lib/python3/dist-packages/beginner_tutorials/srv/ 폴더 내에 .py 파일로 저장합니다.
 - 어떻게 생성하나요? \
    규칙은 매우 간단합니다. .srv 파일 이름 뒤에 Request와 Response라는 단어만 붙이면 됩니다. \
    1. .srv 파일 정의:
        ```
        int64 a
        int64 b
        ---
        int64 sum
        ```
    2. 자동 생성되는 파이썬 클래스 구조:
        ```python
        # ROS가 알아서 만들어둔 코드의 예시
        class AddTwoIntsRequest:
            def __init__(self, a=0, b=0):
                self.a = a
                self.b = b

        class AddTwoIntsResponse:
            def __init__(self, sum=0):
                self.sum = sum
        ```
 - 왜 이렇게 하나요? (데이터 규격화) \
    만약 ROS가 이런 클래스를 자동으로 안 만들어준다면, 개발자는 통신을 위해 매번 dictionary나 list 형태로 데이터를 직접 묶고 풀어야 할 것입니다. 그러면 다른 사람이 만든 노드와 통신할 때 데이터 구조가 맞지 않아 고생하게 되겠죠.
    1. 표준화: ROS가 코드를 자동으로 생성함으로써, 어떤 언어를 쓰든(C++, Python 등) 항상 동일한 인터페이스(AddTwoIntsRequest 객체)를 사용하게 보장합니다.
    2. 타입 안전성: 실수로 a 대신 x라는 변수를 넣으면 에러를 띄워주어 디버깅을 쉽게 만들어줍니다.

Don't forget to make the node executable:
```
chmod +x scripts/add_two_ints_server.py
```

Add the following to your CMakeLists.txt. This makes sure the python script gets installed properly, and uses the right python interpreter.
```
catkin_install_python(PROGRAMS scripts/add_two_ints_server.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
```




# Writing a Client Node
Create the scripts/add_two_ints_client.py file within the beginner_tutorials package and paste the following inside it:
```python
#!/usr/bin/env python

from __future__ import print_function

import sys
import rospy
from beginner_tutorials.srv import *

def add_two_ints_client(x, y):
    # client code for calling services is also simple. For clients you don't have to call init_node(). We first call:
    # Blocks until the service named add_two_ints is available.
    rospy.wait_for_service('add_two_ints')

    try:
        # create a handle for calling the service
        # 우리가 service type을 AddTwoInts로 정했기 때문에, rospy.ServiceProxy('add_two_ints', AddTwoInts)는 "서비스를 호출할 수 있는 호출 가능한(Callable) 객체(일종의 함수)" 객체를 반환한다.
        add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts)
        
        # We can use this handle just like a normal function and call it:
        # Return value is an AddTwoIntsResponse object. If the call fails, a rospy.
        # ServiceException may be thrown, so you should setup the appropriate try/except block.
        resp1 = add_two_ints(x, y)
        return resp1.sum
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 3:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
    else:
        print(usage())
        sys.exit(1)
    print("Requesting %s+%s"%(x, y))
    print("%s + %s = %s"%(x, y, add_two_ints_client(x, y)))
```

*서비스를 호출할 수 있는 호출 가능한(Callable) 객체(일종의 함수)은 함수포인터인가? \
함수 포인터 vs 파이썬의 Callable
 - C/C++ 함수 포인터: 메모리 상에서 특정 함수가 시작되는 주소값을 가리킵니다. 그 주소로 점프해서 코드를 실행하는 방식이죠.
 - 파이썬의 ServiceProxy 객체: 내부적으로 __call__이라는 특별한 메서드를 가지고 있는 **객체(Object)** 입니다. 파이썬에서 객체 이름 뒤에 ()를 붙여서 호출하면, 파이썬은 내부적으로 그 객체의 **\_\_call\_\_** 메서드를 실행합니다.

Don't forget to make the node executable:
```
$ chmod +x scripts/add_two_ints_client.py
```

edit the catkin_install_python() call in your CMakeLists.txt so it looks like the following:
```
catkin_install_python(PROGRAMS scripts/add_two_ints_server.py scripts/add_two_ints_client.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
```




# Building your nodes
We use CMake as our build system and, yes, you have to use it even for Python nodes.
```
# In your catkin workspace
$ cd ~/catkin_ws
$ catkin_make
```




# Examining the Simple Service and Client

### Running the Service
Let's start by running the service:

```
$ rosrun beginner_tutorials add_two_ints_server     (C++)
$ rosrun beginner_tutorials add_two_ints_server.py  (Python) 
```

You should see something similar to:
```
Ready to add two ints.
```

### Running the Client
```
$ rosrun beginner_tutorials add_two_ints_client 1 3     (C++)
$ rosrun beginner_tutorials add_two_ints_client.py 1 3  (Python) 
```

You should see something similar to:
```
Requesting 1+3
1 + 3 = 4
```