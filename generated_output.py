import pyautogui
import time
import sys

try:
    # Use hotkey to open the search tool (Win key for Windows)
    pyautogui.hotkey('win')
    time.sleep(2)

    # Type 'chrome' to search for the application
    pyautogui.write('chrome', interval=0.1)
    time.sleep(2) # Wait for search results

    # Press Enter to launch Chrome
    pyautogui.press('enter')
    time.sleep(4) # Wait for Chrome to open

    # Open a new tab
    pyautogui.hotkey('ctrl', 't')
    time.sleep(2) # Wait for the new tab to open

    # Type the search query
    search_query = "the best AI model in 2025"
    pyautogui.write(search_query, interval=0.05)
    time.sleep(1)

    # Press Enter to perform the search
    pyautogui.press('enter')

except Exception as e:
    print(f"An error occurred: {e}")
    print("Suggestions:")
    print("- Ensure Chrome is installed and accessible via the Windows search.")
    print("- Check if PyAutoGUI is installed ('pip install pyautogui').")
    print("- Make sure no other window unexpectedly takes focus during execution.")
    sys.exit(1)