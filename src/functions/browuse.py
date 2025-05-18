from browser_use import Agent, Browser, BrowserConfig
from langchain_community.chat_models import ChatLiteLLM
import asyncio
import time
from dotenv import load_dotenv
from sqlalchemy import false
load_dotenv()

# Configure the browser to connect to your Chrome instance
config = BrowserConfig(
    headless=False,
    disable_security=True,
    chrome_instance_path="C:/Program Files/Google/Chrome/Application/chrome.exe"
)
browser = Browser(config)

# Create the agent with your configured browser
agent = Agent(
    task="Open YouTube, search welcome to hood and play the video",
    llm=ChatLiteLLM(model='gpt-4o-mini'),
    browser=browser,
)

async def main():
    # Run the agent to perform the task
    await agent.run()
    
    print("Task completed. Browser will remain open until you stop the program.")
    print("Press Ctrl+C to stop the program and close the browser.")
    
    # Keep the program running indefinitely
    try:
        # This will keep the program running without closing Chrome
        while True:
            await asyncio.sleep(1)  # Sleep to prevent high CPU usage
    except KeyboardInterrupt:
        # Handle when user presses Ctrl+C to exit
        print("\nClosing browser and exiting program...")
    finally:
        # Ensure browser closes when program exits
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())