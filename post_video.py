import os
import requests

def run():
    # 업로드할 URL(서버의 업로드 뷰 URL에 맞게 수정)
    upload_url = 'http://127.0.0.1:8000/post/'
    
    # output 디렉토리 경로
    output_directory = 'output/'
    
    # output 디렉토리 내의 모든 파일 가져오기
    video_files = [f for f in os.listdir(output_directory) if os.path.isfile(os.path.join(output_directory, f))]
    
    for video_file_name in video_files:
        video_file_path = os.path.join(output_directory, video_file_name)
        
        try:
            with open(video_file_path, 'rb') as video_file:
                files = {'video': (video_file_name, video_file, 'video/mp4')}
                response = requests.post(upload_url, files=files)
    
            if response.status_code == 200:
                print(f'{video_file_name} 업로드 성공!')
            else:
                print(f'{video_file_name} 업로드 실패. 상태 코드:', response.status_code)
        except Exception as e:
            print(f'{video_file_name} 업로드 중 예외 발생:', str(e))
