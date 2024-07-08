from flask import Flask, request, render_template, jsonify, send_file, Response
import os
import io

app = Flask(__name__)

# In-memory storage for uploaded chunks
uploaded_chunks = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    chunk = request.files['chunk']
    original_filename = request.form['originalFilename']
    chunk_number = int(request.form['chunkNumber'])

    # Store the chunk in the in-memory dictionary
    if original_filename not in uploaded_chunks:
        uploaded_chunks[original_filename] = []
    
    uploaded_chunks[original_filename].append((chunk_number, chunk.read()))

    return 'Chunk uploaded successfully', 200

@app.route('/uploaded_files')
def uploaded_files():
    files = list(uploaded_chunks.keys())
    return jsonify(files)

@app.route('/download/<filename>')
def download(filename):
    if filename not in uploaded_chunks:
        return 'File not found', 404

    # Sort chunks by chunk number and combine them
    chunks = sorted(uploaded_chunks[filename], key=lambda x: x[0])
    combined_file = io.BytesIO()
    for _, chunk_data in chunks:
        combined_file.write(chunk_data)
    combined_file.seek(0)

    # Clear the stored chunks from memory after serving the file
    #del uploaded_chunks[filename]

    return send_file(combined_file, as_attachment=True, download_name=f"{filename}")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
