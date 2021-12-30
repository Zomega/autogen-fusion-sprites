from os import walk, getcwd, mkdir
from os.path import join
from shutil import copy


path = "Battlers"
reverse_path = "reverseBattlers"


def create_folder(new_folder_path):
    # print(new_folder_path)
    try:
        mkdir(new_folder_path)
    except:
        pass


def get_reverse_folder_name(file:str):
    return file.split(".")[1]


def get_reverse_file_name(file:str):
    split = file.split(".")
    result = None
    if len(split)==3:
        head = file.split(".")[0]
        body = file.split(".")[1]
        result = f"{body}.{head}.png"
    else:
        main = file.split(".")[0]
        result = f"{main}.png"
    return result


print(" ")
print("> START\n")
for root, dirs, files in walk(path):
    # print(root, len(dirs), len(files))
    for file in files:
        file_path = join(getcwd(), root, file)
        new_folder = get_reverse_folder_name(file)
        new_folder_path = join(getcwd(), reverse_path, new_folder)
        new_file = get_reverse_file_name(file)
        new_file_path = join(getcwd(), reverse_path, new_folder, new_file)
        
        print(file_path)
        create_folder(new_folder_path)
        copy(file_path, new_file_path)

print("\n> END")
