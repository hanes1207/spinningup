# 서버에서 도커 돌리는 법..
구성: (맥북) ------ (서버   (도커))

```
docker run -it --name euiseok_test \
 --runtime=nvidia \
 --privileged \
 --gpus 'all,"capabilities=compute,utility,graphics,display"' \
 --device /dev/dri:/dev/dri \
 --shm-size=32G \
 --net=host \
 -e HOST_UID=$(id -u) \
 -e NVIDIA_VISIBLE_DEVICES=all \
 -e NVIDIA_DRIVER_CAPABILITIES=all \
 -e MUJOCO_GL=egl \
 -e PYOPENGL_PLATFORM=egl \
 -e DISPLAY=$DISPLAY \
 -v /tmp:/tmp \
 -v ~/.Xauthority:/root/.Xauthority:rw \
 -v /mnt/hdd/intern/euiseok_workspace:/workspace \
 -w /workspace \
 ubuntu:20.04 /bin/bash
```
**환경변수에 HOST_UID를 넣어주어야 한다.**
디스플레이 출력이 안되는 것은 대부분 권한 문제이다.

서버에 x11 설치가 되어있지 않는 경우, 아무리 ` -v /tmp/.X11-unix:/tmp/.X11-unix \`를 해봤자 도움이 되지 않는다. (안에 아무것도 없음)

` -v /tmp:/tmp \`로 연결해주자.

### root에서 user 만드는 법
```
groupadd -g 1000 user
useradd -m -u 1000 -g 1000 -s /bin/bash user
```
필요 시 `root`와 `user` 모두 비밀번호를 설정해주자. 

User에게 sudo 권한을 주는 방법은 root로 접속해서 \
`echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers`

또한 root에서 entrypoint를 설정해주어야 한다. \
`vim /usr/local/bin/entrypoint.sh` 파일을 다음과 같이 만든다.
```
#!/bin/bash

HOST_UID=1029
USER_ID=${HOST_UID}
GROUP_ID=${HOST_UID}

echo "Starting container with UID: $USER_ID, GID: $GROUP_ID"

# Force change the UID and GID of the internal 'user' to match the host
groupmod -o -g "$GROUP_ID" user
usermod -o -u "$USER_ID" -g "$GROUP_ID" user

# Change ownership of the mounted workspace to prevent permission issues
chown -R user:user /workspace

# Drop root privileges, switch to user, and execute the passed command
exec gosu user "$@"
```




## 서버에 x11 없을 때 x11 구성하기
SSH X11 forwarding이 만든 Unix socket을 컨테이너에 공유 \
`ls /tmp/ssh-*/agent.X`를 연결해주어야 하는데 \
Docker 컨테이너 구성할 때 `-v /tmp:/tmp \`가 이미 해줌.

환경변수 `$XAUTHORITY`도 맞춰주어야 한다. \
`export XAUTHORITY=~/.Xauthority`

### Gazebo가 터지는 이유
XQuartz는 OpenGL(GLX) 제대로 지원 안 함
특히 remote + Docker 환경에서는 거의 100% 깨짐




## Gazebo를 GUI에서 돌리고 싶다면... --> VNC
Docker 안에서 GUI → VNC → Mac 브라우저

- 패키지 설치
```
apt update
apt install -y \
  xvfb \
  x11vnc \
  fluxbox \
  xterm \
  net-tools
```

- VNC용 디스플레이 생성
```
export DISPLAY=:1
Xvfb :1 -screen 0 1920x1080x24 &
```

- 윈도우 매니저 실행
`fluxbox &`

- VNC 서버 실행
`x11vnc -display :1 -forever -nopw -listen 0.0.0.0 -xkb &`

- 테스트용 창
`xterm &`

### 접속 (맥에서)
RealVNC 다운받고

VNC 클라이언트에서 `server-ip:5900`

- 근데도 터진다. 왜지?
지금 구조: `Xvfb (:1) + VNC` \
Xvfb는 기본적으로 OpenGL 지원 없음 \
swrast (software renderer) 필요 \
근데 그것도 설치 안 돼 있음