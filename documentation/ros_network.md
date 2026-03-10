# Network Setup
ref: https://wiki.ros.org/ROS/Tutorials/UnderstandingNodes \
ref: https://wiki.ros.org/ROS/NetworkSetup#Single_machine_configuration

$ROS_HOSTNAME이 없다면 Network Setup - Single Machine Configuration을 해줘야 함

### 모든 node들이 directly bi-connected여야 하나?
ROS에서 노드들이 반드시 직접(Directly) bi-connected(양방향 연결)될 필요는 없다.
오히려 ROS의 강력한 점은 **간접적인 연결(Pub/Sub 모델)**을 통해 노드 간의 결합도(Coupling)를 낮추는 데 있다.

Pub/Sub (Publisher/Subscriber)이란?: 노드 A가 노드 B를 직접 호출하는 방식(Client/Server의 개념과는 다름)이 아니라, 노드 A가 데이터를 **토픽(Topic)** 이라는 가상의 채널에 던져놓으면, 노드 B가 그 채널을 구독(Subscribe)하는 방식입니다.

간접 연결의 장점:
 - 분리성: 노드 A는 노드 B가 존재하는지조차 알 필요가 없습니다.
 - 확장성: 노드 C, D가 추가되어도 노드 A는 아무런 수정 없이 그대로 데이터를 뿌리면 됩니다.
 - 우회 가능: 데이터를 전달하는 과정에서 rosbridge나 ros_relay 같은 노드를 거쳐서 통신할 수도 있습니다.

"우회해서 연결"되는 대표적인 사례
 - 브릿지(Bridge) 노드: 예를 들어, 인터넷 환경을 통해 외부의 컴퓨터와 통신할 때, 중간에 rosbridge_server 같은 노드를 두어 메시지를 변환하고 우회해서 전달합니다.
 - 토픽 릴레이(Topic Relay): 대역폭을 줄이거나 특정 노드 간의 연결을 제어하기 위해, 노드 A → 릴레이 노드 → 노드 B 순서로 데이터를 전달하기도 합니다.
 - 마스터(Master/Discovery): 노드들은 서로를 직접 찾지 않고 roscore(또는 ROS 2의 Discovery 서비스)를 통해 서로의 위치를 확인합니다. 즉, 마스터를 통해 **"소개팅"** 을 하고 나면 그때부터 직접 통신을 시작하는 방식입니다.

직접 연결이 필요하다면..
 - 만약 **"직접 응답을 주고받아야 하는 경우"** 라면 Service나 Action 인터페이스를 사용합니다. 이때는 노드 간의 1:1 직접 통신이 발생합니다. 하지만 이조차도 ROS 마스터가 연결 주소를 연결해 주는 '중개' 과정을 거칩니다.

### Loopback test: Self ping test
if fail...
 - ping 127.0.0.1(localhost 주소)은 성공하는데, ping hal만 실패하는 경우 \
 이건 **"주소록(DNS/hosts 파일)이 없어서 hal이라는 이름의 전화번호를 모르는 상태"** 입니다. 네트워크 기능은 정상이지만, hal이라는 별명이 어떤 IP를 가리키는지 컴퓨터가 모르는 것이죠. \
 해결법: `/etc/hosts` 파일을 수정.
    ```
    # /etc/hosts 파일에 내 컴퓨터 IP와 이름을 등록
    echo "127.0.0.1 hal" >> /etc/hosts
    ```
 - ping 127.0.0.1 조차 실패하는 경우
 이건 네트워크 스택 자체가 죽었거나, 격리된 컨테이너 환경에서 네트워크 인터페이스가 제대로 활성화되지 않은 상태입니다. \
    1. 도커 컨테이너 실행 시 --net=none으로 실행했거나, 가상 네트워크 인터페이스가 초기화되지 않았을 때 발생합니다.
    2. 리눅스 커널 수준에서 루프백 인터페이스(lo)가 down 되어 있는 상태입니다.
 확인법: ip link 또는 ifconfig를 입력했을 때 lo 인터페이스가 있는지, 그리고 UP 상태인지 보세요.
    ```
    Bash
    ip link show lo
    LOWER_UP이 보이지 않는다면, 아래 명령어로 살려야 합니다:
    ```
    ```
    Bash
    ip link set dev lo up
    ```




# Name resolution
When a ROS node advertises a topic, it provides a hostname:port combination (a URI) that other nodes will contact when they want to subscribe to that topic.

Hostname that a node provides can be used by all other nodes to contact it.

ROS client libraries use the name that the machine reports to be its hostname. This is the name that is returned by the command hostname.

### DHCP Address란 무엇인가?
**(Dynamic Host Configuration Protocol)** 는 공유기가 네트워크에 새로 들어온 기기에게 **"너는 이제부터 이 IP 주소를 써!"** 라고 자동으로 할당해 주는 시스템입니다.
 - 고정 IP (Static IP): 마치 내 집 주소처럼 바뀌지 않는 번호.
 - DHCP (Dynamic): 카페 와이파이에 연결할 때마다 서버가 그때그때 비어있는 번호를 빌려주는 것. (10.0.0.1 같은 주소는 이렇게 DHCP에 의해 부여받은 주소일 가능성이 높습니다.)

