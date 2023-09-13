import cv2
import os

import pandas as pd
from tracker import *
from ultralytics import YOLO


model = YOLO('yolov8s.pt')
# 원본 동영상 파일 경로
original_video_path = '하이라이트 좌측 영상.mp4'

# 학습 클래스 불러오기
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

# 결과 동영상 파일 저장 디렉토리
output_directory = '출력영상/'

tracker = Tracker()

# 입장프레임.txt에서 프레임 번호를 읽어오기
with open('입장프레임.txt', 'r') as file:
    frame_numbers = [int(line.strip()) for line in file]

# 원본 비디오 파일 열기
cap = cv2.VideoCapture(original_video_path)

# 비디오에서 프레임을 하나씩 읽어서 처리
for frame_number in frame_numbers:
    # 프레임 앞뒤 1초를 계산
    start_frame = max(1, frame_number - 30)  # 1초 전
    end_frame = min(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), frame_number + 30)  # 1초 후

    # 결과 동영상 파일 생성
    output_video_name = f'{frame_number}.mp4'
    output_video_path = os.path.join(output_directory, output_video_name)

    # 원본 동영상의 해상도와 프레임 레이트를 가져옵니다.
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    frame_rate = int(cap.get(5))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (frame_width, frame_height))

    # 원본 비디오를 프레임 단위로 읽어서 저장
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame - 1)  # 시작 프레임으로 이동
    frame_count = start_frame

    while frame_count <= end_frame:
        ret, frame = cap.read()
        if not ret:
            break

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

        # 중심 좌표를 기준으로 2배 확대
        for bbox in bbox_id:
            x3, y3, x4, y4, id = bbox

            # 공의 중심 좌표 계산
            ball_center_x = (x3 + x4) // 2
            ball_center_y = (y3 + y4) // 2

        ball_center_x = max(0, min(ball_center_x, frame.shape[1]))
        ball_center_y = max(0, min(ball_center_y, frame.shape[0]))
        zoomed_frame = frame[max(0, ball_center_y - 250):min(frame.shape[0], ball_center_y + 250),
                            max(0, ball_center_x - 510):min(frame.shape[1], ball_center_x + 510)]

        frame = cv2.resize(frame, (1020, 500))
        # 확대된 화면을 저장
        out.write(zoomed_frame)

        frame_count += 1

    # 파일을 닫습니다.
    out.release()

# 원본 동영상 파일 닫기
cap.release()

print(f"{len(frame_numbers)} 개의 영상 파일이 {output_directory}에 생성되었습니다.")