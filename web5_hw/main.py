from flask import Flask, render_template, url_for, redirect
import os
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField


class LoadImageForm(FlaskForm):
    file = FileField()
    submit = SubmitField('n')


load_dotenv()


app = Flask(__name__)


app.config["SECRET_KEY"] = "1234"


@app.route("/gallery", methods=['GET', 'POST'])
def func():
    form = LoadImageForm()
    if form.validate_on_submit():
        raw_data = form.file.data
        with open(f"./static/img/mem{len(os.listdir('./static/img/')) + 1}.jpg", "wb") as out_file:
            out_file.write(raw_data.read())
        return redirect("gallery")
    return render_template("appender.html", images=list(map(lambda i: url_for('static', filename=i),
                                                        map(lambda j: "img/" + j,
                                                            os.listdir("./static/img/")))), form=form)


if __name__ == '__main__':
    app.run(port=8090, host='127.0.0.1')