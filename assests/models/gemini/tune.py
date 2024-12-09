import time, json
import pandas as pd
import seaborn as sns
import google.generativeai as genai


genai.configure(api_key="gemini-api1-key")
base_model = "models/gemini-1.5-flash-001-tuning"


loaded_training_data = []
with open('training_data.jsonl', 'r') as file:
    for line in file:
        loaded_training_data.append(json.loads(line))

training_data = loaded_training_data

# with open('xyz.txt','a') as x:
#     for i in training_data:
#         stu = str(i)
#         x.write(stu + "\n")

operation = genai.create_tuned_model(
    # You can use a tuned model here too. Set `source_model="tunedModels/..."`
    display_name="Mental_Health_Assistant",
    description="This dataset is designed to fine-tune a large language model (LLM) for mental health support conversations with young adults aged 15-21. The model will be trained to recognize and categorize various mental health issues, assess anxiety levels, identify potential underlying conditions, and suggest appropriate solutions. It aims to provide helpful and empathetic responses while acknowledging the limitations of an AI model and encouraging professional help when needed. The model is not intended to replace human interaction with healthcare professionals but to serve as a supportive tool for young adults navigating mental health challenges.",
    source_model=base_model,
    epoch_count=4,
    batch_size=4,
    learning_rate=0.001,
    training_data=loaded_training_data,
)

for status in operation.wait_bar():
    time.sleep(10)

result = operation.result()
print(result)
snapshots = pd.DataFrame(result.tuning_task.snapshots)
sns.lineplot(data=snapshots, x='epoch', y='mean_loss')

model = genai.GenerativeModel(model_name=result.name)
result = model.generate_content("My somatch is paining and I am feeling very exhauseted")
print(result.text)  # IV

