"""
Multi Browser Launcher with INI Configuration
config.ini 파일에서 URL을 읽어 여러 브라우저를 실행합니다.
"""
import subprocess
import time
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
        application_path = os.path.dirname(os.path.abspath(__file__))

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

def is_process_running(process_name):
    """프로세스가 실행 중인지 확인"""
    try:
        result = subprocess.run(['tasklist'], capture_output=True, text=True)
        return process_name.lower() in result.stdout.lower()
    except Exception:
        return False

def launch_program(program_path):
    """로컬 실행 파일 실행 (이미 실행 중이면 무시)"""
    try:
        # 경로가 존재하는지 확인
        if not os.path.exists(program_path):
            print(f"   ⚠️  파일을 찾을 수 없습니다: {program_path}")
            return False

        # 프로세스 이름 추출 (경로에서 파일명만)
        process_name = os.path.basename(program_path)

        # 이미 실행 중인지 확인
        if is_process_running(process_name):
            print(f"   ⏭️  이미 실행 중 (무시): {process_name}")
            return True  # 이미 실행 중이므로 성공으로 간주

        # 실행
        subprocess.Popen([program_path], shell=True)
        print(f"   ✓ 실행됨: {process_name}")
        return True
    except Exception as e:
        print(f"   ❌ 실행 오류: {e}")
        return False

