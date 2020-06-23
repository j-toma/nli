from flask import Flask, render_template, request, request, url_for, flash, send_from_directory
import sys
sys.path.append("/home/jtoma/nli")

from single import run_display, display_upload, display_text

UPLOAD_FOLDER = '/home/jtoma/nli/static'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        #if 'file' not in request.files:
        #    flash('No file part')
        #    return redirect(request.url)
        if 'file' in request.files:
            f = request.files['file']
            if f.filename == '':
                flash('no selected file')
                return redirect(request.url)
            if f and allowed_file(f.filename):
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('pred_up'))
        if 'doc' in request.form:
            #doc = request.form['doc']
            return redirect(url_for('pred_paste'))

    return render_template('index.html')

@app.route('/pred_up', methods=['GET','POST'])
def pred_up():
    up_content = request.files['doc']
    pred, prob, mkdn = display_text(up_content)
    data = [pred[0],prob, mkdn]
    return render_template('prediction.html', data=data)

@app.route('/pred_paste', methods=['GET','POST'])
def pred_paste():
    paste_content =  request.form['paste']
    pred, prob, mkdn = display_text(paste_content)
    data = [pred[0],prob, mkdn]
    return render_template('prediction.html', data=data)

@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s.html' % page_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


