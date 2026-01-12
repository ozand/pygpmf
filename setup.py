from setuptools import setup, find_packages
import pathlib
import re

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding='utf-8')

# Read version from __init__.py
init_file = (HERE / "gpmf" / "__init__.py").read_text(encoding='utf-8')
version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', init_file)
if version_match:
    __version__ = version_match.group(1)
else:
    __version__ = "0.3.0"

if __name__ == "__main__":
    setup(
        name="pygpmf_oz",
        author="Alexis Mignon",
        author_email="alexis.mignon@gmail.com",
        description="A module to read GPMF data embedded in GoPro video files. Modernized fork with Python 3.9+ and Windows support.",
        long_description=README,
        long_description_content_type="text/markdown",
        version=__version__,
        packages=find_packages(),
        python_requires=">=3.9",
        install_requires=[
            "numpy>=1.21.0",
            "pandas>=1.3.0",
            "gpxpy>=1.5.0",
            "ffmpeg-python>=0.2.0",
            "geopandas>=0.12.0",
            "contextily>=1.3.0",
            "matplotlib>=3.5.0"
        ],
        url="https://github.com/ozand/pygpmf-oz",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Operating System :: OS Independent",
        ]
    )
