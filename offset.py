from PIL import Image
import os

# 이미지 파일 경로 설정
for path in os.listdir('image'):
    if not path.startswith('z'):
        continue
    image = Image.open('image/'+path)
    crop_px = 19
    width, height = image.size
    cropped_image = image.crop((crop_px, 0, width - crop_px, height))
    cropped_image.save(f'output/{path}')
