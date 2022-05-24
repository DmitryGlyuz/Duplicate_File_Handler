from collections import defaultdict
import os
import sys
import hashlib


if len(sys.argv) < 2:
    print("Directory is not specified")
    exit()


# Program's start
root_dir = sys.argv[1]
os.chdir(root_dir)
full_path = os.getcwd()
file_sizes = defaultdict(set)
file_hashes = defaultdict(list)


def input_sorting_option() -> str:
    print("""\
Size sorting options:
1. Descending
2. Ascending""")
    while True:
        sorting_option = input("\nEnter a sorting option:\n")
        if sorting_option in ('1', '2'):
            break
        else:
            print("\nWrong option\n")
    return sorting_option


def collect_file_sizes():
    for root, dirs, files in os.walk(full_path):
        for name in files:
            if file_format:
                current_format = os.path.splitext(name)[-1].replace('.', '')
                if current_format != file_format:
                    continue
            file_path = os.path.join(root, name)
            file_size = os.path.getsize(file_path)
            file_sizes[file_size].add(file_path)


def print_size(size):
    print(f'\n{size} bytes')


def print_file_sizes():
    for size, files in sorted(file_sizes.items(), reverse=descending_sorting):
        if len(files) > 1:
            print_size(size)
            for file_name in files:
                print(file_name)
        else:
            file_sizes.pop(size)


def ask_yes_or_no(question: str):
    user_input = input(f"{question}\n")
    while user_input not in ("yes", "no"):
        print("Wrong option")
    if user_input == "no":
        exit()


def get_file_hash(file_path):
    md5hash = hashlib.md5()
    with open(file_path, 'rb') as file:
        chunk = None
        while chunk != b'':
            chunk = file.read(1024)
            md5hash.update(chunk)
    return md5hash.hexdigest()


def collect_hashes():
    for size, files in file_sizes.items():
        for file_name in files:
            file_hash = get_file_hash(file_name)
            if not sizes_and_hashes[size].get(file_hash):
                sizes_and_hashes[size][file_hash] = []
            sizes_and_hashes[size][file_hash].append(file_name)


def print_duplicates():
    index = 1
    for file_size, hashes in sorted(sizes_and_hashes.items(), reverse=descending_sorting):
        size_printed = False
        for file_hash, file_names in hashes.items():
            if len(file_names) < 2:
                continue
            if not size_printed:
                print_size(file_size)
                size_printed = True
            print(f"Hash: {file_hash}")
            for file_name in file_names:
                print(f"{index}. {file_name}")
                duplicates.append(file_name)
                index += 1


def delete_duplicates():
    while True:
        file_numbers = input("\nEnter file numbers to delete:\n").split(' ')
        try:
            if all(map(lambda n: 0 <= int(n) - 1 <= len(duplicates), file_numbers)):
                break
            else:
                raise ValueError
        except ValueError:
            print("\nWrong format")
    freed_up_space = 0
    for number in file_numbers:
        index = int(number) - 1
        current_file = duplicates[index]
        file_size = os.path.getsize(current_file)
        os.remove(current_file)
        freed_up_space += file_size
    print(f"'nTotal freed up space: {freed_up_space} bytes")


file_format = input("Enter file format:\n")
descending_sorting: bool = input_sorting_option() == '1'
collect_file_sizes()
print_file_sizes()
if file_sizes:
    ask_yes_or_no("Check for duplicates?")
else:
    exit()
sizes_and_hashes = defaultdict(dict)
duplicates = []
collect_hashes()
print_duplicates()
ask_yes_or_no("Delete files?")
delete_duplicates()