### Setting a name explicitly
"hostname을 IP로 resolve할 수 없다"는 게 무슨 뜻인가?

컴퓨터들은 서로 통신할 때 이름(marvin, hal, artoo)을 쓰길 원하지만, 실제 데이터는 IP 주소(10.0.0.1)를 타고 갑니다.

Resolve (이름 해석): artoo라는 이름을 들었을 때 "아, 그건 10.0.0.1이지!"라고 찾아내는 과정을 말합니다.

문제 상황: artoo가 DHCP로 주소를 받았는데, 공유기나 네트워크 관리 시스템이 다른 컴퓨터들에게 "새로 들어온 artoo가 10.0.0.1을 쓰고 있어"라고 알려주지 않았을 때 발생합니다.

Fix is to set `ROS_IP` in the environment before starting a node on artoo:
```
# artoo가 마스터에게 보고할 때, "내 이름은 artoo지만, 이름 대신 숫자 주소인 10.0.0.1로 나를 불러줘!"라고 명시하는 것이 바로 export ROS_IP=10.0.0.1입니다.
ssh 10.0.0.1 # We can't ssh to artoo by name
export ROS_IP=10.0.0.1 # Correct the fact that artoo's address can't be resolved
<start a node here>
```

If a machine's name is resolvable, but the machine doesn't know its own name. \
Artoo can be properly resolved into 10.0.0.1, but running hostname on artoo returns localhost. \
Then you should set ROS_HOSTNAME:
```
ssh artoo # We can ssh to artoo by name
export ROS_HOSTNAME=10.0.0.1 # Correct the fact that artoo doesn't know its name
<start a node here>
```

### Single machine configuration
you just want to run tests on your local machine (like to run the ROS Tutorials), set these environment variables:
```
$ export ROS_HOSTNAME=localhost
$ export ROS_MASTER_URI=http://localhost:11311
```

### Configuring /etc/hosts
Another option is to add entries to your /etc/hosts file so that the machines can find each other.

당신이 marvin 터미널에서 ping artoo를 쳤을 때, marvin은 artoo가 어느 IP에 있는지 찾지 못해서 **"알 수 없는 호스트입니다"** 라며 핑을 보낼 수 없게 됩니다.

ROS 노드들이 서로 대화하려면 "누가 누구인지" 이름과 IP를 정확히 알아야 하는데, artoo가 어디 있는지 모르면 통신이 아예 시작이 안됌.

이런 상황이 발생하면 수동으로 **"이름표"** 를 붙여주면 됩니다. 모든 기기의 /etc/hosts 파일에 정보를 적어주는 방식입니다.
```
# 모든 기기의 /etc/hosts 파일에 이렇게 적어줍니다
10.0.0.1 artoo
```

### Avahi 사용하기
기기들이 같은 네트워크에 묶여있다면 `.local`로 **mDNS (Multicast DNS)** 라는 방식을 쓸 수 있다.

동작 원리: 내 컴퓨터가 네트워크 전체에 **"누구 'ubuntu.local' 쓰는 사람 있어? 있으면 IP 주소 좀 알려줘!"** 라고 소리를 지릅니다(Multicast).

응답: 이름이 ubuntu인 기기가 그 소리를 듣고 **"어, 나야! 내 IP는 10.0.0.1이야"** 라고 대답합니다.

이 과정을 자동으로 처리해 주는 리눅스용 프로그램 이름이 바로 본문에 언급된 **Avahi(아바히)** 입니다. (Mac에서는 'Bonjour'라고 부릅니다.)

Avahi 서버 설정 확인하는 법
```
# running을 확인
$  systemctl is-active avahi-daemon.service

# restart avahi
$  systemctl restart avahi-daemon.service
```



# Multiple machines에서 ros를 구동시켜보자
ROS_MASTER_URI을 이용해서 multiple machines이 single master를 사용하게 해보자.

### well-written node makes no assumptions about where in the network it runs
Exception: Driver node that communicate with a piece of hardware must run on the machine to which the hardware is physically connected

드라이버 노드 vs 일반 노드 (역할의 분리)
 - 드라이버 노드 (Hardware Interface): 하드웨어와 **0과 1의 신호(USB, 시리얼, 이더넷 등)** 를 직접 주고받는 노드입니다. 당연히 장비와 물리적으로 연결된 컴퓨터에서 돌아야 합니다.
 - 나머지 노드 (Algorithm/Logic): 이 드라이버 노드가 읽어온 데이터를 토픽으로 발행(Publish)하면, **다른 컴퓨터(혹은 다른 프로세스)** 에 있는 노드들이 그 데이터를 구독(Subscribe)하여 처리합니다.

