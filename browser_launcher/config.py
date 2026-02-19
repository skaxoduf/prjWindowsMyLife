"""
Config 관리 모듈
config.ini 파일 읽기 및 URL 추출
"""
import os
import sys
from configparser import ConfigParser


def get_config_path():
    """exe 파일과 같은 디렉토리에서 config.ini 찾기"""
    if getattr(sys, 'frozen', False):
        # PyInstaller로 만든 exe인 경우
        application_path = os.path.dirname(sys.executable)
    else:
        # 일반 Python 스크립트인 경우
        application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(application_path, 'config.ini')


def load_config():
    """config.ini 파일 읽기"""
    config_path = get_config_path()

    if not os.path.exists(config_path):
        print(f"❌ 오류: config.ini 파일을 찾을 수 없습니다!")
        print(f"경로: {config_path}")
        input("엔터를 눌러 종료하세요...")
        sys.exit(1)

    config = ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config


def get_urls_from_section(config, section_name):
    """섹션에서 url1, url2, url3... 형태로 모든 URL 읽기"""
    urls = []
    i = 1
    while True:
        url_key = f'url{i}'
        if config.has_option(section_name, url_key):
            url = config.get(section_name, url_key).strip()
            if url:  # 빈 문자열이 아니면
                urls.append(url)
            i += 1
        else:
            break
    return urls
