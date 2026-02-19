"""
Multi Browser Launcher with INI Configuration
config.ini 파일에서 URL을 읽어 여러 브라우저를 실행합니다.

진입점 파일 - 실제 구현은 browser_launcher 패키지에 있습니다.
"""
import sys
import io

# Windows 콘솔 인코딩 설정 (이모지 출력을 위해)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from browser_launcher.main import main
from browser_launcher.shutdown import shutdown_all


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
