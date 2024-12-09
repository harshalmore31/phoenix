import webbrowser
import keyboard
import time

def research(text :str) -> str:
    print("Let's research on Perplexity !")
    webbrowser.open("https://www.perplexity.ai/")
    time.sleep(7)
    keyboard.write(text)
    keyboard.press_and_release('enter')
    keyboard.press_and_release('ctrl+.')

# research("hii")