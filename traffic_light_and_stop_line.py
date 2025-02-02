from sensor_msgs.msg import Image
import rospy
from cv_bridge import CvBridge
from std_msgs.msg import Bool
import cv2
import numpy as np

is_stopline = False
is_stop = False

# 이미지 콜백 함수
def image_callback(msg):
    try:
        # ROS 이미지 메시지를 OpenCV 이미지로 변환
        bridge = CvBridge()
        image = bridge.imgmsg_to_cv2(msg, "bgr8")
        
        process_videos(image)
      
        cv2.imshow("USB Camera Image", image)
        cv2.waitKey(1)  # 1밀리초 동안 대기

    except Exception as e:
        print(e)
        
     
     
def detect_traffic_light_color(frame):    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 대회 중에 HSV 범위 조정
    green_on_lower = np.array([70, 100, 200])
    green_on_upper = np.array([100, 255, 255])
    
    green_off_lower = np.array([70, 100, 50])
    green_off_upper = np.array([100, 255, 100])
    
    green_on_mask = cv2.inRange(hsv_frame, green_on_lower, green_on_upper)
    green_off_mask = cv2.inRange(hsv_frame, green_off_lower, green_off_upper)
    
    green_on_count = cv2.countNonZero(green_on_mask)
    green_off_count = cv2.countNonZero(green_off_mask)
    
    is_green = green_on_count > 150

    return is_green


def detect_stop_line(frame):
    # 대회 중에 ROI 범위 조정
    img_roi = frame
    
    img_gray = cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)
    retval, img_binary = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

    white_count = cv2.countNonZero(img_binary)

    # ROI 범위에 따라 적당히 조정
    is_stopline = white_count > 9000

    return is_stopline


def process_videos(image):
    
        global is_stop
        traffic_light_frame = image
        roi_traffic_light_frame = traffic_light_frame[160:320,0:120] #620:480
   
        cv2.imshow('roi',roi_traffic_light_frame)

        is_green = detect_traffic_light_color(roi_traffic_light_frame)
        
        is_stopline = detect_stop_line(image)

        print(f" is_green: {is_green}, is_stopline: {is_stopline}", end = ' ')

        
        is_stop = False
        
        if is_stopline:
            if is_green:
                is_stop = False
            else:
                is_stop = True
        else:
            is_stop = False  # Provide a default value if is_stopline is False

        print(f"is_stop: {is_stop}")
            
        talker(is_stop)
	
        # 프레임을 화면에 표시
        cv2.imshow('Traffic Light', traffic_light_frame)
        #cv2.imshow('Stop Line', stop_line_frame)

        key = cv2.waitKey(100)   # 키보드 입력 대기 (영상 속도 조절)
         
       
def listener():
    rospy.init_node('usb_cam_subscriber', anonymous=True)
    
    # 이미지 토픽 구독자 설정
    rospy.Subscriber("/usb_cam/image_raw", Image, image_callback)
    
    rospy.spin()
    
def talker(is_stop):
    
    pub = rospy.Publisher('is_stop', Bool,queue_size = 10)
        # is_stop 토픽으로 메시지 발행
    pub.publish(is_stop)
        

if __name__ == '__main__':
    listener()
