import webbrowser
import keyboard
import time
from functions.cms import check_my_screen
def research(text :str) -> str:
    print("Let's research on Perplexity !")
    webbrowser.open("https://www.perplexity.ai/")
    keyboard.press_and_release('ctrl+i')
    time.sleep(6)
    keyboard.write(text)
    keyboard.press_and_release('enter')
    keyboard.press_and_release('ctrl+.')
    time.sleep(2)
    keyboard.press_and_release('f11')
    time.sleep(3)
    check_my_screen()

# research("hii")