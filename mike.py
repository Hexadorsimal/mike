import os
import subprocess
from tempfile import TemporaryDirectory
from flask import Flask, render_template, send_file
from flask_bootstrap import Bootstrap
from submit_form import SubmitForm


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['WTF_CSRF_ENABLED'] = False


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SubmitForm()
    if form.validate_on_submit():
        with TemporaryDirectory() as tempdir:
            output_filename = run_script(tempdir)
            return send_file(output_filename, as_attachment=True)

    return render_template("index.html", form=form)


def run_script(dirname):
    output = subprocess.check_output(["echo", dirname])

    filename = os.path.join(dirname, "echo.txt")
    with open(filename, "wb+") as f:
        f.write(output)

    return filename


if __name__ == '__main__':
    app.run(host="0.0.0.0")
