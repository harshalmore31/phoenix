import webbrowser
import keyboard
import time

def write_in_document(text: str) -> None:
    """
    Creates a new Google Doc and writes formatted text.
    
    Args:
        text (str): The text content to write in the document
    """
    print("Creating new document...")
    # Open a new Google Doc
    webbrowser.open("https://docs.new")
    
    # Wait for the document to load
    time.sleep(10)  # Increased wait time for slower connections
    
    # Press Enter to bypass any initial dialogs
    keyboard.press_and_release('enter')
    time.sleep(2)
    
    # Write the text content
    for line in text.split('\n'):
        keyboard.write(line)
        keyboard.press_and_release('enter')
        time.sleep(0.1)  # Small delay between lines for better formatting
    
    # Optional: Save the document (Ctrl + S)
    keyboard.press_and_release('ctrl+s')

# Example usage
# roadmap_text = """# Data Structures and Algorithms (DSA) Roadmap

# ## Phase 1: Foundations (4-6 Weeks)

# ### 1. Phase Overview:
# • Goal: Build a strong foundation in basic data structures and algorithms
# """  # Truncated for brevity

# write_in_document(roadmap_text)
