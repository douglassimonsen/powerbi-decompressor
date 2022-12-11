from distutils.core import run_setup
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
import extract_library
import shutil


def main():
    old_dir = os.getcwd()
    os.chdir(Path(__file__).parents[1])

    run_setup("setup.py", script_args=["sdist"])
    shutil.copy(
        f"dist/extract_library-{extract_library.__version__}.tar.gz",
        "dist/extract_library-latest.tar.gz",
    )
    os.chdir(old_dir)


if __name__ == "__main__":
    main()
