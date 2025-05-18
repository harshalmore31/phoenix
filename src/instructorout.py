import instructor
import google.generativeai as genai

# Configure the Gemini client
client = instructor.from_gemini(
    client=genai.GenerativeModel(
        model_name="models/gemini-1.5-flash-latest",
    ),
    mode=instructor.Mode.GEMINI_JSON,
)

# Generate and display raw output
response = client.messages.create(
    messages=[
        {
            "role": "user",
            "content": "Extract: Jason is 25 years old.",
        }
    ]
)

print(response)