def find_ssms_path():
    """SSMS 설치 경로 찾기"""
    # 일반적인 SSMS 설치 경로들
    possible_paths = [
        r"C:\Program Files (x86)\Microsoft SQL Server Management Studio 20\Common7\IDE\Ssms.exe",
        r"C:\Program Files (x86)\Microsoft SQL Server Management Studio 19\Common7\IDE\Ssms.exe",
        r"C:\Program Files (x86)\Microsoft SQL Server Management Studio 18\Common7\IDE\Ssms.exe",
        r"C:\Program Files\Microsoft SQL Server Management Studio 20\Common7\IDE\Ssms.exe",
        r"C:\Program Files\Microsoft SQL Server Management Studio 19\Common7\IDE\Ssms.exe",
        r"C:\Program Files\Microsoft SQL Server Management Studio 18\Common7\IDE\Ssms.exe",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    return None

def launch_ssms(server, database, sqlfile=None, auth='Windows', username=None, password=None, program_path=None):
    """SSMS 실행 및 DB 연결"""
    try:
        # SSMS 경로 결정
        if program_path and os.path.exists(program_path):
            ssms_path = program_path
        else:
            # 자동으로 찾기
            ssms_path = find_ssms_path()

        if not ssms_path:
            print(f"   ⚠️  SSMS를 찾을 수 없습니다")
            print(f"      config.ini에 program 경로를 지정하세요")
            print(f"      예: program = C:\\Program Files (x86)\\Microsoft SQL Server Management Studio 19\\Common7\\IDE\\Ssms.exe")
            return False

        # SQL 파일 경로 확인
        if sqlfile and not os.path.exists(sqlfile):
            print(f"   ⚠️  SQL 파일을 찾을 수 없습니다: {sqlfile}")
            return False

        # 명령어 구성
        cmd = [ssms_path]

        # SQL 파일이 있으면 먼저 추가
        if sqlfile:
            cmd.append(sqlfile)

        # 서버 연결 옵션
        cmd.extend(['-S', server])

        # 데이터베이스 지정
        if database:
            cmd.extend(['-d', database])

        # 인증 방식
        if auth.upper() == 'WINDOWS' or auth.upper() == 'W':
            cmd.append('-E')  # Windows 인증
        elif auth.upper() == 'SQL' or auth.upper() == 'S':
            if username:
                cmd.extend(['-U', username])
            # 주의: SSMS는 명령줄에서 -P (password) 스위치를 지원하지 않습니다
            # 비밀번호는 SSMS 로그인 대화상자에서 수동으로 입력해야 합니다

        # 실행
        subprocess.Popen(cmd)

        # 출력 메시지
        print(f"   ✓ 연결: {server} -> {database}")
        if sqlfile:
            print(f"      파일: {os.path.basename(sqlfile)}")

        return True

    except Exception as e:
        print(f"   ❌ SSMS 실행 오류: {e}")
        return False

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

def close_all_programs():
    """config.ini의 Programs 섹션에 있는 모든 프로그램 종료"""
    try:
        config = load_config()

        if not config.has_section('Programs'):
            return 0

        print("\n🔄 프로그램 종료 중...")
        closed_count = 0

        # Programs 섹션에서 모든 프로그램 읽기
        i = 1
        while True:
            program_key = f'program{i}'
            if config.has_option('Programs', program_key):
                program_path = config.get('Programs', program_key).strip()
                if program_path and not program_path.startswith('#'):
                    # 프로세스 이름 추출
                    process_name = os.path.basename(program_path)

                    try:
                        result = subprocess.run(
                            ['taskkill', '/F', '/IM', process_name],
                            capture_output=True,
                            text=True
                        )
                        if result.returncode == 0:
                            print(f"   ✓ {process_name} 종료됨")
                            closed_count += 1
                    except Exception:
                        pass
                i += 1
            else:
                break

        if closed_count > 0:
            print(f"   총 {closed_count}개 프로그램 종료됨")
        else:
            print("   실행 중인 프로그램 없음")

        return closed_count
    except Exception as e:
        print(f"   ❌ 오류: {e}")
        return 0

def shutdown_all():
    """모든 브라우저 및 프로그램 종료"""
    print("=" * 50)
    print("프로그램 종료 모드")
    print("=" * 50)

    # 브라우저 종료
    close_all_browsers()

    # 프로그램 종료
    close_all_programs()

    # SSMS 종료
    print("\n🔄 SSMS 종료 중...")
    try:
        result = subprocess.run(
            ['taskkill', '/F', '/IM', 'Ssms.exe'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("   ✓ SSMS 종료됨")
        else:
            print("   실행 중인 SSMS 없음")
    except Exception:
        print("   실행 중인 SSMS 없음")

    print("\n" + "=" * 50)
    print("✅ 모든 프로세스 종료 완료")
    print("=" * 50)

    # 3초 후 자동 종료
    print("\n3초 후 자동으로 종료됩니다...")
    time.sleep(3)

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

def main():
    print("=" * 50)
    print("Multi Browser & Program Launcher")
    print("=" * 50)

    # config.ini 읽기
    config = load_config()

    success_count = 0
    total_count = 0

    # 모든 섹션을 순회하며 브라우저 및 SSMS 섹션 찾기
    for section in config.sections():
        # Programs 섹션은 건너뛰기 (나중에 처리)
        if section == 'Programs':
            continue

        # SSMS 섹션 처리
        if section.upper().startswith('SSMS'):
            print(f"\n🗄️  {section}:")
            total_count += 1

            # SSMS 설정 읽기
            program_path = config.get(section, 'program', fallback=None)
            server = config.get(section, 'server', fallback='localhost')
            database = config.get(section, 'database', fallback='')
            sqlfile = config.get(section, 'sqlfile', fallback=None)
            auth = config.get(section, 'auth', fallback='Windows')
            username = config.get(section, 'username', fallback=None)
            password = config.get(section, 'password', fallback=None)

            if launch_ssms(server, database, sqlfile, auth, username, password, program_path):
                success_count += 1
            time.sleep(0.5)
            continue

        # 브라우저 섹션 처리
        browser_cmd, icon, browser_type = get_browser_info(section)

        if browser_cmd:  # 브라우저 섹션인 경우
            urls = get_urls_from_section(config, section)

            if urls:
                print(f"\n{icon} {section} ({len(urls)}개 탭):")
                for url in urls:
                    # URL이 너무 길면 축약
                    display_url = url if len(url) <= 60 else url[:57] + "..."
                    print(f"   - {display_url}")

                total_count += 1
                if launch_browser(browser_cmd, urls, section):
                    success_count += 1
                time.sleep(0.5)

    # 로컬 프로그램 실행
    if config.has_section('Programs'):
        programs = []
        i = 1
        while True:
            program_key = f'program{i}'
            if config.has_option('Programs', program_key):
                program_path = config.get('Programs', program_key).strip()
                if program_path and not program_path.startswith('#'):  # 주석이 아니면
                    programs.append(program_path)
                i += 1
            else:
                break

        if programs:
            print(f"\n💻 로컬 프로그램 ({len(programs)}개):")
            for program_path in programs:
                total_count += 1
                if launch_program(program_path):
                    success_count += 1
                time.sleep(0.3)

    print("\n" + "=" * 50)
    if total_count > 0:
        print(f"✅ 완료: {success_count}/{total_count}개 항목 실행됨")
    else:
        print("⚠️  실행할 항목이 없습니다. config.ini를 확인하세요.")
    print("=" * 50)

    # 3초 후 자동 종료
    print("\n3초 후 자동으로 종료됩니다...")
    time.sleep(3)

if __name__ == '__main__':
    try:
        # 종료 모드 확인
        if len(sys.argv) > 1 and sys.argv[1] in ['--close', '--shutdown', '-c']:
            shutdown_all()
        else:
            main()
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류 발생: {e}")
        input("\n엔터를 눌러 종료하세요...")
