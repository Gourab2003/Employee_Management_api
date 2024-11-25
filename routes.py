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
        if salary is None: 
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

@employee_bp.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    try:
        employee = Employee.query.get(id)
        
        if not employee:
            return jsonify({'error':'Employee not found'}), 404
        
        data = request.json
        name = data.get('name')
        department = data.get('department')
        designation = data.get('designation')
        salary = data.get('salary')
        
        if not any([name, department, designation, salary]):
            return jsonify({'error':'at least one field'})
        
        if name:
            employee.name = name
        if department:
            employee.department = department
        if designation:
            employee.designation = designation
        if salary is not None:
            employee.salary = salary
            
        db.session.commit()
        
        return jsonify({
            'message': 'Employee update successfully',
            'Employee':{
                'id': employee.id,
                'name': employee.name,
                'department': employee.department,
                'designation': employee.designation,
                'salary': employee.salary
            }
        }), 200
    except Exception as e:
        return jsonify({'error':str(e)}), 500
    
    
