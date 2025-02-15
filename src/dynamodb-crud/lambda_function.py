import json
from handler.insert_record import insert_sample_data
from handler.query_records import get_all_departments, get_all_managers, get_department, get_all_projects, get_organization_metadata, get_all_employees
from botocore.exceptions import ClientError
from sampledata import data
from handler.utils import convert_decimal


def lambda_handler(event, context):
    try:

        insert_sample_data(data=data)

        # Example usage of query methods
        org_id = "ORG#CodexOrg"

        # Get Organization Metadata
        org_metadata = get_organization_metadata(org_id)
        print("Organization Metadata:", org_metadata)

        # Get All Departments
        departments = get_all_departments(org_id)
        print("All Departments:", departments)

        # Get a Specific Department (e.g., Engineering)
        dept_name = "Engineering"
        department = get_department(org_id, dept_name)
        print(f"Department '{dept_name}':", department)

        # Get All Projects in a Department
        projects = get_all_projects(org_id)
        print("All Projects:", projects)

        # Get All Employees in a Project
        employees = get_all_employees(org_id)
        print("All Employees:", employees)

        # Get Manager Details
        managers = get_all_managers(org_id)
        print("All Managers:", managers)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'organization_metadata': org_metadata,
                'departments': departments,
                'department': department,
                'projects': projects,
                'employees': employees,
                'managers': managers
            }, indent=2, default=convert_decimal)
        }
    except ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error querying data from DynamoDB')
        }
