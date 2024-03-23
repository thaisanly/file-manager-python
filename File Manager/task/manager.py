import math
import os
import re
import shutil

# run the user's program in our generated folders
os.chdir('module/root_folder')


def list_directory_contents(args, list_dir):
    try:
        contents = os.listdir(list_dir)
        dirs = [f for f in contents if os.path.isdir(os.path.join(list_dir, f))]
        files = [f for f in contents if os.path.isfile(os.path.join(list_dir, f))]

        if dirs:
            for dir in dirs:
                print(dir)

        if files:
            if args in ['l', 'lh']:
                for file in files:
                    file_path = os.path.join(list_dir, file)
                    file_stat = os.stat(file_path)

                    if 'lh' in args:
                        file_size = human_readable_size(file_stat.st_size)
                    else:
                        file_size = file_stat.st_size

                    print(f"{file} {file_size}")
            else:
                for file in files:
                    print(f"{file}")

    except:
        print(f"Invalid command")


def human_readable_size(size_bytes):
    """Converts file size to human-readable format"""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p)
    return "%s %s" % (s, size_name[i])


def get_target_file(source_path, target_path):
    if os.path.isfile(target_path):
        newFileName = os.path.basename(target_path)
    else:
        newFileName = os.path.basename(source_path)

    if target_path == '.':
        target_dir = os.getcwd()
    elif target_path == '..':
        target_dir = os.getcwd().split("/")
        target_dir.pop()
        target_dir = '/'.join(target_dir)
    else:
        target_dir = os.path.dirname(target_path)

    return os.path.join(target_dir, newFileName)


def get_file_folder(path):
    paths = path.split('/')
    paths.pop()
    return '/'.join(paths)


def is_extension(string):
    pattern = r"\.([a-zA-Z0-9]{2,4})$"
    return bool(re.match(pattern, string))


# put your code here
while True:

    user_input = input()
    paths = user_input.split(" ")

    if user_input.startswith('pwd'):
        print(os.getcwd())
    elif user_input.startswith('cp'):

        if len(paths) < 3:
            print("Specify the file")
            continue

        if len(paths) > 3:
            print("Specify the current name of the file or directory and the new location and/or name")
            continue

        # perform copy file by extension to directory
        if is_extension(paths[1]) and os.path.isdir(paths[2]):

            files = [f for f in os.listdir(os.getcwd()) if f.endswith(paths[1])]

            if len(files) <= 0:
                print("File extension {extension} not found in this directory".format(extension=paths[1]))

            for file in files:

                target_file = os.path.join(paths[2], file)

                if os.path.exists(target_file):
                    is_override = input("{filename} already exists in this directory. Replace? (y/n)".format(filename=file))

                    if is_override == 'y':
                        os.remove(target_file)
                        shutil.copyfile(file, target_file)
                else:
                    shutil.copyfile(file, target_file)
            continue

        target_file = get_target_file(paths[1], paths[2])
        target_dir = get_file_folder(target_file)

        if not os.path.exists(target_dir):
            print("No such file or directory")
            continue

        if os.path.exists(target_file):
            print("{filename} already exists in this directory".format(filename=target_file))
            continue

        shutil.copyfile(paths[1], target_file)

    elif user_input.startswith('ls'):

        args = []
        list_dir = "."

        for path in paths:
            if '-' in path:
                args = path.replace("-", "")
                break

        list_directory_contents(args, list_dir)

    elif user_input.startswith('rm'):

        if len(paths) < 2:
            print("Specify the file or directory")
            continue

        if is_extension(paths[1]):

            files = [f for f in os.listdir(os.getcwd()) if f.endswith(paths[1])]

            if len(files) <= 0:
                print("File extension {extension} not found in this directory".format(extension=paths[1]))
            else:
                for file in files:
                    os.remove(file)
        else:

            if not os.path.exists(paths[1]):
                print("No such file or directory")
                continue

            if os.path.isdir(paths[1]):
                shutil.rmtree(paths[1])
            else:
                os.remove(paths[1])

    elif user_input.startswith('mv'):

        if len(paths) < 3:
            print("Specify the current name of the file or directory and the new location and/or name")
            continue

        # perform moving file by extension into directory
        if is_extension(paths[1]) and not os.path.splitext(paths[2])[1]:

            files = [f for f in os.listdir(os.getcwd()) if f.endswith(paths[1])]

            if len(files) <= 0:
                print("File extension {extension} not found in this directory".format(extension=paths[1]))
            else:

                for file in files:

                    target_file = os.path.join(paths[2], file)

                    if os.path.exists(target_file):
                        is_override = input("{filename} already exists in this directory. Replace? (y/n)".format(filename=file))

                        if is_override == 'y':
                            os.remove(target_file)
                            shutil.move(file, target_file)
                    else:
                        shutil.move(file, target_file)
            continue

        if not os.path.exists(paths[1]):
            print("No such file or directory")
            continue

        if os.path.isfile(paths[2]) and os.path.exists(paths[2]):
            print("The file or directory already exists")
            continue

        if os.path.isdir(paths[2]):
            shutil.move(paths[1], paths[2])
        else:
            dir_name = os.path.dirname(paths[2])

            if dir_name and not os.path.exists(dir_name):
                os.mkdir(dir_name)

            shutil.move(paths[1], paths[2])

    elif user_input.startswith('mkdir'):

        if len(paths) < 2:
            print("Specify the name of the directory to be made")
            continue

        if os.path.exists(paths[1]):
            print("The directory already exists")
            continue

        os.mkdir(paths[1])

    elif user_input == "cd module":
        os.chdir("../../module")
        print(os.path.basename(os.getcwd()))
    elif user_input.startswith('cd'):

        if len(paths) <= 1:
            print("Invalid command")
        else:
            os.chdir(paths[1])
            folders = os.getcwd().split("/")
            print(folders[-1])
    else:
        print("Invalid command")
