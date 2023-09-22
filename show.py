import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import *
import plus

def run():
    model = YOLO('yolov8s.pt')  # YOLO 모델 사용

    # 마우스의 현재 위치로 x, y 좌표값 출력 (영역 그릴 때 x, y 좌표값 확인용)
    def RGB(event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            colorsBGR = [x, y]
            print(colorsBGR)

    cv2.namedWindow('RGB')
    cv2.setMouseCallback('RGB', RGB)

    # 사용할 비디오 파일
    cap = cv2.VideoCapture('input/goalline.mp4')

    # 학습 클래스 불러오기
    my_file = open("yolov8/coco.txt", "r")
    data = my_file.read()
    class_list = data.split("\n")

    count = 0

    tracker = Tracker()
    # 필드박스
    area = [(10, 10), (10, 490), (1010, 490), (1010, 10)]

    ball_enter = {}
    frame_dict = {}  # 객체 ID를 키로 하고 해당 객체가 퇴장 또는 입장할 때의 프레임을 값으로 저장

    # 입장 횟수 카운터
    enter_count = 0

    after_change_state = 30

    # 입장프레임 저장 파일
    enter_frame_file = open("frames.txt", "w")

    state = False # 현재 공의 상태
    previous_state = False  # 이전 상태를 추적하기 위한 변수

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        count += 1
        if count % 3 != 0:
            continue
        frame = cv2.resize(frame, (1020, 500))

        after_change_state +=1

        results = model.predict(frame)
        a = results[0].boxes.boxes
        px = pd.DataFrame(a).astype("float")
        list = []
        for index, row in px.iterrows():
            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            d = int(row[5])
            c = class_list[d]
            if 'sports ball' in c:
                list.append([x1, y1, x2, y2])
        bbox_id = tracker.update(list)
        
        if after_change_state >=30:
                    state = False

        for bbox in bbox_id:
            x3, y3, x4, y4, id = bbox

            results = cv2.pointPolygonTest(np.array(area, np.int32), (((x3+x4)/2, (y3+y4)/2)), False)

            if results >= 0:
                state = True  # 객체가 area에 있음
                ball_enter[id] = (x4, y4)
                if id not in frame_dict:
                    frame_dict[id] = count  # 입장한 객체의 프레임 저장
                    if not previous_state:
                        enter_count += 1  # 이전 상태가 False였으면 입장 횟수 증가
                        # 입장 순간의 프레임 값을 파일에 저장
                        enter_frame_file.write(f"{count}\n")

            if state != previous_state:
                after_change_state =0
            
            

        cv2.polylines(frame, [np.array(area, np.int32)], True, (0, 0, 255), 1)

        # 입장 횟수 출력
        print("입장 횟수:", enter_count)
        print("State:", state, "프레임", after_change_state)
        
        previous_state = state  # 현재 상태를 이전 상태로 업데이트

        cv2.imshow("RGB", frame)
        if cv2.waitKey(500) & 0xFF == 27:
            break

    # # 입장시 해당 프레임 출력
    # for obj_id, enter_frame in frame_dict.items():
    #     print(f"Object ID: {obj_id}, 입장 프레임: {enter_frame}")

    # 파일 닫기
    enter_frame_file.close()
    cap.release()
    cv2.destroyAllWindows()

    #plus.makeShortFormVideo()
    #plus.makeLongVideo()