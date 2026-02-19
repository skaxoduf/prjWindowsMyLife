"""
브라우저 실행/종료 모듈
여러 브라우저 실행 및 일괄 종료 기능
"""
import subprocess
import time


def get_browser_process_name(browser_cmd):
    """브라우저 명령어에서 프로세스 이름 반환"""
    process_map = {
        'msedge': 'msedge.exe',
        'chrome': 'chrome.exe',
        'brave': 'brave.exe',
        'firefox': 'firefox.exe',
        'opera': 'opera.exe',
    }
    return process_map.get(browser_cmd, f'{browser_cmd}.exe')


def launch_browser(browser_cmd, urls, section_name):
    """브라우저 실행"""
    try:
        if isinstance(urls, str):
            urls = [urls]

        # 브라우저 플래그
        # --new-window: 새 창으로 열기
        # --start-maximized: 창 최대화
        # --no-default-browser-check: 기본 브라우저 확인 안 함
        # --disable-session-crashed-bubble: 세션 복구 팝업 숨김
        flags = ['--new-window', '--start-maximized', '--no-default-browser-check', '--disable-session-crashed-bubble']

        subprocess.Popen(['start', browser_cmd] + flags + urls, shell=True)
        print(f"   ✓ 실행됨")
        return True
    except Exception as e:
        print(f"   ❌ 실행 오류: {e}")
        return False


def get_browser_info(section_name):
    """섹션 이름에서 브라우저 타입 추출"""
    # 브라우저 매핑: (브라우저명, 실행명령어, 아이콘)
    browser_map = {
        'edge': ('msedge', '🔵'),
        'chrome': ('chrome', '🟢'),
        'brave': ('brave', '🟠'),
        'firefox': ('firefox', '🟧'),
        'opera': ('opera', '🔴'),
    }

    # 섹션 이름을 소문자로 변환하여 검사
    section_lower = section_name.lower()

    for browser_key, (browser_cmd, icon) in browser_map.items():
        if section_lower.startswith(browser_key):
            return browser_cmd, icon, browser_key.capitalize()

    return None, None, None


def close_all_browsers():
    """실행 중인 모든 브라우저 종료"""
    browser_processes = {
        'Edge': 'msedge.exe',
        'Chrome': 'chrome.exe',
        'Brave': 'brave.exe',
        'Firefox': 'firefox.exe',
        'Opera': 'opera.exe',
    }

    print("\n🔄 기존 브라우저 종료 중...")
    closed_count = 0

    for browser_name, process_name in browser_processes.items():
        try:
            # taskkill로 프로세스 종료 (/F: 강제, /IM: 이미지 이름)
            result = subprocess.run(
                ['taskkill', '/F', '/IM', process_name],
                capture_output=True,
                text=True
            )
            # 성공적으로 종료된 경우 (에러 코드 0)
            if result.returncode == 0:
                print(f"   ✓ {browser_name} 종료됨")
                closed_count += 1
        except Exception as e:
            # 오류 무시 (브라우저가 실행 중이 아닐 수 있음)
            pass

    if closed_count > 0:
        print(f"   총 {closed_count}개 브라우저 종료됨")
        time.sleep(1)  # 종료 완료를 위한 대기
    else:
        print("   실행 중인 브라우저 없음")

    return closed_count
