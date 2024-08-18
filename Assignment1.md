> First 

* I first installed the smb_common zipped folder from the course website.
* Then I made a new directory in my home directory named catkin_ws ans initialized the workspace using **catkin_init**.
* Then I made a source directory.
* Then created a package called *smb_ws* using **catkin_create_pkg smb_ws**.
* Then I build the workspace using **catkin build**.
* I unzipped the downloaded file using **unzip smb_common.zip** from the downloads directory.
* Move the unzipped folder to ~/git using **mv smb_common ~/git/**
* Moved to *smb_ws* directory.
* Created a symlink using **ln -s ~/git/smb_common smb_common**.
* Then went to *smb_ws*.
* Built the workspace using **catkin_make**.
* Sourced the workspace using **source devel/setup.bash**.

> For second-

* Launched the smb_gazebo package using commabd "roslaunch smb_gazebo smb_gazebo.launch"
* Once the simulation is running, use **rosnode list** and **rostopic list** to find the currently active nodes and available topics.
* To observe the data being published to the **/cmd_vel** topic, run **rostopic echo /cmd_vel**.
* Finally used rqt_graph to check all nodes and topics.

> Third-

* Used rostopic pub /cmd_vel geometry_msgs/Twist "Linear: X:0.0
							y:1.0
							z:0.0
						angular:
							x:0.0
							y:0.0
							z:1.0"
Bot started moving circle on the gazebo.

> Fourth-

* I cloned the **teleop_twist_keyboard** repository using the **git clone** command.
* To start the **teleop_twist_keyboard** node, I ran:  **rosrun teleop_twist_keyboard teleop_twist_keyboard.py**.
* I can now control the bot through the keys on my keyboard.

> Fifth-
 
* Made a launch file to launch gazebo.

<launch>
<include file="$(find smb_gazebo)/launch/smb_gazebo.launch">
        <arg name="world_file" value="/usr/share/gazebo-11/worlds/robocup14_spl_field.world"/>
 </include>
</launch>


