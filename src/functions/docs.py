import webbrowser
import keyboard
import time

def write_in_document(text :str) -> str:
    """Simulates creating a new document."""
    print("Let's write:")
    webbrowser.open("https://docs.new")
    time.sleep(7)
    keyboard.write(text)
