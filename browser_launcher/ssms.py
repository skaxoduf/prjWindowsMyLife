"""
SSMS (SQL Server Management Studio) 실행 모듈
SSMS 자동 실행 및 DB 연결
"""
import os
import subprocess


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
