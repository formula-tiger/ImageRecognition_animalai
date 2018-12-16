"""
http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
Flaskの公式ドキュメント保存
"""

import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename  # WSGIの不便さをカバーしてくれているツールセット



UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):  # 2つのチェックをしてファイルのアップロードの可否判定関数
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        # ファイル名に . が含まれているか。　ファイル名のピリオド以降のところに 指定の拡張子が含まれているか

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 未知のユーザーによるハッキング防止 / => _ に変更するなど
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))  # Flaskの url_forメソッドはファイル名を引数に取り、 そのURLを生成する
    return '''
    <!doctype html>
    <html>
    <head>
    <meta charset = "UTF-8">
    <title>ファイルをアップロードして判定しよう</title></head>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    </body>
    </html>
    
    '''

from flask import send_from_directory

@app.route('/uploads/<filename>')
# アップロードされたファイルを返す関数
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)  # arg1 に指定したディレクトリ名から arg2に指定したファイルを送信