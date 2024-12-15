import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = os.getenv("nvidia_api_key")
)

completion = client.chat.completions.create(
  model="nvidia/llama-3.1-nemotron-70b-reward",
  messages=[{"role":"user",
             "content":input("User_Input : ")},
            {"role":"assistant",
             "content":input("AI-Response :")}
             ],
)
# print(completion)
# Parse the JSON response and print the reward
response_json = completion.to_dict()
reward = response_json['choices'][0]['message']['content'].split(':')[1]
print(f"Reward: {reward}")