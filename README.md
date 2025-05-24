# Library Manager

Library Manager je jednostavna aplikacija za upravljanje knjižničnim fondom i posudbama.

---

## Ključne značajke

- Upravljanje knjigama (naslov, autor, datum izdavanja, količina, status, žanrovi)
- Evidencija posudbi i vraćanja
- Praćenje dostupnosti primjeraka knjiga
- Grafički prikaz statistika posudbi
- Jednostavno web sučelje

---

## Instalacija i pokretanje

### Pokretanje lokalno bez Dockera

1. Kloniraj repozitorij:

   ```bash
   git clone https://github.com/loredanade/library.git
   cd library
   ```

2. Kreiraj virtualno okruženje i aktiviraj ga:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```


3. Instaliraj zavisnosti:
    ```bash
    pip install -r requirements.txt
    ```

4. Pokreni aplikaciju:
    ```bash
    python app.py
    ```

5. Otvori preglednik na [http://localhost:8080](http://localhost:8080)

---

### Pokretanje s Dockerom

Izgradi Docker image:

```bash
docker build -t library-manager:1.1 .
```

Pokreni kontejner:

```bash
docker run -p 5001:8080 library-manager:1.1
```

Otvori preglednik na [http://localhost:5001](http://localhost:5001)
