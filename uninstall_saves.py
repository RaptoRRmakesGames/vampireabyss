import os
import shutil

username = os.getlogin()

# Specify the path to the folder you want to delete
folder_path = rf'C:\Users\{username}\AppData\Local\VampireAbyss'

def main():

    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return
        
    try:
        # Use shutil.rmtree to delete the folder and its contents
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' has been deleted.")
    except Exception as e:
        print(f"An error occurred while deleting the folder\n: {e}")

        
main()