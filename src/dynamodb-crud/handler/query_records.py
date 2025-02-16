import boto3
from botocore.exceptions import ClientError
from .utils import convert_decimal
import os
# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))


def get_organization_metadata(org_id):
    """Get Organization Metadata: PK = ORG#CodexCorp AND SK = METADATA"""
    response = table.get_item(
        Key={
            "PK": org_id,
            "SK": "METADATA"
        }
    )
    return convert_decimal(response.get('Item', {}))


def get_all_departments(org_id):
    """Get All Departments: PK = ORG#CodexCorp AND SK BEGINS_WITH DEPT#"""
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": org_id,
            ":sk": "DEPT#"
        }
    )
    return [convert_decimal(item) for item in response.get('Items', [])]


def get_department(org_id, dept_name):
    """Get a Specific Department: PK = ORG#CodexCorp AND SK = DEPT#Engineering"""
    response = table.get_item(
        Key={
            "PK": org_id,
            "SK": f"DEPT#{dept_name}"
        }
    )
    return convert_decimal(response.get('Item', {}))


def get_all_projects(org_id):
    """Get All Projects: PK = ORG#CodexCorp AND SK BEGINS_WITH PROJ#"""
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": org_id,
            ":sk": "PROJ#"
        }
    )
    return [convert_decimal(item) for item in response.get('Items', [])]


def get_all_employees(org_id):
    """Get All Employees: PK = ORG#CodexCorp AND SK BEGINS_WITH EMP#"""
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": org_id,
            ":sk": "EMP#"
        }
    )
    return [convert_decimal(item) for item in response.get('Items', [])]


def get_all_managers(org_id):
    """Get Manager Details: PK = ORG#CodexCorp AND SK BEGINS_WITH MGR#"""
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": org_id,
            ":sk": "MGR#"
        }
    )
    return [convert_decimal(item) for item in response.get('Items', [])]
