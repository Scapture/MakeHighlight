import os
import random
import string
import requests
import mqtt_pub
# 서버의 엔드포인트 URL 설정

def run():
    server_url = 'http://192.168.1.11:8000/post'
    # POST 요청에 함께 보낼 데이터 설정 (예: 헤더, 파라미터, 기타 데이터)
    game_number = random.randrange(1, 10000) # 1부터 10 사이의 난수 생성
    data = {'game': game_number}
    # 영상 파일이 있는 폴더 경로 설정
    video_folder_path = './output/'
    # video_folder_path 내의 모든 파일 목록 가져오기
    video_files = os.listdir(video_folder_path)
    video_files = [file for file in video_files if not file.startswith('.')]
    # 각 영상 파일을 서버로 전송
    for video_file_name in video_files:
        video_file_path = os.path.join(video_folder_path, video_file_name)
        # 영상 파일 열기
        with open(video_file_path, 'rb') as video_file:
            # 파일 이름을 무작위로 생성하여 전달
            name = "".join([random.choice(string.ascii_letters) for _ in range(30)])
            files = {'video': (f'{name}.mp4', video_file)}
            # POST 요청 보내기
            response = requests.post(server_url, data=data, files=files)
        # 서버 응답 확인
        if response.status_code == 201:
            print(f'서버에 영상 {video_file_name}을 성공적으로 전송했습니다.')
        else:
            print(f'영상 {video_file_name} 전송에 실패했습니다. 응답 코드:', response.status_code)
            print('에러 메시지:', response.text)
    mqtt_pub.run(game_number)
