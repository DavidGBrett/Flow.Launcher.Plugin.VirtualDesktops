import shutil
import os
from pathlib import Path
import subprocess
import sys
    

def build():

    script_dir = Path(__file__).parent.resolve()

    build_dir = script_dir / "build"

    lib_dir = build_dir / "lib"

    requirements_path = build_dir / "requirements.txt"

    dist_dir = script_dir / "dist"

    zip_path = dist_dir / "VirtualDesktopSwitcher"


    # remove build dir if it already exists
    if build_dir.exists():
        shutil.rmtree(build_dir)

    # make build dir
    build_dir.mkdir(parents=True, exist_ok=True)

    # copy to the build dir
    shutil.copytree(
        script_dir, 
        build_dir, 
        dirs_exist_ok=True,
        ignore=lambda path,names:('.git', ".venv", "build", "build.py", ".github", "dist")
    )

    # install dependencies
    lib_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,  # current Python interpreter
        "-m", 
        "pip", "install",
        "-t", lib_dir,
        "-r", requirements_path
    ]

    cmd_using_module = cmd
    cmd_without_module = cmd[2:]

    try:
        subprocess.run(cmd_without_module, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e1:

        try: subprocess.run(cmd_using_module, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e2:
            print("Trying without module:",e1.stderr)
            print("Trying with module:",e2.stderr)
            sys.exit(1)

    
    # zip build and put in dist
    dist_dir.mkdir(parents=True, exist_ok=True)

    shutil.make_archive(zip_path.as_posix(), 'zip', build_dir)

if __name__ == "__main__":
    build()