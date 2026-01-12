Installation
============

Install from PyPI
-----------------

The easiest way to install pygpmf_oz is using pip:

.. code-block:: bash

   pip install pygpmf-oz

Install from Source
-------------------

Clone the repository and install:

.. code-block:: bash

   git clone https://github.com/ozand/pygpmf-oz.git
   cd pygpmf_oz
   pip install -e .

Requirements
------------

* Python 3.9 or higher
* numpy >= 1.21.0
* pandas >= 1.3.0
* ffmpeg-python >= 0.2.0
* gpxpy >= 1.5.0
* geopandas >= 0.12.0
* matplotlib >= 3.5.0
* contextily >= 1.3.0

System Requirements
-------------------

**FFmpeg** must be installed on your system to extract GPMF streams from video files.

**Windows:**

.. code-block:: bash

   # Using Chocolatey
   choco install ffmpeg

   # Or download from https://ffmpeg.org/download.html

**macOS:**

.. code-block:: bash

   brew install ffmpeg

**Linux:**

.. code-block:: bash

   sudo apt install ffmpeg  # Ubuntu/Debian
   sudo dnf install ffmpeg  # Fedora
