# Flask REST API Image Processing
What is provided by this webservices :
- API for changing a format of image file (user must upload an image file and desired format)
- API for image compression (user must upload an image file to be compressed)
- API for downloading result files

## Dependencies
Dependencies for this webservice :
- click==8.0.3
- colorama==0.4.4
- Flask==2.0.2
- gunicorn==20.1.0
- itsdangerous==2.0.1
- Jinja2==3.0.2
- MarkupSafe==2.0.1
- Pillow==8.4.0
- Werkzeug==2.0.2

## How to use
- Make sure that Python 3 is installed on your computer or server
- Create a virtual environment
```
python -m venv env
```
- Install requirement from requirements.txt
```
pip3 install -r requirements.txt
```
- Execute script
```
python app.py
```