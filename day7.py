"""
Day 7 of Advent Of Code 2022
https://adventofcode.com/2022/
"""
import os
import re
import sys

import requests

SESSION_KEY = {"session": os.environ.get("SESSION_KEY", None)}
DAY = int(re.findall(r"[0-9]+", sys.argv[0].rsplit("/", maxsplit=1)[-1])[0])


response = requests.get(
    f"https://adventofcode.com/2022/day/{DAY}/input", cookies=SESSION_KEY, timeout=500
)

data = response.text.strip()  # .split("\n")

data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

# print(data)


class Folder:
    """Folder Class"""

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.files = []
        self.subfolders = []
        self.size = 0

        if self.parent:
            self.path = self.parent.path + f"{self.name}/"
        else:
            self.path = "/"

    def info(self):
        info_str = f"Current folder: {self.path}"
        info_str += f"\nSubdirectories: {self.subfolders}"
        info_str += f"\nFiles: {self.files}"
        info_str += f"\nFolder size: {self.size}"
        info_str += "\n" + "=" * 100
        return info_str

    def ls(self):
        """List the content of the folder"""
        if len(self.files) == 0 and len(self.subfolders) == 0:
            print("Folder is empty")
        for folder in self.subfolders:
            print(f"dir {folder.name}")
        for file_ in self.files:
            print(f"{file_.filename} {file_.size}")

    def get_size(self, maxsize=None):
        """Get size of folder

        Args:
            maxsize (int, optional): The maximum size of folders to Return. Defaults to None.

        Returns:
            int: Size of files in folder and subfolders
        """
        return sum(f.size for f in self.files)

    def add_folder(self, name):
        """Add a subfolder to the current folder

        Args:
            name (str): Name of folder
        """
        self.subfolders.append(
            Folder(
                name,
                parent=self,
            )
        )

    def add_file(self, filename, size):
        """Add a file to the folder

        Args:
            filename (str): Name of file
            size (int): File size
        """
        self.files.append(File(self, filename, size))
        self.size += int(size)

    def __repr__(self) -> str:
        # return f"(Folder): {self.path}"
        return f"{self.path}"


class File:
    """File Class"""

    def __init__(self, folder, filename, size):
        self.folder = folder
        self.filename = filename
        self.size = int(size)

    def get_size(self):
        """Get the size of the file

        Returns:
            int: File size
        """
        return self.size

    def __repr__(self):
        return f"(File) {self.filename} - {self.size}"


def cd(folder, arg):
    """Change Directory

    Args:
        folder (Folder): Current folder
        arg (str): Folder to change into

    Returns:
        Folder: New current folder
    """
    # print(f"(func) CD: {folder, arg}")
    if arg == "/":
        # print("/")
        return root_folder
    elif arg == "..":
        # print(folder.parent.path)
        return folder.parent
    else:
        for f in folder.subfolders:
            # print("SUBFOLDER NAMES:", f.name)
            if arg == f.name:
                return f
        print(f"No folder {arg}")
        return folder


def ls(folder, new_objects, add_objects=False):
    """Create new files or folders from listing a folder

    Args:
        folder (Folder): Current working folder
        output (List): List of files and folders

    Returns:
        None: None
    """
    # print(f"(func) LS: {folder}")
    for row in new_objects:
        if row.startswith("dir"):
            folder.add_folder(row[4:])
        else:
            size, filename = row.split()
            folder.add_file(filename, size)
    # return folder.ls()
    return None


operations = []

operation = []
new_operation = True

for line in data.split("\n"):
    if line.startswith("$"):
        if operation:
            operations.append(operation)
        operation = []

    operation.append(line)
operations.append(operation)

root_folder = Folder("/")

cwd = root_folder
# print(cwd)
for operation in operations:
    # print(cwd, root_folder.subfolders)
    if len(operation) == 1:
        command, output = operation[0], ""
    else:
        command, output = operation[0], operation[1:]

    # print(command)

    if command.startswith("$ cd"):
        new_folder = command[5:]
        # print(operation, command, arg)
        if new_folder == "/":
            cwd = root_folder
        else:
            cwd = cd(cwd, new_folder)

    elif command.startswith("$ ls"):
        ls(cwd, output)
    else:
        print("NOT A COMMAND")

    # print(cwd)

    # print(command, output)

# print(root_folder.get_size())

# Check directories less than maxsize
total = 0
# for f in root_folder.subfolders:
#     # print(f.get_size(100000))
#     print(f.get_size())
#     total += f.get_size()

# print(total)


folder_sizes = {}

pattern = [root_folder]


def add_sub(rf, l=[]):
    for f in rf.subfolders:
        if not f.subfolders:
            l.append(f)
        else:
            f = add_sub(f, l)
            l.append(f)

    return l


pattern.append(add_sub(pattern[0]))

# print(len(pattern))
# for p in pattern:
#     if isinstance(p, Folder):
#         print(p.subfolders)
#     else:
#         for p1 in p:
#             print(p1)
#         print(p, type(p))


def all_below(root_dir, maxsize=1000000):
    if root_dir.size <= maxsize:
        yield root_dir

    for d in root_dir.subfolders:
        yield from all_below(d, maxsize)


# print(sum(d.size for d in all_below(root_folder)))

print(root_folder.info())
print(root_folder.subfolders[0].info())
