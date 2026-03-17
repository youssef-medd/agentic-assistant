import ollama
try:
    response = ollama.chat(model='llama3.2', messages=[
        {'role': 'user', 'content': 'Is the brain online?'},
    ])
    print("--- RESPONSE FROM AI ---")
    print(response['message']['content'])
    print("-------------------------")
except Exception as e:
    print(f"ERROR: {e}")