import os
import subprocess
import time
from pywinauto.application import Application

def write_code(code: str) -> str:
    print("I will write the code")

    # Get the current directory of the file
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Create a new folder named 'codes' if it doesn't exist
    codes_directory = os.path.join(current_directory, 'codes')
    if not os.path.exists(codes_directory):
        os.makedirs(codes_directory)

    # Define the base file path
    base_file_path = os.path.join(codes_directory, 'new_code.py')
    new_file_path = base_file_path

    # Check if the file already exists and rename if needed
    file_counter = 1
    while os.path.exists(new_file_path):
        new_file_path = os.path.join(codes_directory, f'new_code_{file_counter}')
        file_counter += 1

    # Write the code to the file
    try:
        with open(new_file_path, 'w') as file:
            file.write(code)
    except Exception as e:
        print(f"Error writing to file: {e}")
        return "Error writing to file"

    # Try to Open VS Code and the new file directly using subprocess
    try:
        subprocess.Popen([r"C:\Users\harsh\AppData\Local\Programs\Microsoft VS Code\Code.exe", new_file_path])

        # Optional: Wait for a short time for VS Code to start. You may need to adjust this.
        time.sleep(2)

        # Additional Optional Check: Try to connect with pywinauto to see if vs code started correctly
        app = Application()
        app.connect(title_re=".*Visual Studio Code.*")
        print("VS Code opened and connected!")

         # Send the Ctrl+S keypress to save the file
        keyboard = pywinauto.keyboard
        keyboard.send_keys('^s')
        
    except Exception as e:
        print(f"Error opening VS Code: {e}")
        return "Error opening VS Code"

    return f"Code written to {os.path.basename(new_file_path)} and opened in VS Code"

if __name__ == '__main__':
    test_code = """ 
    #include<iostream.h>
    #include<conio.h>
    """
    
    # Create some existing files to test the renaming
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'codes'), exist_ok=True)
    
    # Create 2 existing files before running the script
    
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'codes', 'new_code.py'), 'a').close()
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'codes', 'new_code_1.py'), 'a').close()
   
    result = write_code(test_code)
    print(result)
    
    # Clean up the test files (optional)
    os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'codes', 'new_code.py'))
    os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'codes', 'new_code_1.py'))