#include <ros/ros.h>
#include <sensor_msgs/LaserScan.h>
#include <std_msgs/String.h>
#include <geometry_msgs/Pose.h>
#include <nav_msgs/Odometry.h>
#include <tf/transform_listener.h>
#include <dynamic_reconfigure/server.h>
#include <vector>
#include <string>
#include <iostream>
#include <algorithm>
#include <memory>
#include <thread>

namespace smb_highlevel_controller {
    class SmbHighlevelController;
}

void processLaserScan(const sensor_msgs::LaserScan::ConstPtr& scan_message) {
    ROS_INFO("Received new LaserScan message");

    const std::vector<float>& range_data = scan_message->ranges;

    if (range_data.empty()) {
        ROS_WARN("Received an empty range data array.");
        return;
    }

    float closest_distance = range_data[0];
    for (size_t i = 1; i < range_data.size(); ++i) {
        if (range_data[i] < closest_distance) {
            closest_distance = range_data[i];
        }
    }

    ROS_INFO("Closest object distance: %.2f meters", closest_distance);
}

int main(int argc, char** argv) {
    ros::init(argc, argv, "highlevel_control_node");

    ros::NodeHandle nh("~");

    ROS_INFO("High-level control node has started");

    std::string laser_topic = "/scan";

    ros::Subscriber laser_subscriber = nh.subscribe(laser_topic, 100, processLaserScan);

    smb_highlevel_controller::SmbHighlevelController controller(nh);

    ros::spin();

    return 0;
}

