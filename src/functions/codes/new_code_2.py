import os
from pywinauto.application import Application

import pywinauto.keyboard as keyboard

def write_code(code: str) -> str:
    print("I will write the code")
    
    # Get the current directory of the file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Create a new folder named 'codes' if it doesn't exist
    codes_directory = os.path.join(current_directory, 'codes')
    if not os.path.exists(codes_directory):
        os.makedirs(codes_directory)
    
    # Define the new file path
    new_file_path = os.path.join(codes_directory, 'new_code.py')
    
    # Open VS Code
    try:
        app = Application().start(r"C:\\Users\\harsh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
        # Wait for VS Code to open
        app.window(title_re=".*Visual Studio Code.*", visible_only=True).wait('ready', timeout=30)
    except Exception as e:
        print(f"Error opening VS Code: {e}")
        return "Failed to open VS Code"
    
    # Open the command palette
    keyboard.send_keys('^`')
    
    # Create a new file
    keyboard.send_keys('^n')
    
    # Write the code into the new file
    with open(new_file_path, 'w') as file:
        file.write(code)
    
    # Open the new file in VS Code
    keyboard.send_keys('^o')
    keyboard.send_keys(new_file_path)
    keyboard.send_keys('{ENTER}')
    
    return "Code written successfully"