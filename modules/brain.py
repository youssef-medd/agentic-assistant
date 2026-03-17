import ollama
def ask_ollama(question, context=""):
    prompt = f"Context: {context}\n\nQuestion: {question}"
    response = ollama.chat(
        model='llama3.2', 
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content']
