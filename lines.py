import os

def count_lines_in_current_folder():
    folder_path = os.getcwd()
    total_lines = 0
    file_names = {}

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(".py"):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r") as file:
                    lines = file.readlines()
                    file_names[file_name] = len(lines)
                    
                    total_lines += len(lines)

    return total_lines, file_names

lines, files = count_lines_in_current_folder()

files = dict(sorted(files.items()))

print('______________________________')
for file in files:
    
    lns = files[file]

    print(f'|{file} : {lns} lines |')
    print('______________________________')
    
print(f'|total lines {lines}             |')
