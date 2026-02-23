import os
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate 
from document_processor import search_in_pdf
from system_prompts import get_cerebro_prompt

# M2 Mac için hızlı model
MODEL_NAME = "llama3:8b-instruct-q4_0"

def ask_cerebro(user_message, selected_language="Türkçe"):
    # 1. PDF hafızasında derin arama (k=8 ayarıyla gelir)
    pdf_context = search_in_pdf(user_message) 
    
    # 2. Sistem talimatını al
    system_instruction = get_cerebro_prompt(selected_language)
    
    # 3. Sohbet kontrolü
    sohbet_kelimeleri = ["merhaba", "selam", "nasılsın", "kimsin"]
    is_chat = any(word in user_message.lower() for word in sohbet_kelimeleri)

    if pdf_context.strip() != "" and not is_chat:
        # PDF sorusuysa direkt kaynağa odaklanmasını sağlayan temiz prompt
        augmented_message = (
            f"KAYNAK METİN:\n{pdf_context}\n\n"
            f"SORU: {user_message}\n\n"
            f"TALİMAT: Yukarıdaki kaynak metne göre soruyu yanıtla. "
            f"Eğer metinde Tablo veya Analiz sonuçları varsa katsayıları net ver."
        )
    else:
        augmented_message = user_message
    
    # 4. Prompt Yapısı
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_instruction),
        ("user", "{input}")
    ])
    
    try:
        llm = Ollama(model=MODEL_NAME)
        chain = prompt_template | llm
        response = chain.invoke({"input": augmented_message})
        return response
    except Exception as e:
        return f"CEREBRO Hatası: {str(e)}"
    