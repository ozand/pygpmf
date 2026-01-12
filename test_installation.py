"""
Скрипт для проверки корректности установки pygpmf
Test script to verify pygpmf installation
"""

import sys
import importlib

def test_import(module_name):
    """Попытка импорта модуля"""
    try:
        importlib.import_module(module_name)
        print(f"✓ {module_name} - OK")
        return True
    except ImportError as e:
        print(f"✗ {module_name} - FAILED: {e}")
        return False

def main():
    print("Проверка установки pygpmf / Testing pygpmf installation")
    print("=" * 60)
    
    # Проверка основных зависимостей
    print("\nПроверка зависимостей / Checking dependencies:")
    dependencies = [
        "numpy",
        "pandas",
        "matplotlib",
        "gpxpy",
        "ffmpeg",
        "geopandas",
        "contextily"
    ]
    
    all_ok = True
    for dep in dependencies:
        if not test_import(dep):
            all_ok = False
    
    # Проверка модулей pygpmf
    print("\nПроверка модулей pygpmf / Checking pygpmf modules:")
    gpmf_modules = [
        "gpmf",
        "gpmf.parse",
        "gpmf.gps",
        "gpmf.io",
        "gpmf.gps_plot"
    ]
    
    for module in gpmf_modules:
        if not test_import(module):
            all_ok = False
    
    # Проверка версии
    print("\nИнформация о версии / Version information:")
    try:
        import gpmf
        print(f"✓ pygpmf version: {gpmf.__version__}")
    except Exception as e:
        print(f"✗ Не удалось получить версию / Cannot get version: {e}")
        all_ok = False
    
    # Проверка FFmpeg
    print("\nПроверка FFmpeg / Checking FFmpeg:")
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✓ FFmpeg найден / FFmpeg found: {version_line}")
        else:
            print("✗ FFmpeg не отвечает / FFmpeg not responding")
            all_ok = False
    except FileNotFoundError:
        print("✗ FFmpeg не найден в PATH / FFmpeg not found in PATH")
        print("  Установите FFmpeg согласно инструкции в WINDOWS_INSTALL.md")
        print("  Install FFmpeg according to WINDOWS_INSTALL.md")
        all_ok = False
    except Exception as e:
        print(f"✗ Ошибка проверки FFmpeg / Error checking FFmpeg: {e}")
        all_ok = False
    
    # Итоговый результат
    print("\n" + "=" * 60)
    if all_ok:
        print("✓ Все проверки пройдены успешно!")
        print("✓ All checks passed successfully!")
        print("\nВы можете начать использовать pygpmf:")
        print("You can start using pygpmf:")
        print("  python -m gpmf --help")
        return 0
    else:
        print("✗ Некоторые проверки не прошли")
        print("✗ Some checks failed")
        print("\nУстановите недостающие зависимости:")
        print("Install missing dependencies:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
