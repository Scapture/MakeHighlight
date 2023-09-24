import os

def run():
    directory_output_path = 'output/'
    # 디렉토리 내의 모든 파일 가져오기
    file_list = os.listdir(directory_output_path)
    # 디렉토리 내의 모든 파일 삭제
    for filename in file_list:
        file_path = os.path.join(directory_output_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f'{filename} 파일 삭제 완료')
            else:
                print(f'{filename}은 파일이 아닙니다.')
        except Exception as e:
            print(f'{filename} 삭제 중 예외 발생:', str(e))