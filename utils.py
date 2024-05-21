import openai
import config

openai.api_key = config.OPENAI_API_KEY


def load_prompt(file_name):
    with open(f"prompts/{file_name}", "r", encoding="utf-8") as file:
        return file.read()


def get_chatgpt_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()
