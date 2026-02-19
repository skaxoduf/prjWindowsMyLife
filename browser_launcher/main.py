"""
메인 실행 모듈
브라우저, 프로그램, SSMS를 config.ini에 따라 실행
"""
import time
from .config import load_config, get_urls_from_section
from .browser import launch_browser, get_browser_info
from .program import launch_program
from .ssms import launch_ssms


def main():
    """메인 실행 함수"""
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
