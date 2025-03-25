import cv2
import os
import pandas as pd

# 이미지 폴더 경로 설정
IMAGE_FOLDER = './data'
CSV_FILE = 'clicked_coordinates.csv'

# 결과 저장용 DataFrame 생성
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=['image_name', 'x', 'y'])

# 이미지 파일 불러오기
image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
current_index = 0

# 좌표 클릭 시 실행될 함수 정의
def click_event(event, x, y, flags, param):
    global current_index, df

    if event == cv2.EVENT_LBUTTONDOWN:
        image_name = image_files[current_index]
        print(f"Clicked at: ({x}, {y}) on {image_name}")

        # 좌표를 DataFrame에 추가
        new_row = pd.DataFrame({'image_name': [image_name], 'x': [x], 'y': [y]})
        df = pd.concat([df, new_row], ignore_index=True)

        # CSV 파일로 저장
        df.to_csv(CSV_FILE, index=False)

        # 다음 이미지로 이동
        current_index += 1
        if current_index < len(image_files):
            cv2.destroyWindow('Image')  # 현재 창만 닫기
            show_next_image()
        else:
            print("All images have been processed.")
            cv2.destroyAllWindows()

def show_next_image():
    global current_index

    if current_index < len(image_files):
        image_path = os.path.join(IMAGE_FOLDER, image_files[current_index])
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"Failed to load image: {image_path}")
            current_index += 1
            show_next_image()
            return

        # 이미지 표시 및 마우스 이벤트 바인딩
        cv2.imshow('Image', image)
        cv2.setMouseCallback('Image', click_event)

        # ESC 키를 누르면 종료
        key = cv2.waitKey(0)
        if key == 27:  # ESC 키 코드
            print("Program terminated by user.")
            cv2.destroyAllWindows()

# 첫 번째 이미지 출력
show_next_image()
