# Windows Installation Guide / Руководство по установке на Windows

## Требования / Requirements

- Windows 10/11
- Python 3.9 или выше / Python 3.9 or higher
- FFmpeg

## Шаг 1: Установка FFmpeg / Step 1: Install FFmpeg

### Вариант A: Через Chocolatey (рекомендуется)
```powershell
# Установите Chocolatey, если еще не установлен
# Install Chocolatey if not installed
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Установите FFmpeg
# Install FFmpeg
choco install ffmpeg -y
```

### Вариант B: Через Scoop
```powershell
# Установите Scoop
# Install Scoop
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Установите FFmpeg
# Install FFmpeg
scoop install ffmpeg
```

### Вариант C: Ручная установка / Manual Installation
1. Скачайте FFmpeg с https://ffmpeg.org/download.html (Windows build)
2. Распакуйте в `C:\ffmpeg`
3. Добавьте `C:\ffmpeg\bin` в PATH:
   - Откройте "Система" → "Дополнительные параметры системы"
   - "Переменные среды" → "Path" → "Изменить"
   - Добавьте путь к папке bin FFmpeg

4. Проверьте установку / Verify installation:
```powershell
ffmpeg -version
```

## Шаг 2: Установка Python пакета / Step 2: Install Python Package

### Из локальной директории / From local directory
```powershell
cd t:\Code\python\pygpmf
pip install -e .
```

### Или установите зависимости отдельно / Or install dependencies separately
```powershell
pip install -r requirements.txt
```

## Шаг 3: Проверка установки / Step 3: Verify Installation

```powershell
python -m gpmf --help
```

## Использование / Usage

### Пример 1: Извлечение GPX
```powershell
python -m gpmf gps-extract "C:\Videos\GoPro\GOPR0001.MP4" -o "C:\Output\track.gpx"
```

### Пример 2: Создание карты трека
```powershell
python -m gpmf gps-plot "C:\Videos\GoPro\GOPR0001.MP4" -o "C:\Output\map.png"
```

### Пример 3: Получение первой GPS координаты
```powershell
python -m gpmf gps-first "C:\Videos\GoPro\GOPR0001.MP4"
```

## Решение проблем / Troubleshooting

### Ошибка: "ffmpeg not found"
- Убедитесь что FFmpeg установлен: `ffmpeg -version`
- Проверьте что FFmpeg в PATH
- Перезапустите PowerShell/терминал после установки

### Ошибка: "No module named 'ffmpeg'"
```powershell
pip install ffmpeg-python
```

### Ошибка с geopandas на Windows
Geopandas может требовать дополнительных зависимостей на Windows:
```powershell
# Попробуйте установить через conda
conda install geopandas

# Или используйте предсобранные wheels
pip install --find-links=https://www.lfd.uci.edu/~gohlke/pythonlibs/ geopandas
```

### Ошибки кодировки
Проект уже настроен для работы с UTF-8 на Windows. Если возникают проблемы:
```powershell
# Установите кодировку UTF-8 для PowerShell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

## Быстрый старт / Quick Start

```python
import gpmf

# Извлечь GPS данные из видео
# Extract GPS data from video
stream = gpmf.io.extract_gpmf_stream(r"C:\Videos\GOPR0001.MP4")

# Получить GPS блоки
# Get GPS blocks
gps_blocks = gpmf.gps.extract_gps_blocks(stream)
gps_data = list(map(gpmf.gps.parse_gps_block, gps_blocks))

# Конвертировать в GPX
# Convert to GPX
import gpxpy
gpx = gpxpy.gpx.GPX()
gpx_track = gpxpy.gpx.GPXTrack()
gpx.tracks.append(gpx_track)
gpx_track.segments.append(gpmf.gps.make_pgx_segment(gps_data))

# Сохранить
# Save
with open(r"C:\Output\track.gpx", "w", encoding="utf-8") as f:
    f.write(gpx.to_xml())
```

## Дополнительная информация / Additional Information

- Все файловые операции используют UTF-8 кодировку
- All file operations use UTF-8 encoding
- Пути можно использовать как с `/`, так и с `\`
- Paths can use both `/` and `\`
- Рекомендуется использовать raw strings для путей: `r"C:\path\to\file"`
- Recommended to use raw strings for paths: `r"C:\path\to\file"`
