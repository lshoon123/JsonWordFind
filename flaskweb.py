from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug import secure_filename
from Jjson import *
import os
import datetime

Upload_Folder = './stored'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Upload_Folder


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/')
def main() -> 'html':
    return render_template('main.html')


@app.route('/upload', methods=['POST'])
def upload() -> 'html':
    Uploadtime = datetime.datetime.now()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            n = os.path.getsize(filename) / 1024.0
            n = round(n, 3)

            if c.find_one():
                for x in c.find():
                    if filename == x["FileName"]:
                        if n == x["DataSize"]:
                            arr = c.find_one({'FileName': filename})
                            count = 0
                            return render_template('result.html', DATA=arr["DATA"], DATE=arr["DATE"], FILENAME=arr["FileName"], size=arr["DataSize"])
                    else:
                        count = 1
                if(count == 1):
                    insert(filename, n, Uploadtime)
                    for x in c.find():
                        print(x["FileName"])
                        arr = c.find_one({'FileName': filename})
                    return render_template('result.html', DATA=arr["DATA"], DATE=arr["DATE"], FILENAME=arr["FileName"],
                                       size=arr["DataSize"])
            else:
                insert(filename, n, Uploadtime)
                for x in c.find():
                    print(x["FileName"])
                arr = c.find_one({'FileName': filename})
                return render_template('result.html', DATA=arr["DATA"], DATE=arr["DATE"], FILENAME=arr["FileName"], size=arr["DataSize"])
        return render_template('main.html')

@app.route('/history', methods=['POST'])
def history()->'html':
    ar = []
    for x in c.find():
        ar.append(x["FileName"])
    print(ar)
    arra = {}
    for x in ar:
        arra[x] = c.find_one({'FileName': x})
    for x in arra:
        print(arra[x]["DATE"])
    return render_template('history.html', NAMEARRAY=ar, DATAARRAY=arra)


@app.route('/result2/<filename>', methods=['GET'])
def result2(filename)->'html':
    arr = c.find_one({'FileName': filename})
    return render_template('result.html', DATA=arr["DATA"], DATE=arr["DATE"], FILENAME=arr["FileName"],
                           size=arr["DataSize"])


def insert(filename, n, Uploadtime):
    wordData = openfile(Upload_Folder, filename)
    print(wordData)

    post = {"FileName": filename, "DataSize": n, "DATE": Uploadtime,
            "DATA": wordData}
    db.word.insert(post, check_keys=False)













app.secret_key = 'thisismysecretsecretsecretkey'

if __name__ == '__main__':
    app.run(debug=True)
