import random

from PIL import Image

from src.core.config import Config


def pick_random_hwatu(count=2):
    # 이미지 파일 목록 생성
    image_files = [f"{Config.SUTDA_IMAGE_FOLDER_PATH}/{i}.png" for i in range(1, 21)]

    # 랜덤으로 두 개의 이미지 선택
    selected_images = random.sample(image_files, count)

    # 이미지 열기
    images = [Image.open(img) for img in selected_images]

    # 이미지 크기 설정 (가로로 붙이기 위해 크기 조정)
    total_width = sum(image.width for image in images)
    max_height = max(image.height for image in images)

    # 새로운 이미지 생성
    new_image = Image.new("RGB", (total_width, max_height))

    # 이미지를 붙이기
    x_offset = 0
    for image in images:
        new_image.paste(image, (x_offset, 0))
        x_offset += image.width

    # 결과 이미지 저장
    return new_image


def remove_not_except(list, key):
    try:
        list.remove(key)
    except:
        pass
