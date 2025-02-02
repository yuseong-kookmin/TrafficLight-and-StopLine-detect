import cv2
import numpy as np

# 전역 변수 선언
click_x, click_y = -1, -1

def mouse_callback(event, x, y, flags, param):
    global click_x, click_y
    if event == cv2.EVENT_LBUTTONDOWN:
        click_x, click_y = x, y
        print(f"Clicked at: ({click_x}, {click_y})")

def main(video_path):
    cv2.namedWindow('Video')
    cv2.setMouseCallback('Video', mouse_callback)
    
    video = cv2.VideoCapture(video_path)
    
    while video.isOpened():
        ret, frame = video.read()
        
        if not ret:
            break
        
        # 클릭된 좌표가 유효한 경우 HSV 값 출력
        if click_x >= 0 and click_y >= 0:
            pixel_bgr = frame[click_y, click_x]
            pixel_hsv = cv2.cvtColor(np.uint8([[pixel_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
            print(f"Pixel at ({click_x}, {click_y}): BGR={pixel_bgr}, HSV={pixel_hsv}")
        
        cv2.imshow('Video', frame)
        
        key = cv2.waitKey(30)
        if key == 27:  # ESC 키를 누르면 종료
            break
    
    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main("red_light.mp4")
