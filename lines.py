import os

def count_lines_in_current_folder():
    folder_path = os.getcwd()
    total_lines = 0

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(".py"):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r") as file:
                    lines = file.readlines()
                    total_lines += len(lines)

    return total_lines

print(count_lines_in_current_folder())