from ollama import chat

def generate(prompt):
    messages = [
    {
        'role': 'user',
        'content': prompt,
    },
    ]

    for part in chat('llama2-uncensored', messages=messages, stream=True):
        print(part['message']['content'], end='', flush=True)

    # end with a newline
    print()

print(generate("why"))