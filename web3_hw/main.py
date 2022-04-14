from flask import Flask, render_template, url_for
import os

app = Flask(__name__)


@app.route("/carousel", methods=['GET'])
def carousel():
    return render_template("carousel.html", images=list(map(lambda x: url_for('static', filename=x),
                                                        map(lambda name: "img/" + name,
                                                            os.listdir("C:/PyQt/WEB_HW/web3_hw/static/img/")))))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')