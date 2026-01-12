# pygpmf_oz - Модуль для извлечения GPMF данных из видео GoPro

[![PyPI version](https://badge.fury.io/py/pygpmf-oz.svg)](https://pypi.org/project/pygpmf-oz/)
[![Python versions](https://img.shields.io/pypi/pyversions/pygpmf-oz.svg)](https://pypi.org/project/pygpmf-oz/)
[![Documentation Status](https://readthedocs.org/projects/pygpmf-oz/badge/?version=latest)](https://pygpmf-oz.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Test Coverage](https://img.shields.io/badge/coverage-79.51%25-brightgreen)](htmlcov/index.html)

Обновленная и адаптированная версия проекта для работы с современными версиями Python (3.9+) и полной поддержкой Windows.

📖 **Документация**: [pygpmf-oz.readthedocs.io](https://pygpmf-oz.readthedocs.io/)  
📋 **Дорожная карта**: [DEVELOPMENT_ROADMAP.md](DEVELOPMENT_ROADMAP.md)

## 🎯 Особенности

- ✅ Извлечение GPS данных из видео GoPro
- ✅ Экспорт в формат GPX
- ✅ Визуализация GPS треков на картах
- ✅ Поддержка Python 3.9 - 3.12
- ✅ Полная поддержка Windows
- ✅ Современные зависимости
- ✅ CLI интерфейс

## 📋 Требования

- Python 3.9 или выше
- FFmpeg (должен быть установлен в системе)

## 🚀 Быстрая установка (Windows)

### 1. Установка FFmpeg

**Через Chocolatey (рекомендуется):**
```powershell
choco install ffmpeg -y
```

**Через Scoop:**
```powershell
scoop install ffmpeg
```

**Или скачайте с** https://ffmpeg.org/download.html

### 2. Установка pygpmf_oz

```powershell
# Из PyPI (рекомендуется)
pip install pygpmf_oz

# Или из исходников
cd t:\Code\python\pygpmf
pip install -e .
```

### 3. Проверка установки

```powershell
python test_installation.py
```

Подробная инструкция: [WINDOWS_INSTALL.md](WINDOWS_INSTALL.md)

## 📖 Использование

### Командная строка

```powershell
# Извлечь GPS данные в GPX формат
python -m gpmf gps-extract video.mp4 -o track.gpx

# Получить первую GPS позицию
python -m gpmf gps-first video.mp4

# Создать изображение с GPS треком
python -m gpmf gps-plot video.mp4 -o track.png
```

### Python API

```python
import gpmf

# Извлечь GPMF поток из видео
stream = gpmf.io.extract_gpmf_stream("video.mp4")

# Получить GPS блоки
gps_blocks = gpmf.gps.extract_gps_blocks(stream)
gps_data = list(map(gpmf.gps.parse_gps_block, gps_blocks))

# Конвертировать в GPX
import gpxpy
gpx = gpxpy.gpx.GPX()
gpx_track = gpxpy.gpx.GPXTrack()
gpx.tracks.append(gpx_track)
gpx_track.segments.append(gpmf.gps.make_pgx_segment(gps_data))

# Сохранить в файл
with open("track.gpx", "w", encoding="utf-8") as f:
    f.write(gpx.to_xml())
```

### Визуализация на карте

```python
import gpmf

stream = gpmf.io.extract_gpmf_stream("video.mp4")
gpmf.gps_plot.plot_gps_trace_from_stream(stream, output_path="map.png")
```

## 🔄 Что изменилось в версии 0.2.0

### Обновленные зависимости
- ✅ `python-ffmpeg` → `ffmpeg-python>=0.2.0`
- ✅ Удален устаревший `descartes`
- ✅ Все зависимости обновлены до актуальных версий
- ✅ `GeoportailFrance` → `OpenStreetMap.Mapnik` (провайдер карт)

### Улучшения для Windows
- ✅ Явная кодировка UTF-8 для всех файловых операций
- ✅ Правильная обработка путей Windows
- ✅ Полная совместимость с PowerShell

### Современная конфигурация
- ✅ Добавлен `pyproject.toml` (PEP 517/518)
- ✅ Обновлен `setup.py` с classifiers
- ✅ Настроены инструменты разработки (black, mypy, pytest)

## 📚 Документация

- [Руководство по установке на Windows](WINDOWS_INSTALL.md)
- [История изменений](CHANGELOG.md)
- [Оригинальный README](README.md)

## 🔧 Разработка

```powershell
# Установка с dev зависимостями
pip install -e ".[dev]"

# Форматирование кода
black gpmf/

# Запуск тестов
pytest
```

## 🐛 Решение проблем

### FFmpeg не найден
```powershell
# Проверьте установку
ffmpeg -version

# Если не найден - установите (см. выше)
choco install ffmpeg -y
```

### Ошибки с geopandas
```powershell
# На Windows может потребоваться conda
conda install geopandas
```

### Проблемы с кодировкой
Проект уже настроен для UTF-8. Если проблемы остались:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

## 📄 Лицензия

MIT License - см. [LICENSE](LICENSE)

## 👏 Благодарности и атрибуция

**Автор и сопровождающий**: ozand  
**Оригинальный проект**: [pygpmf](https://github.com/alexis-mignon/pygpmf) от Alexis Mignon

Данный проект (`pygpmf-oz`) является модернизированным форком оригинальной библиотеки `pygpmf` от Alexis Mignon.  
Ключевые улучшения: поддержка Python 3.9-3.13, совместимость с Windows, активная поддержка.

**Формат GPMF**: [GoPro GPMF Parser](https://github.com/gopro/gpmf-parser)

## 🔗 Ссылки

- [GitHub Repository](https://github.com/ozand/pygpmf-oz)
- [PyPI Package](https://pypi.org/project/pygpmf-oz/)
- [Оригинальный проект](https://github.com/alexis-mignon/pygpmf) (Alexis Mignon)
- [GPMF Parser](https://github.com/gopro/gpmf-parser)

## 📮 Контакты

Если у вас есть вопросы или предложения, создайте Issue в GitHub репозитории.

---

**Статус проекта**: Активная разработка  
**Версия**: 0.3.0  
**Последнее обновление**: Январь 2026
