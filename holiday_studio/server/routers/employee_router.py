from flask import Blueprint, request, Response
from models import AlchemyEncoder, Order, EmployeeOrder
from models import Employee, create_session
import json

from flask_login import login_required, current_user

router = Blueprint("employee_api",
                   __name__,
                   template_folder="/server/templates",
                   url_prefix="/employee")


@router.get("/<int:employee_id>/order/<int:order_id>")
def add_order(employee_id, order_id):
    status = 200
    session = create_session()
    employee = session.query(Employee).get(
        employee_id)  # аналогично session.query(Employee).where(Employee.id == employee_id).first()
    if not employee:
        status = 404
        result = json.dumps({"error": f"Employee with id {employee_id} not found"})
        session.close()
        return Response(result, status=status, mimetype="application/json")
    order = session.query(Order).get(order_id)
    if not order:
        status = 404
        result = json.dumps({"error": f"Order with id {order_id} not found"})
        session.close()
        return Response(result, status=status, mimetype="application/json")
    employee_order = session.query(EmployeeOrder). \
        where(EmployeeOrder.id_employee == employee_id,
              EmployeeOrder.id_order == order_id).first()
    if employee_order:
        status = 208
        result = json.dumps(
            {"detail (dangerous!!)": f"Employee with id {employee_id} and Order with id {order_id} is bounded"})
        session.close()
        return Response(result, status=status, mimetype="application/json")
    employee_order = EmployeeOrder(id_employee=employee_id,
                                   id_order=order_id)
    session.add(employee_order)
    session.commit()
    return "ok"


@router.get("/<int:employee_id>/orders")
def get_orders(employee_id):
    status = 200
    session = create_session()
    employee = session.query(Employee).get(
        employee_id)
    if not employee:
        status = 404
        result = json.dumps({"error": f"Employee with id {employee_id} not found"})
        session.close()
        return Response(result, status=status, mimetype="application/json")
    employee_orders = session.query(EmployeeOrder). \
        where(EmployeeOrder.id_employee == employee_id).all()
    orders = list(map(lambda x: x.order, employee_orders))
    result = json.dumps(orders, cls=AlchemyEncoder, ensure_ascii=False)
    session.close()
    return Response(result, mimetype="application/json")


@router.route("/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    status = 200
    session = create_session()
    employee = session.query(Employee).get(employee_id)
    if employee:
        result = json.dumps(employee, cls=AlchemyEncoder, ensure_ascii=False)
    else:
        status = 404
        result = json.dumps(None)
    session.close()
    return Response(result, status=status, mimetype="application/json")


@router.route("/", methods=["GET"])
def get_employees():
    session = create_session()
    employees = session.query(Employee).all()
    result = json.dumps(employees, cls=AlchemyEncoder, ensure_ascii=False)
    session.close()
    return Response(result, mimetype="application/json")


@router.route("/", methods=["POST"])
def create_employee():
    session = create_session()
    json_data = request.json
    for key, value in json_data.items():
        try:
            getattr(Employee, key)
        except AttributeError:
            status = 400
            session.close()
            return Response(json.dumps({"error": f"{key} filed not found"}), status=status, mimetype="application/json")
    new_employee = Employee(**json_data)
    new_employee.set_password(json_data["password"])
    session.add(new_employee)
    session.commit()
    result = json.dumps(new_employee, cls=AlchemyEncoder, ensure_ascii=False)
    session.close()
    return result


@router.route("/<int:employee_id>", methods=["PUT"])
def put_employee(employee_id):
    session = create_session()
    employee = session.query(Employee).get(
        employee_id)  # аналогично session.query(Employee).where(Employee.id == employee_id)
    if employee:
        json_data = request.json  # пример: {"fullname": "Роман", login: "grm"} - означает, что нужно изменить только 2 поля. Как распарсить?

        for key, value in json_data.items():
            try:
                getattr(Employee, key)
            except AttributeError:
                status = 400
                session.close()
                return Response(json.dumps({"error": f"{key} filed not found"}), status=status,
                                mimetype="application/json")
            setattr(employee, key, value)  # задаем в employee полю key значение value
        session.commit()
        result = json.dumps(employee, cls=AlchemyEncoder, ensure_ascii=False)
    else:
        result = json.dumps(None)
    session.close()
    return result


@router.delete("/<int:employee_id>")
def delete_employee(employee_id):
    status = 200
    session = create_session()
    employee = session.query(Employee).get(
        employee_id)  # аналогично session.query(Employee).where(Employee.id == employee_id)
    if employee:
        session.delete(employee)
        session.commit()
        result = json.dumps(True)
    else:
        status = 404
        result = json.dumps(False)
    session.close()
    return Response(result, status=status, mimetype="application/json")
