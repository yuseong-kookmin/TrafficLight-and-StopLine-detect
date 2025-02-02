# TrafficLight-and-StopLine-detect

## Overview

This repository contains two Python scripts designed to detect traffic lights and stop lines using computer vision techniques with OpenCV and ROS (Robot Operating System).

## 1. video_mouse_event.py

Description: This script allows users to click on a video frame to get the HSV and BGR values of the selected pixel. It helps fine-tune the HSV color ranges required for accurate traffic light detection.

Usage: Run the script and click on the video display to get pixel color information.

## 2. traffic_light_and_stop_line.py

Description: This ROS node subscribes to a camera feed and processes the images to detect the color of traffic lights and the presence of stop lines. It determines whether the vehicle should stop based on these detections and publishes the result to a ROS topic.

Key Features:

Traffic Light Detection: Identifies green lights to determine when to proceed.

Stop Line Detection: Detects stop lines using grayscale thresholding.

ROS Integration: Subscribes to /usb_cam/image_raw and publishes to is_stop topic.



Adjust the HSV ranges and ROI settings as needed based on your environment for optimal detection accuracy.
