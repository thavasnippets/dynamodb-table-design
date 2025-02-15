import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
import os

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))


def insert_sample_data(data):
    org = data['organization']
    org_id = f"ORG#{org['name']}"

    # Insert organization metadata
    table.put_item(Item={
        "PK": org_id,
        "SK": "METADATA",
        "name": org['name'],
        "location": org['location'],
        "founded": org['founded']
    })

    # Insert departments
    for dept in org['departments']:
        dept_id = f"DEPT#{dept['name']}"
        table.put_item(Item={
            "PK": org_id,
            "SK": dept_id,
            "name": dept['name'],
            "manager": dept['manager'],
            "projects": [f"PROJ#{proj['name']}" for proj in dept.get('projects', [])]
        })

        # Insert manager
        manager = dept['manager']
        table.put_item(Item={
            "PK": org_id,
            "SK": f"MGR#{manager['name']}",
            "id": manager['id'],
            "name": manager['name'],
            "email": manager['email'],
            "experience": manager['experience'],
            "certifications": manager['certifications']
        })

        # Insert projects
        for proj in dept.get('projects', []):
            proj_id = f"PROJ#{proj['name']}"
            table.put_item(Item={
                "PK": org_id,
                "SK": proj_id,
                "name": proj['name'],
                "budget": proj['budget'],
                "deadline": proj['deadline'],
                "employees": [f"EMP#{emp['name']}" for emp in proj.get('employees', [])]
            })

            # Insert employees
            for emp in proj.get('employees', []):
                emp_id = f"EMP#{emp['name']}"
                table.put_item(Item={
                    "PK": org_id,
                    "SK": emp_id,
                    "id": emp['id'],
                    "name": emp['name'],
                    "role": emp['role'],
                    "tasks": emp.get('tasks', [])
                })
