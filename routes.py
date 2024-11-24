from flask import request, jsonify, Blueprint
from app import app
from models import Employee


employee_bp = Blueprint('blueprint',__name__)

# Example route to fetch all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([{
        "id": emp.id,
        "name": emp.name,
        "department": emp.department,
        "designation": emp.designation,
        "salary": emp.salary
    } for emp in employees])
