import requests
import sqlalchemy
from flask import Blueprint, request, render_template, redirect
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from wtforms_sqlalchemy.fields import QuerySelectField

from forms.create_client import CreateClientForm
from forms.create_order import CreateOrderForm
from forms.login import LoginForm
from forms.put_client import PutClient
from forms.put_order import PutOrder
from forms.delete_client import DeleteClient
from forms.delete_order import DeleteOrder
from models import AlchemyEncoder, Employee, Client, EmployeeOrder, ClientOrder
from models import Order, create_session
import json

# from flask_login import current_user

router = Blueprint("",
                   __name__,
                   template_folder="/server/templates")


@router.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        session = create_session()
        employee = session.query(Employee). \
            filter(Employee.email == login_form.email.data).first()
        if employee and employee.check_password(login_form.password.data):
            login_user(employee)
            session.close()
            return redirect("/")
        else:
            session.close()
            return redirect("/site/login")
    return render_template("login.html", title="Авторизация", form=login_form)


@router.route("/all_clients", methods=["GET", "POST"])
@login_required
def all_clients():
    session = create_session()
    clients = session.query(Client).all()
    result = json.dumps(clients, cls=AlchemyEncoder, ensure_ascii=False)
    session.close()
    return render_template("all_clients.html", clients=json.loads(result))


@router.route("/create_client", methods=["GET", "POST"])
@login_required
def create_client():
    create_client_form = CreateClientForm()
    if create_client_form.validate_on_submit():
        session = create_session()
        client = Client(full_name=create_client_form.full_name.data,
                        age=create_client_form.age.data,
                        phone=create_client_form.phone.data,
                        email=create_client_form.email.data)
        session.add(client)
        try:
            session.commit()
            session.close()
            return redirect("/")
        except IntegrityError:
            create_client_form.email.errors.append("Email уже используется")
            session.close()
            return render_template("create_client.html", title="Создание клиента", form=create_client_form)

    return render_template("create_client.html", title="Создание клиента", form=create_client_form)


@router.route("/put_client", methods=["GET", "POST"])
@login_required
def put_client():
    put_client_form = PutClient()
    session = create_session()
    if put_client_form.validate_on_submit():
        cr = json.loads(json.dumps(put_client_form.client_list.data, cls=AlchemyEncoder, ensure_ascii=False))
        client = session.query(Client).get(cr["id"])
        if client:
            json_data = Client(full_name=put_client_form.full_name.data,
                               age=put_client_form.age.data,
                               phone=put_client_form.phone.data,
                               email=put_client_form.email.data)
            json_data = json.loads(json.dumps(json_data, cls=AlchemyEncoder, ensure_ascii=False))
            for key, value in json_data.items():
                if value is not None:
                    setattr(client, key, value)
            session.commit()
        session.close()
        return redirect("/")
    return render_template("put_client.html", form=put_client_form)


@router.route("/delete_client", methods=["POST", "GET"])
@login_required
def delete_client():
    delete_client_form = DeleteClient()
    session = create_session()
    if delete_client_form.validate_on_submit():
        client = delete_client_form.client_list.data
        client_to_delete = session.query(Client).get(client.id)
        if client_to_delete:
            session.delete(client_to_delete)
            session.commit()
        clients_orders = session.query(ClientOrder).all()
        clients_orders = json.loads(json.dumps(clients_orders, cls=AlchemyEncoder, ensure_ascii=False))
        client_order_ids = []
        for elem in clients_orders:
            if elem["id_client"] == client.id:
                client_order_ids.append(elem["id"])
        if client_order_ids:
            for id in client_order_ids:
                client_order_to_delete = session.query(ClientOrder).get(id)
                session.delete(client_order_to_delete)
                session.commit()
        session.close()
        return redirect("/")
    return render_template("delete_client.html", form=delete_client_form)


@router.route("/create_order", methods=["GET", "POST"])
@login_required
def create_order():
    create_order_form = CreateOrderForm()
    if create_order_form.validate_on_submit():
        client = create_order_form.client_list.data
        session = create_session()
        order = Order(price=create_order_form.price.data,
                      title=create_order_form.title.data,
                      describtion=create_order_form.describtion.data)
        session.add(order)
        session.commit()

        employee_order = EmployeeOrder(id_employee=current_user.id,
                                       id_order=order.id)
        client_order = ClientOrder(id_client=client.id,
                                   id_order=order.id)

        session.add(client_order)
        session.add(employee_order)
        session.commit()
        session.close()
        return redirect("/")
    return render_template("create_order.html", title="Создание заказа", form=create_order_form)


@router.route("/all_orders", methods=["GET"])
@login_required
def all_orders():
    session = create_session()
    orders = session.query(EmployeeOrder).all()
    result = json.dumps(orders, cls=AlchemyEncoder, ensure_ascii=False)
    lst = []
    for item in json.loads(result):
        if item["id_employee"] == current_user.id:
            lst.append(item["id_order"])
    my_orders = []
    for i in lst:
        my_order = session.query(Order).get(i)
        result_1 = json.dumps(my_order, cls=AlchemyEncoder, ensure_ascii=False)
        my_orders.append(json.loads(result_1))
    session.close()
    return render_template("all_orders.html", my_orders=my_orders)


@router.route("/put_order", methods=["GET", "POST"])
@login_required
def put_order():
    put_order_form = PutOrder()
    session = create_session()
    if put_order_form.validate_on_submit():
        cr = json.loads(json.dumps(put_order_form.order_list.data, cls=AlchemyEncoder, ensure_ascii=False))
        order = session.query(Order).get(cr["id"])
        if order:
            json_data = Order(price=put_order_form.price.data,
                              title=put_order_form.title.data,
                              describtion=put_order_form.describtion.data)
            json_data = json.loads(json.dumps(json_data, cls=AlchemyEncoder, ensure_ascii=False))
            for key, value in json_data.items():
                if value is not None:
                    setattr(order, key, value)
            session.commit()
        session.close()
        return redirect("/")
    return render_template("put_order.html", form=put_order_form)


@router.route("/delete_order", methods=["POST", "GET"])
@login_required
def delete_order():
    delete_order_form = DeleteOrder()
    session = create_session()
    if delete_order_form.validate_on_submit():
        order = delete_order_form.order_list.data
        order_to_delete = session.query(Order).get(order.id)
        if order_to_delete:
            session.delete(order_to_delete)
            session.commit()
        clients_orders = session.query(ClientOrder).all()
        clients_orders = json.loads(json.dumps(clients_orders, cls=AlchemyEncoder, ensure_ascii=False))
        employee_orders = session.query(EmployeeOrder).all()
        employee_orders = json.loads(json.dumps(employee_orders, cls=AlchemyEncoder, ensure_ascii=False))
        client_order_ids = []
        employee_order_ids = []
        for elem in clients_orders:
            if elem["id_order"] == order.id:
                client_order_ids.append(elem["id"])
        for elem in employee_orders:
            if elem["id_order"] == order.id:
                employee_order_ids.append(elem["id"])
        for id in client_order_ids:
            client_order_to_delete = session.query(ClientOrder).get(id)
            session.delete(client_order_to_delete)
            session.commit()
        for id in employee_order_ids:
            employee_order_to_delete = session.query(EmployeeOrder).get(id)
            session.delete(employee_order_to_delete)
            session.commit()
        session.close()
        return redirect("/")
    return render_template("delete_order.html", form=delete_order_form)


@router.route("/logout")
def logout():
    logout_user()
    return redirect("/")
