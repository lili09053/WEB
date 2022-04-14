from flask import Flask, render_template

app = Flask(__name__)


@app.route("/results/<name>/<level>/<rating>")
def func(name, level, rating):
    return render_template("res.html", name=name, level=level, rating=rating)


if __name__ == '__main__':
    app.run(port=8084, host='127.0.0.1')