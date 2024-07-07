from flask import Flask, render_template, request, redirect, url_for, send_file
import requests
import io
import mimetypes
from urllib.parse import urlparse, unquote
import os

app = Flask(__name__)

downloaded_content = []

@app.route('/')
def index():
    return render_template('index.html', downloaded_content=downloaded_content)

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    file = request.files.get('file')
    if url:
        response = requests.get(url)
        if response.status_code == 200:
            parsed_url = urlparse(url)
            _, extension = os.path.splitext(parsed_url.path)
            extension = extension.lower()
            if not extension or extension == '.html' or extension == '.htm':
                extension = '.txt'
            downloaded_content.append((response.content, extension))
            return redirect(url_for('index', success=True))
        else:
            return redirect(url_for('index', success=False))
    elif file:
        content = file.read()
        extension = mimetypes.guess_extension(file.content_type) or '.txt'
        downloaded_content.append((content, extension))
        return redirect(url_for('index', success=True))
    else:
        return redirect(url_for('index', success=False))

@app.route('/get_content/<int:number>')
def get_content(number):
    try:
        content, extension = downloaded_content[number]
        return send_file(io.BytesIO(content), as_attachment=True, download_name=f"download_{number}{extension}")
    except IndexError:
        return "Content not found"

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=80, debug=True)
    except Exception:
        True # get raped
    finally: # Saves all stored files.
        with open("downloaded_files.txt", "w") as file:
            for item in downloaded_content:
                file.write("%s\n" % item)