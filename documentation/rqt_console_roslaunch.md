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
