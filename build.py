import argparse
import json
import shutil
import os
from pathlib import Path
import subprocess
import sys
import fnmatch
    
def get_ignore_func():
    # Assumes this script is in the root directory
    root_dir = Path(__file__).parent.resolve()

    build_ignore_path = root_dir / "build_ignore.json"

    with open(build_ignore_path) as build_ignore_file:
        build_ignore = json.load(build_ignore_file)
        root_level_ignores:list[str] = build_ignore["root_level"]
        any_level_ignores:list[str]  = build_ignore["any_level"]

    def ignore_func(path:str,names:list[str]) -> set[str]:
        ignored_names = set()

        # if we are at the root level
        if root_dir.match(path):
            #ignore file/dir if its name matches any pattern in root_level_ignores
            for name in names:
                for pattern in root_level_ignores:
                    if fnmatch.fnmatch(name, pattern):
                        ignored_names.add(name)

        # ignore file/dir if its name matches any pattern in any_level_ignores
        for name in names:
            for pattern in any_level_ignores:
                if fnmatch.fnmatch(name, pattern):
                    ignored_names.add(name)

        
        return ignored_names
    return ignore_func
        


def build(dist_dir_name,output_file_name):

    # Assumes this script is in the root directory
    root_dir = Path(__file__).parent.resolve()

    build_dir = root_dir / "build"

    lib_dir = build_dir / "lib"

    requirements_path = build_dir / "requirements.txt"

    dist_dir = root_dir / dist_dir_name

    zip_path = dist_dir / output_file_name


    # remove build dir if it already exists
    if build_dir.exists():
        shutil.rmtree(build_dir)

    # make build dir
    build_dir.mkdir(parents=True, exist_ok=True)

    # copy to the build dir
    shutil.copytree(
        root_dir, 
        build_dir, 
        dirs_exist_ok=True,
        ignore=get_ignore_func()
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

    # remove dist dir if it already exists
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    # create dist dir
    dist_dir.mkdir(parents=True, exist_ok=True)

    # zip build and put in dist
    shutil.make_archive(zip_path.as_posix(), 'zip', build_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build script')

    parser.add_argument('--output-dir', '-d', type=str, default='dist', 
                       help='Output directory name (relative to root)')
    parser.add_argument('--filename', '-f', type=str, default='build',
                       help='Output filename (without extension)')

    args = parser.parse_args()
    
    build(
        dist_dir_name=args.output_dir,
        output_file_name=args.filename
    )