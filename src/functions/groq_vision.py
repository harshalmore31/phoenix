import os
import groq
import base64
from PIL import ImageGrab
from dotenv import load_dotenv

load_dotenv()

def check_my_screen():
# Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    screenshot = ImageGrab.grab()
    img = screenshot
    img.save('image.jpg')

    image_path = "image.jpg"

    # Get base64 encoded image
    base64_image = encode_image(image_path)

    client = groq.Client(api_key=os.environ["GROQ_API_KEY"])

    completion = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe the image in detailed"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

