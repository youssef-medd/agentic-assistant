import ollama
try:
    response = ollama.chat(model='llama3.2', messages=[
        {'role': 'user', 'content': 'Is the brain online?'},
    ])
    print(response['message']['content'])
except Exception as e:
    print(f"ERROR: {e}")