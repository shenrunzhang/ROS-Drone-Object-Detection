#include <ros/ros.h>
#include <darknet_ros_msgs/BoundingBoxes.h>

void detection_cb(const darknet_ros_msgs::BoundingBoxes::ConstPtr& msg)
{	
	//rest of callback function code
    for(int i=0; i< msg->bounding_boxes.size();i++){
        ROS_INFO("%s detected", msg->bounding_boxes[i].Class.c_str());
    }
}

int main(int argc, char **argv)
{
	ros::init(argc, argv, "detection_sub");
	ros::NodeHandle n;
	//rest of code will go here 
    ros::Subscriber sub = n.subscribe("/darknet_ros/bounding_boxes", 
        1, detection_cb); // nodehandle subscribes to a topic, specify buffer rate, and then  name of callback function
    
    ros::spin();


	return 0;
}

