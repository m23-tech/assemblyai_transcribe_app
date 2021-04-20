# views.py

import os
import requests
import json
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, flash
from werkzeug.utils import secure_filename

from app import app


@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template("upload.html", files=files)


@app.errorhandler(400)
def invalid_file_type(e):
    return render_template('/error_pages/400.html'), 400


@app.errorhandler(404)
def invalid_file_type(e):
    return render_template('/error_pages/404.html'), 404


@app.errorhandler(413)
def invalid_file_type(e):
    return render_template('/error_pages/413.html'), 413


@app.errorhandler(500)
def invalid_file_type(e):
    return render_template('/error_pages/500.html'), 500


def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


@app.route('/', methods=['POST'])
def upload_files():
    if request.form['submit'] == "Submit":
        # Obtain the Files
        uploaded_file = request.files['fileupload']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                flash('Allowed file types are mp3, mp4, acc and flac')
                return redirect(request.url)
            else:
                # Upload to local storage
                uploaded_file.save(os.path.join(
                    app.config['UPLOAD_PATH'], filename))

                # Upload the audio file to AssemblyAI
                upload_response = requests.post('https://api.assemblyai.com/v2/upload',
                                                headers=app.config['ASSEMBLYAI'],
                                                data=read_file(os.path.join(app.config['UPLOAD_PATH'], filename)))

                file_name_only = os.path.splitext(filename)[0]
                assembly_ai_path = app.config['TRANSCRIBE_PATH'] + \
                    "\\" + file_name_only + ".json"
                with open(assembly_ai_path, 'w') as outfile:
                    json.dump(upload_response.json(), outfile)

                # Transcribe the Uploaded audio file
                endpoint = "https://api.assemblyai.com/v2/transcript"
                audio_upload_url = upload_response.json()

                json_string = {"audio_url": audio_upload_url['upload_url']}
                transcript_response = requests.post(endpoint,
                                                    headers=app.config['ASSEMBLYAI'],
                                                    json=json_string)

                file_name_only = os.path.splitext(filename)[0]
                assembly_ai_transcription_path = app.config['TRANSCRIBE_PATH'] + \
                    "\\" + file_name_only + "_transcription.json"
                with open(assembly_ai_transcription_path, 'w') as outfile:
                    json.dump(transcript_response.json(), outfile)

                return redirect(url_for('upload_files', filename=filename))


@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    if request.form['delete'] == "DELETE":
        os.remove(os.path.join(app.config['UPLOAD_PATH'], filename))
        file_name_only = os.path.splitext(filename)[0]
        assembly_ai_path = app.config['TRANSCRIBE_PATH'] + \
            "\\" + file_name_only + ".json"
        os.remove(assembly_ai_path)
        assembly_ai_transcription_path = app.config['TRANSCRIBE_PATH'] + \
            "\\" + file_name_only + "_transcription.json"
        os.remove(assembly_ai_transcription_path)
        return redirect(url_for('index'))


@app.route('/audio/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/transcribe/<filename>',  methods=['POST'])
def transcribe(filename):
    if request.form['getResult'] == "RESULT":
        file_name_only = os.path.splitext(filename)[0]
        assembly_ai_transcription_path = app.config['TRANSCRIBE_PATH'] + \
            "\\" + file_name_only + "_transcription.json"
        with open(assembly_ai_transcription_path, 'r') as openfile:
            data = json.load(openfile)
            transcript_id = data['id']

            endpoint = "https://api.assemblyai.com/v2/transcript/" + transcript_id
            response = requests.get(endpoint, headers=app.config['ASSEMBLYAI'])

            result = response.json()
            if result['status'] == 'completed':
                text_result = result['text']
                return render_template('result.html', data=text_result, filename=file_name_only)
            elif result['status'] == 'queued' or result['status'] == 'processing':
                text_result = "Still Processing Please Try Again Later"
                return render_template('result.html', data=text_result, filename=file_name_only)
            elif result['status'] == 'error':
                error = "Delete the File and Try Again"
                return render_template('result.html', data=text_result, filename=file_name_only)


@app.route('/about')
def about():
    return render_template("about.html")
