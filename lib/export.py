from distutils.core import run_setup
import os
from pathlib import Path
import extract_library
import shutil

os.chdir(Path(__file__).parent)

run_setup("setup.py", script_args=["sdist"])
shutil.copy(
    f"dist/extract_library-{extract_library.__version__}.tar.gz",
    "dist/extract_library-latest.tar.gz",
)
