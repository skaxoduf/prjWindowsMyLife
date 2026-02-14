"""
브라우저 런처 아이콘 생성 스크립트
"""
from PIL import Image, ImageDraw, ImageFont

def create_browser_icon():
    """깔끔한 브라우저 런처 아이콘 생성"""
    # 256x256 이미지 생성 (고해상도)
    size = 256
    img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 배경 원형 그라데이션 효과 (파란색 계열)
    # 외곽 원 (진한 파란색)
    draw.ellipse([10, 10, size-10, size-10], fill='#1976D2', outline='#0D47A1', width=8)

    # 내부 원 (밝은 파란색)
    draw.ellipse([40, 40, size-40, size-40], fill='#42A5F5', outline='#1976D2', width=4)

    # 브라우저 창 아이콘 그리기 (흰색)
    window_color = '#FFFFFF'

    # 첫 번째 창 (앞)
    draw.rounded_rectangle([70, 80, 180, 160], radius=8, fill=window_color, outline='#0D47A1', width=3)
    # 주소창
    draw.rounded_rectangle([78, 88, 172, 105], radius=3, fill='#E3F2FD')

    # 두 번째 창 (뒤, 살짝 오른쪽 위)
    draw.rounded_rectangle([90, 60, 200, 140], radius=8, fill=window_color, outline='#0D47A1', width=3)
    draw.rounded_rectangle([98, 68, 192, 85], radius=3, fill='#E3F2FD')

    # 세 번째 창 (제일 뒤, 오른쪽 위)
    draw.rounded_rectangle([110, 40, 220, 120], radius=8, fill=window_color, outline='#0D47A1', width=3)
    draw.rounded_rectangle([118, 48, 212, 65], radius=3, fill='#E3F2FD')

    # 재생/실행 아이콘 (오른쪽 하단에 작은 원)
    draw.ellipse([170, 170, 210, 210], fill='#4CAF50', outline='#2E7D32', width=3)
    # 재생 삼각형
    draw.polygon([(182, 180), (182, 200), (200, 190)], fill='#FFFFFF')

    # 여러 해상도로 저장
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save('browser_launcher.ico', format='ICO', sizes=sizes)
    print("Icon created successfully: browser_launcher.ico")
    print("Sizes: 256x256, 128x128, 64x64, 48x48, 32x32, 16x16")

if __name__ == '__main__':
    try:
        create_browser_icon()
    except ImportError:
        print("ERROR: PIL(Pillow) library required.")
        print("Install: pip install Pillow")
    except Exception as e:
        print(f"ERROR: {e}")
