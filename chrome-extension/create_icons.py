from PIL import Image, ImageDraw, ImageFont
import os

# 아이콘 크기
sizes = [16, 48, 128]

# 각 크기별 아이콘 생성
for size in sizes:
    # 새 이미지 생성
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 배경 원 그리기 (파란색)
    margin = size // 10
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 fill=(70, 130, 255, 255))
    
    # 돋보기 모양 그리기 (흰색)
    center = size // 2
    lens_radius = size // 4
    
    # 렌즈
    draw.ellipse([center - lens_radius, center - lens_radius,
                  center + lens_radius, center + lens_radius],
                 outline=(255, 255, 255, 255), width=max(2, size//16))
    
    # 손잡이
    handle_start = center + lens_radius * 0.7
    handle_end = size - margin * 2
    draw.line([handle_start, handle_start, handle_end, handle_end],
              fill=(255, 255, 255, 255), width=max(2, size//16))
    
    # 저장
    img.save(f'icon{size}.png')
    print(f'Created icon{size}.png')

print("Icons created successfully!")