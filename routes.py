from flask import request, jsonify, Blueprint 

employee_bp =  Blueprint('employees',__name__)

@employee_bp.route('/employees', methods=['GET'])
def get_employees():
    from models import Employee
    employees = Employee.query.all()
    employee_list = [
        {
            "id": emp.id,
            "name": emp.name,
            "department": emp.department,
            "designation": emp.designation,
            "salary": emp.salary
        }
        for emp in employees
    ]
    return jsonify(employee_list), 200