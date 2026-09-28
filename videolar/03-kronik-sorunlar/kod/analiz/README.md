# V2 veri çekme kodu

```bash
cd ~/Files/Projects/KokNeden/Content/03-kronik-sorunlar/kod
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python veri_cek.py
```

- Göstergeler `gosterge_listesi.csv` içinde; yeni gösterge eklemek için satır eklemek yeterli.
- API yanıtları `veri/ham/api/` altında önbelleğe alınır; tazelemek için o klasörü sil.
- Maddison, PWT, V-Dem ve elle derlenen seriler için dosyaları `veri/ham/` altına koy (adlar `veri_cek.py` başında).
- Çekilemeyenler `veri/eksikler.csv` dosyasına yazılır; kod durmaz.
