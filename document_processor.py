import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Ayarlar
PERSIST_DIRECTORY = "db_cerebro"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def process_and_save_pdf(file_path):
    """PDF'i okur, parçalara böler ve vektör veritabanına kaydeder."""
    # 1. PDF'i Yükle
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # 2. Metni Küçük Parçalara Böl (Tabloları kaçırmamak için chunk_overlap önemli)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    
    # 3. Embeddings Modelini Hazırla
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    # 4. Vektör Veritabanını Oluştur ve Kaydet
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    
    return len(chunks)

def search_in_pdf(query):
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    if os.path.exists(PERSIST_DIRECTORY):
        vector_store = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=embeddings
        )
        
        # k=8 yapıyoruz ki dökümanın neredeyse %20'sini tek seferde tarasın
        results = vector_store.similarity_search(query, k=8) 
        
        # Verileri birleştirirken araya belirgin çizgiler ekleyelim ki LLM karışıklığı anlasın
        context = "\n--- SAYFA PARÇASI ---\n".join([doc.page_content for doc in results])
        return context
    
    return ""


