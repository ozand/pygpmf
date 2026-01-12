# pygpmf_oz - Адаптированная версия

Эта версия проекта `pygpmf` была обновлена и адаптирована для работы с современными версиями Python (3.9+) и Windows.

**Название изменено на `pygpmf_oz`** для публикации на PyPI и отличия от оригинального проекта.

## Основные изменения

### 1. Обновленные зависимости
- ✅ Заменен `python-ffmpeg` на `ffmpeg-python>=0.2.0`
- ✅ Удален устаревший пакет `descartes` (функциональность встроена в geopandas)
- ✅ Обновлены минимальные версии всех зависимостей
- ✅ Изменен провайдер карт с GeoportailFrance на OpenStreetMap.Mapnik

### 2. Совместимость с Python 3.9+
- ✅ Добавлена явная кодировка UTF-8 для файловых операций
- ✅ Обновлен `setup.py` с указанием `python_requires=">=3.9"`
- ✅ Добавлены classifiers для Python 3.9-3.12

### 3. Поддержка Windows
- ✅ Явная кодировка UTF-8 при работе с файлами
- ✅ Совместимость путей с Windows
- ✅ Обновлены зависимости для корректной работы на Windows

### 4. Современная конфигурация проекта
- ✅ Добавлен `pyproject.toml` с современными стандартами PEP 517/518
- ✅ Настроены инструменты разработки (black, mypy, pytest)
- ✅ Добавлены метаданные проекта

## Установка

### Требования
- Python 3.9 или выше
- FFmpeg должен быть установлен в системе

### Установка FFmpeg на Windows
```powershell
# Через Chocolatey
choco install ffmpeg

# Через Scoop
scoop install ffmpeg

# Или скачать с https://ffmpeg.org/download.html
```

### Установка пакета

```bash
# Установка из локального каталога
pip install -e .

# Или установка зависимостей из requirements.txt
pip install -r requirements.txt
```

## Использование

### Извлечение GPS данных в GPX формат

```python
import gpmf

# Чтение бинарного потока из файла
stream = gpmf.io.extract_gpmf_stream("my_gopro_video.mp4")

# Извлечение GPS блоков низкого уровня
gps_blocks = gpmf.gps.extract_gps_blocks(stream)

# Парсинг в удобный формат
gps_data = list(map(gpmf.gps.parse_gps_block, gps_blocks))

# Конвертация в GPX
import gpxpy

gpx = gpxpy.gpx.GPX()
gpx_track = gpxpy.gpx.GPXTrack()
gpx.tracks.append(gpx_track)
gpx_track.segments.append(gpmf.gps.make_pgx_segment(gps_data))

# Сохранение в файл
with open("output.gpx", "w", encoding="utf-8") as f:
    f.write(gpx.to_xml())
```

### Визуализация GPS трека на карте

```python
import gpmf

# Чтение бинарного потока из файла
stream = gpmf.io.extract_gpmf_stream("my_gopro_video.mp4")

# Построение карты с треком
gpmf.gps_plot.plot_gps_trace_from_stream(stream, output_path="track.png")
```

### Командная строка

```bash
# Извлечение GPX
python -m gpmf gps-extract video.mp4 -o output.gpx

# Получение первой GPS позиции
python -m gpmf gps-first video.mp4

# Создание изображения с треком
python -m gpmf gps-plot video.mp4 -o track.png
```

## Изменения в API

### contextily провайдер карт
Старый код:
```python
ctx.providers.GeoportailFrance["maps"]  # Больше не работает
```

Новый код:
```python
ctx.providers.OpenStreetMap.Mapnik  # Работает по умолчанию
```

### Кодировка файлов
Все файловые операции теперь явно используют UTF-8:
```python
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
```

## Известные проблемы и решения

### FFmpeg не найден
Если возникает ошибка "ffmpeg not found":
1. Установите FFmpeg (см. раздел "Установка FFmpeg")
2. Убедитесь что FFmpeg в PATH: `ffmpeg -version`

### Ошибки импорта geopandas
На Windows может потребоваться установка через conda:
```bash
conda install geopandas
```

## Разработка

```bash
# Установка с зависимостями для разработки
pip install -e ".[dev]"

# Форматирование кода
black gpmf/

# Запуск тестов
pytest
```

## Лицензия

MIT License - см. файл LICENSE

## Благодарности

- Оригинальный автор: Alexis Mignon
- Информация о формате GPMF: [GoPro GitHub](https://github.com/gopro/gpmf-parser)

## Изменения версии 0.2.0

- Обновлена поддержка Python 3.9+
- Добавлена полная поддержка Windows
- Обновлены все зависимости до современных версий
- Добавлен pyproject.toml
- Улучшена документация
- Исправлены проблемы с кодировкой
