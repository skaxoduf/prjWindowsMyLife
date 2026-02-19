"""
일괄 종료 모듈
모든 브라우저 및 프로그램 종료
"""
import subprocess
import time
from .browser import close_all_browsers
from .program import close_all_programs
from .config import load_config


def shutdown_all():
    """모든 브라우저 및 프로그램 종료"""
    print("=" * 50)
    print("프로그램 종료 모드")
    print("=" * 50)

    # 브라우저 종료
    close_all_browsers()

    # 프로그램 종료
    config = load_config()
    close_all_programs(config)

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