예시
 - 로봇 몸체(Jetson/라즈베리파이): 카메라, 라이더, 모터 제어기가 물리적으로 꽂혀 있습니다. 여기서 **'드라이버 노드'** 가 실행됩니다.
 - 지상 통제실(노트북): 여기에는 카메라나 모터가 꽂혀 있지 않습니다. 하지만 로봇이 발행하는 camera/image 토픽을 **네트워크(Wi-Fi)** 를 통해 구독하면, 마치 내 노트북에 카메라가 있는 것처럼 화면을 볼 수 있습니다.

요약
 - 하드웨어 드라이버: 장치가 꽂힌 컴퓨터에서 실행해야 한다. (필수)
 - 데이터 처리 노드: 장치가 안 꽂힌 컴퓨터에서도 원격으로 데이터를 받아 실행 가능하다. (분리 가능)
 - 네트워크: 물리적인 USB/시리얼 연결 대신, Wi-Fi나 이더넷으로 노드 간의 데이터를 주고받는다.

그래서 ROS가 **'분산 시스템(Distributed System)'** 이라고 불리는 것입니다. 로봇의 각 부품을 따로따로 관리하면서, 마치 한 덩어리인 것처럼 네트워크로 엮는 것이 ROS의 본질입니다.




# Appendix 1: ros와 관련없이 거대한 네트워크 속에서 내 장비에 loopback을 걸었는데 제대로 찍히면 내 장비에는 이상이 없는걸까?
네트워크 이론에서 루프백(Loopback) 테스트가 성공했다는 것은, 적어도 당신의 장비 내부에서는 **"네트워크 데이터를 처리할 준비가 완전히 끝났다"** 는 강력한 증거입니다.

**'내부 통신 계층'** 에 이상이 없다는 뜻.

### 루프백 성공이 의미하는 것
 - TCP/IP 스택: 운영체제의 네트워크 프로토콜 처리 기능이 정상.
 - 네트워크 인터페이스(NIC) 로직: OS가 자신의 가상 네트워크 카드(lo 인터페이스)를 제대로 인지하고 패킷을 주고받는 능력이 있음.
 - 드라이버 계층: 네트워크 카드 드라이버가 OS와 커널 수준에서 문제없이 통신 중임.

### "내 장비에 이상이 없다"는 말의 한계
루프백은 **'내부'** 만 확인. 실제 현장(실무)에서는 다음과 같은 문제는 여전히 남아있을 수 있습니다.
 - 물리적 인터페이스(NIC) 단절: 루프백은 소프트웨어적인 가상 통로를 쓰기 때문에, 실제 랜선이 꽂힌 포트나 와이파이 안테나(물리적 하드웨어)가 고장 났는지는 알 수 없습니다.
 - IP 할당 실패: 루프백은 127.0.0.1을 쓰지만, 외부와 통신하려면 실제 IP(예: 192.168.0.x)가 필요합니다. 이 IP를 제대로 할당받지 못했거나 공유기 설정이 꼬였다면 외부 통신은 불가능합니다.
 - 방화벽(Firewall): 내부에서는 잘 돌아가도, OS 방화벽(iptables, ufw 등)이 외부에서 들어오는 패킷을 차단하고 있을 수 있습니다.

### Loopback 이후 체크리스트
"내부"에서 "외부"로 나가는 과정을 점검해야 한다.
 - 물리적 연결 확인: ip addr 또는 ifconfig를 쳐서 내 장비에 실제 IP 주소가 할당되어 있는지 확인하세요.
 - 게이트웨이(Gateway) 확인: 내 장비가 밖으로 나가는 출구(공유기 등)와 통신 가능한지 확인하세요. (ping <게이트웨이_IP>)
 - 외부망 확인: 인터넷상의 DNS 서버에 핑을 날려보세요. (ping 8.8.8.8)




# Appendix 2: Firewall 이슈
need to create a virtual network to connect them. We recommend




# Appendix 3: Debugging network problems
Try roswtf and rqt_graph. \
roswtf: https://wiki.ros.org/roswtf \
rqt_graph: https://wiki.ros.org/rqt_graph




# Appendix 4: TF complaining about extrapolation into the future?
You may have a discrepancy in system times for various machines. \
You can check one machine against another using

`ntpdate -q other_computer_ip`

If there is a discrepancy, install chrony (for Ubuntu, sudo apt-get install chrony) \
Edit the chrony configuration file (/etc/chrony/chrony.conf) on one machine to add the other as a server.

For instance, on the PR2, computer c2 gets its time from c1 and thus has the following line:

`server c1 minpoll 0 maxpoll 5 maxdelay .05`

That machine will then slowly move its time towards the server. \
If the discrepancy is enormous, you can make it match instantly using
```
/etc/init.d/chrony stop
ntpdate other_computer_ip
/etc/init.d/chrony start
```
(as root) but large time jumps can cause problems, so this is not recommended unless necessary

**로봇 시스템을 운영할 때는 chrony가 항상 백그라운드에서 돌고 있어야 합니다. systemctl status chrony를 입력했을 때 active (running) 상태인지 항상 확인하세요!**