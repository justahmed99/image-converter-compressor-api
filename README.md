# Flask REST API Image Processing
Beberapa hal yang terdapat pada API ini adalah :
- API pengubahan format file gambar (untuk mengupload dan mendownload)
- Kompresi gambar (TBD)

Dependensi yang digunakan adalah sebagai berikut :
- click==8.0.3
- colorama==0.4.4
- Flask==2.0.2
- gunicorn==20.1.0
- itsdangerous==2.0.1
- Jinja2==3.0.2
- MarkupSafe==2.0.1
- Pillow==8.4.0
- Werkzeug==2.0.2

## Langkah-langkah menggunakan
- Pastikan interpreter Python 3 sudah terinstal pada komputer
- Buat virtual environment
```
python -m venv env
```
- Instal requirement pada requirements.txt
```
pip3 install -r requirements.txt
```
- Eksekusi program
```
python app.py
```