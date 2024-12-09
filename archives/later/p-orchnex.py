import google.generativeai as genai

genai.configure(api_key='enter api key')

# To checkout all the available gemini models

# for x in genai.list_models():
#     print(x.name)

Refiner = genai.GenerativeModel(
    "gemini-1.5-flash-8b-exp-0924",
    generation_config=genai.GenerationConfig()
    )

test = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config=genai.create_tuned_model(
        training_data=training_data,
    )
)