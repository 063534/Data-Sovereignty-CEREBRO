import ollama

def ask_cerebro(prompt, selected_language):
    try:
        # Her seferinde taze bir bağlantı kurarak "client closed" hatasını engelliyoruz
        response = ollama.chat(
            model='llama3',
            messages=[
                {
                    'role': 'system', 
                    'content': f"Sen kurumsal bir asistan olan CEREBRO'sun. Analiz dili: {selected_language}."
                },
                {'role': 'user', 'content': prompt},
            ],
        )
        return response['message']['content']
    except Exception as e:
        return f"Motor Hatası: {str(e)}"
    