from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/cabin/<gender>/<age>")
def func(gender, age):
    if "female" in gender.lower():
        if int(age) >= 21:
            return render_template("params.html",
                                   cabin="Оформление каюты",
                                   way_to_img_1=url_for("static",
                                                         filename="img/room_o_f.jpg"),
                                   way_to_img_2=url_for("static",
                                                           filename="img/old_female.jpg"))
        else:
            return render_template("params.html",
                                   cabin="Оформление каюты",
                                   way_to_img_1=url_for("static",
                                                         filename="img/room_b_f.jpg"),
                                   way_to_img_2=url_for("static",
                                                           filename="img/baby_female.png"))
    if "male" in gender.lower():
        if int(age) >= 21:
            return render_template("params.html",
                                   cabin="Оформление каюты",
                                   way_to_img_1=url_for("static",
                                                         filename="room_o_m.jpg"),
                                   way_to_img_2=url_for("static",
                                                           filename="img/old_male.jpg"))
        else:
            return render_template("params.html",
                                   cabin="Оформление каюты",
                                   way_to_img_1=url_for("static",
                                                         filename="img/room_b_m.jpg"),
                                   way_to_img_2=url_for("static",
                                                           filename="img/baby_male.jpg"))


if __name__ == '__main__':
    app.run(port=8088, host='127.0.0.1')
