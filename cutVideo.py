import cv2
import time
index =0
def cut_and_slow_down_video(frame):
    left_input_video_path = "input/left.mp4"
    right_input_video_path = "input/right.mp4"

    left_output_normal = "source/left_normal.mp4"
    right_output_normal = "source/right_normal.mp4"
    left_output_slow = "source/left_slow.mp4"
    right_output_slow = "source/right_slow.mp4"

    video_path = f"output/output_{index}.mp4"



    # 들어온 Frame 기준으로 기본 속도(앞 뒤 100) 자르기
    normal_start_frame_number = frame - 60
    normal_end_frame_number = frame + 60
    
    # 들어온 Frame 기준으로 느린 속도(앞 뒤 100) 자르기
    slow_start_frame_number = frame - 10
    slow_end_frame_number = frame + 10

    # 좌측 영상 자르기(기본 속도)
    cut(left_input_video_path, left_output_normal, normal_start_frame_number, normal_end_frame_number, 5)
    # 우측 영상 자르기(기본 속도)
    cut(right_input_video_path, right_output_normal, normal_start_frame_number, normal_end_frame_number, 5)
    # 좌측 영상 자르기(느린 속도)
    cut(left_input_video_path, left_output_slow, slow_start_frame_number, slow_end_frame_number, 4)
    # 우측 영상 자르기(느린 속도)
    cut(right_input_video_path, right_output_slow, slow_start_frame_number, slow_end_frame_number, 4)


    #합치기
    left_normal = cv2.VideoCapture(left_output_normal)
    right_normal = cv2.VideoCapture(right_output_normal)
    left_slow = cv2.VideoCapture(left_output_slow)
    right_slow = cv2.VideoCapture(right_output_slow)

    fps = left_normal.get(cv2.CAP_PROP_FPS)
    print(fps)
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    width = int(left_normal.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(left_normal.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    while True:
        ret1, frame1 = left_normal.read()
        if not ret1:
            ret2, frame2 = right_normal.read()
            if not ret2:
                ret3, frame3 = left_slow.read()
                if not ret3:
                    ret4, frame4 = right_slow.read()
                    if not ret4:
                        break
                    else:
                        for _ in range(int(fps * 0.5) - 1):
                            output.write(frame4)    
                else:
                    for _ in range(int(fps * 0.5) - 1):
                        output.write(frame3)
            else:
                output.write(frame2)    
        else:
            output.write(frame1)

    # 모든 비디오 파일을 닫습니다.
    left_normal.release()
    right_normal.release()
    left_slow.release()
    right_slow.release()
    output.release()
    print("END")
############################################################################

def cut(input_path, output_path, start_frame, end_frame, speed):
    vc = cv2.VideoCapture(input_path)
    if not vc.isOpened():
        print("Can't open input video.")
        return

    fps = vc.get(cv2.CAP_PROP_FPS)
    print("fps: ",fps)

    width = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("width: ", width, ", height: ", height)

    if start_frame >= end_frame:
        print("Invalid frame range.")
        return

    total_frames = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))

    if end_frame > total_frames:
        print("End frame exceeds the total number of frames. Setting end frame to the last frame.")
        end_frame = total_frames

    vc.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    vw = cv2.VideoWriter(output_path, fourcc, fps*speed, (width, height))

    frame_count = start_frame
    while frame_count <= end_frame:
        ret, frame = vc.read()
        if not ret:
            break

        # 속도 조절
        vw.write(frame)
        frame_count += 1

    vc.release()
    vw.release()
    print("Video cut and speed adjusted successfully!")
###############################################################################################


def run():
    global index
    index = 0
    
    with open('frames.txt', 'r') as file:
        lines = file.readlines()

    # 리스트에 저장된 각 줄의 내용 출력
    for line in lines:
        cut_and_slow_down_video(int(line.strip()))
        index+=1

