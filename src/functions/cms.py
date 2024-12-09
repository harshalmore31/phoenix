import PIL
import google.generativeai as genai
from PIL import ImageGrab

def check_my_screen():
    # img = PIL.Image.open('image.jpg')
    # Capture screenshot of current window
    screenshot = ImageGrab.grab()
    img = screenshot
    img.save('image.jpg')

    genai.configure(api_key="AIzaSyDkfYex8fyClLkv33P4JXgoCmurwYX4-aY")

    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="You are an Image, describe agent, your role is to describle each detail on the image that you recive such that it will help, to understand which button is where and what is on-going in the image, provide the description with clarity"
    )

    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(["describe image", img])
    fresp = response.text
    return fresp
