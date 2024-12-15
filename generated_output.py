import pyautogui
import time
import pyperclip

try:
    pyautogui.hotkey('win')
    time.sleep(2)
    pyautogui.typewrite('notepad')
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'n')
    time.sleep(2)

    essay_lines = [
        "Artificial Intelligence: A Paradigm Shift",
        "",
        "Artificial intelligence (AI) is rapidly transforming our world, permeating various aspects of our lives, from the mundane to the extraordinary.  This essay explores the multifaceted nature of AI, its potential benefits, and the challenges it presents.",
        "",
        "At its core, AI involves the creation of intelligent agents, which are systems that can reason, learn, and act autonomously. This capability is achieved through a variety of techniques, including machine learning, deep learning, and natural language processing.  Machine learning algorithms enable computers to learn from data without explicit programming, while deep learning utilizes artificial neural networks to extract complex patterns from vast datasets. Natural language processing allows machines to understand and interact with human language.",
        "",
        "The potential benefits of AI are vast.  In healthcare, AI can assist in diagnosis, drug discovery, and personalized medicine.  In transportation, self-driving cars promise to reduce accidents and improve traffic flow. In manufacturing, AI-powered robots can increase efficiency and productivity.  Moreover, AI can contribute to scientific discovery, environmental protection, and even artistic expression.",
        "",
        "However, the rise of AI also presents significant challenges.  One major concern is job displacement, as AI-powered systems could automate many tasks currently performed by humans.  Another concern is the ethical implications of AI, particularly regarding bias, privacy, and accountability.  As AI systems become more sophisticated, ensuring their fairness, transparency, and safety becomes paramount.",
        "",
        "Furthermore, the development of advanced AI raises questions about the very nature of intelligence and consciousness.  Could machines one day surpass human intelligence?  If so, what are the implications for humanity?  These are profound questions that require careful consideration.",
        "",
        "In conclusion, artificial intelligence represents a paradigm shift in our technological landscape.  While it offers tremendous potential for progress, it also poses significant challenges that we must address responsibly.  As we navigate this new era of intelligent machines, a balanced approach that prioritizes human well-being and ethical considerations is essential."
    ]


    for line in essay_lines:
        pyperclip.copy(line)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

except Exception as e:
    print(f"An error occurred: {e}")