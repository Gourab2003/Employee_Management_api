from flask import request, jsonify, Blueprint 
from models import Employee, db


employee_bp =  Blueprint('employees',__name__)

@employee_bp.route('/employees', methods=['GET'])
def get_employees():
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


@employee_bp.route('/employees', methods=['POST'])
def add_employees():
    try:
        # Parse JSON payload
        data = request.json
        if not data:
            return jsonify({'error': 'Request payload must be in JSON format'}), 400

        # Extract and validate fields
        name = data.get('name')
        department = data.get('department')
        designation = data.get('designation')
        salary = data.get('salary')

        # Validate all fields
        missing_fields = []
        if not name:
            missing_fields.append('name')
        if not department:
            missing_fields.append('department')
        if not designation:
            missing_fields.append('designation')
        if salary is None:  # Explicit check for None (to allow 0.0 as valid)
            missing_fields.append('salary')

        if missing_fields:
            return jsonify({'error': f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Create and add new employee
        new_employee = Employee(name=name, department=department, designation=designation, salary=salary)
        db.session.add(new_employee)
        db.session.commit()

        # Successful response
        return jsonify({
            'message': 'Employee added successfully',
            'employee': {
                'id': new_employee.id,
                'name': new_employee.name,
                'department': new_employee.department,
                'designation': new_employee.designation,
                'salary': new_employee.salary
            }
        }), 201

    except Exception as e:
        print(f"Error occurred: {e}")  # Optional logging
        return jsonify({'error': 'An unexpected error occurred'}), 500

