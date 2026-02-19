"""
프로그램 실행/종료 모듈
로컬 실행 파일 실행 및 프로세스 관리
"""
import os
import subprocess


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


def close_all_programs(config):
    """config.ini의 Programs 섹션에 있는 모든 프로그램 종료"""
    try:
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
