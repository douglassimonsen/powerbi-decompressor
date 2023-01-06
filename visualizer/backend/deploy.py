import shutil
from pathlib import Path
import os
import subprocess
import zipfile

local_dir = Path(__file__).parent


def gen_dist_folder():
    if os.path.exists(local_dir / "dist"):
        shutil.rmtree(local_dir / "dist")
    os.makedirs(local_dir / "dist")

    for f in ("app.py", "application.py", "util.py"):
        shutil.copy(local_dir / f, local_dir / "dist")
    shutil.copytree(local_dir / "static", local_dir / "dist" / "static")
    shutil.copytree(
        local_dir / "lambda_psycopg2", local_dir / "dist" / "psycopg2"
    )  # this keeps psycopg2 from overshadowing things locally
    subprocess.Popen(
        ["pip3", "install", "-r", "requirements.txt", "-t" "dist/"],
        cwd=str(local_dir),
        stdout=subprocess.DEVNULL,
    ).communicate()


def package():
    with zipfile.ZipFile(local_dir / "lambda.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        dist_prefix = len(str(local_dir / "dist")) + 1
        for dir, _, files in os.walk(local_dir / "dist"):
            for f in files:
                file_path = os.path.join(dir, f)
                zipf.write(file_path, arcname=file_path[dist_prefix:])
    shutil.move(
        local_dir / "lambda.zip", local_dir.parents[1] / "docker-assets/lambda.zip"
    )
    shutil.rmtree(local_dir / "dist")


def main():
    gen_dist_folder()
    package()


if __name__ == "__main__":
    main()
