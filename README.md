🧠 CEREBRO: Data Sovereignty & AI Ecosystem
CEREBRO, modern işletmelerin en büyük sorunu olan veri sızıntısı riskine karşı, "Veri Egemenliği" (Data Sovereignty) ilkesiyle geliştirilmiş, %100 yerel (offline) çalışan bir yapay zeka ekosistemidir.   

🛡️ Mimari Vizyon: Air-Gapped Güvenlik
Bu sistem, buluta veri gönderen sıradan araçların aksine, internete tamamen kapalı (air-gapped) bir makinede çalışacak şekilde tasarlanmıştır.   

Gizlilik: Şirketin verisi, şirketin fiziksel sınırları içinde kalır.   

Uyumluluk: Mimari, Avrupa GDPR (DSGVO) standartlarına %100 uyumlu olması için özel olarak yapılandırılmıştır.   

⚙️ Çift Motorlu Veri Tabanı Mimarisi
Sıradan bir veri tabanı kaydının ötesinde, sistem iki farklı "organ" ile çalışır:   

Vektör Hafıza (ChromaDB): * RAG (Retrieval-Augmented Generation) mimarisi entegre edilmiştir.   

Yüzlerce sayfalık PDF ve kurumsal raporları saniyeler içinde okuyup vektörlere (sayılara) çevirerek yerel hafızasına alır.   

Audit Log Kasası (SQLite - Kara Kutu): * Yapay zekadan bağımsız çalışan ilişkisel bir denetim kaydı sistemidir.   

Hangi kullanıcının saat kaçta ne sorduğunu saniyesi saniyesine şifreli bir şekilde kaydeder.   

📊 Çok Yönlü Yetenek: Veri Analizi ve Görselleştirme
CEREBRO sadece bir sohbet arayüzü değil, aynı zamanda bir veri analistidir:   

Excel İşleme: Karmaşık Excel dosyalarını okuyup analiz edebilir.   

Görselleştirme: Verileri anında kurumsal grafiklere dönüştürerek temiz bir Streamlit arayüzüyle sunar.   

📂 Teknik Standartlar
Modüler Yapı: Proje; app.py, audit_logger.py ve hafıza modülleri gibi parçalara ayrılarak Temiz Kod (Clean Code) prensipleriyle yazılmıştır.   

Versiyon Kontrolü: Tüm geliştirme süreci Git sistemiyle profesyonel iş akışlarına uygun yönetilmektedir.   

🚀 Kurulum ve Çalıştırma

Gerekli kütüphaneleri yükleyin:

Bash
pip install -r requirements.txt
Sistemi başlatın:

Bash
streamlit run app.py
