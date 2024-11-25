from flask import request, jsonify, Blueprint 
from sqlalchemy.sql import text 
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

@employee_bp.route('/employees/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def employee_operations(id):
    try:
        # Handle GET request: Fetch employee details
        if request.method == 'GET':
            employee = Employee.query.get(id)
            if not employee:
                return jsonify({'error': 'Employee not found'}), 404

            return jsonify({
                'id': employee.id,
                'name': employee.name,
                'department': employee.department,
                'designation': employee.designation,
                'salary': employee.salary
            }), 200

        # Handle PUT request: Update employee details
        elif request.method == 'PUT':
            employee = Employee.query.get(id)
            if not employee:
                return jsonify({'error': 'Employee not found'}), 404

            data = request.json
            if not data:
                return jsonify({'error': 'Request payload must be in JSON format'}), 400

            # Update fields if provided
            name = data.get('name')
            department = data.get('department')
            designation = data.get('designation')
            salary = data.get('salary')

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
                'message': 'Employee updated successfully',
                'employee': {
                    'id': employee.id,
                    'name': employee.name,
                    'department': employee.department,
                    'designation': employee.designation,
                    'salary': employee.salary
                }
            }), 200

        # Handle DELETE request: Delete employee
        elif request.method == 'DELETE':
            employee = Employee.query.get(id)
            if not employee:
                return jsonify({'error': 'Employee not found'}), 404

            db.session.delete(employee)
            db.session.commit()

            return jsonify({'message': f'Employee with ID {id} has been deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@employee_bp.route('/employee/dept/<string:department>', methods=['GET'])
def get_employees_by_department(department):
    try:
        # Use text() to explicitly declare the SQL query
        query = text("SELECT id, name, department, designation, salary FROM employee WHERE department = :department")
        result = db.session.execute(query, {'department': department}).fetchall()

        if not result:
            return jsonify({'error': f'No employees found in the {department} department'}), 404

        # Format the response
        employees = [
            {
                'id': row.id,
                'name': row.name,
                'department': row.department,
                'designation': row.designation,
                'salary': row.salary
            }
            for row in result
        ]

        return jsonify({'employees': employees}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

