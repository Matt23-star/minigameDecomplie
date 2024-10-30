import os
import shutil
import argparse

parser = argparse.ArgumentParser(description="Unpack wxapkg files.")
parser.add_argument('-s', '--source', required=True, help='Source directory path')
parser.add_argument('-t', '--target', required=True, help='Target directory path')


def unpack_wxapkg(source, target):
    rename_sorted_files_by_mtime("..\\wxpack")

    main_file = f"{source}\\main.wxapkg"
    if os.path.exists(main_file):
        run_command(f"node .\\wuWxapkg.js {main_file}")
    else:
        print("main.wxapkg not found.")
        return

    # Get the number of files in the source directory
    num_files = len([name for name in os.listdir(source) if os.path.isfile(os.path.join(source, name))])

    for i in range(1, num_files-1):
        file = f"{source}\\pkg{i}.wxapkg"
        if os.path.exists(file):
            run_command(f"node .\\wuWxapkg.js {file}")
            path = f"{source}\\pkg{i}"
            move_subpackage(path, target)

def run_command(command):
    os.system(command)

def rename_sorted_files_by_mtime(directory):
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    files = [f for f in files if os.path.isfile(f)]
    files.sort(key=os.path.getmtime)

    # 重命名文件
    for i, file in enumerate(files):
        if i == 0:
            new_name = os.path.join(directory, "..\\wxpack\\main.wxapkg")
        else:
            new_name = os.path.join(directory, f"..\\wxpack\\pkg{i}.wxapkg")
        os.rename(file, new_name)

def move_subpackage(path, target):
    if os.path.exists(path):
        for item in os.listdir(path):
            s = os.path.join(path, item)
            d = os.path.join(target, item)
            print(s + " -> " + d)
            if os.path.isdir(s):
                if not os.path.exists(d):
                    os.makedirs(d)
                for root, dirs, files in os.walk(s):
                    for dir_ in dirs:
                        os.makedirs(os.path.join(d, os.path.relpath(os.path.join(root, dir_), s)), exist_ok=True)
                    for file_ in files:
                        shutil.move(os.path.join(root, file_), os.path.join(d, os.path.relpath(os.path.join(root, file_), s)))
            else:
                shutil.move(s, d)


if __name__ == "__main__":
    args = parser.parse_args()
    unpack_wxapkg(args.source, args.target)