# DynamoDB NoSQL Design: Single-Table vs. Multiple-Table Approach

NoSQL databases like Amazon DynamoDB are popular for their speed, scalability, and flexibility. However, developers migrating from relational databases often design DynamoDB tables similarly, leading to poor performance and higher costs. 

This article explores two primary design approaches: Single-Table Design and Multiple-Table Design. 

I’ll explain why I strongly prefer the Single-Table Approach, as it optimizes cost and performance by minimizing queries and read/write operations. 

Properly leveraging DynamoDB’s capabilities ensures efficient data modeling, reducing complexity while enhancing scalability and responsiveness. 

Understanding these approaches is key to making the most of DynamoDB’s strengths in real-world applications.

## The NoSQL Mindset: Breaking Free from RDBMS

NoSQL databases like DynamoDB are fundamentally different from relational databases. While RDBMS relies on normalization, joins, and complex relationships, NoSQL databases are designed for scalability, high performance, and flexibility. DynamoDB, in particular, is built to handle massive workloads with low latency, but only if you design your schema with its strengths in mind.

A common mistake developers make is treating DynamoDB like an RDBMS. They create multiple tables, normalize data, and attempt to replicate relational joins using multiple queries. While this approach might feel familiar, it often results in:

- **Increased Costs**: Multiple queries and read/write operations can quickly add up.
- **Reduced Performance**: Joins and multiple queries introduce latency.
- **Complexity**: Managing multiple tables and relationships becomes heavy.

To truly harness the power of DynamoDB, you need to embrace the NoSQL mindset and design your schema around access patterns, not relationships.

## Single-Table Design: The DynamoDB Way

In a **Single-Table Design**, all entities (e.g., organizations, departments, employees, projects) are stored in a single table. This approach leverages DynamoDB’s composite primary keys (partition key + sort key) to model hierarchical relationships and optimize for specific access patterns.

### Advantages of Single-Table Design

1. **Cost-Effective**: Fetching related data requires fewer read/write operations, reducing requests and costs in a pay-per-request model.

2. **High Performance**: Queries are faster since all related data is in one table, eliminating the need for joins or multiple queries.

3. **Scalability**: Single-table design optimizes DynamoDB partitioning and scaling, ensuring seamless performance with growing data and traffic.

4. **Simplified Access Patterns**: By designing the schema around access patterns, you can retrieve all required data in a single query.

5. **Denormalization**: Data is stored in a denormalized format, reducing the need for joins and improving query performance.

### Example Use Case

```json
{
        "organization": {
            "name": "CodexOrg",
            "location": "Bangalore",
            "founded": 1998,
            "departments": [
                {
                    "name": "Engineering",
                    "manager": {
                        "name": "Johnson",
                        "id": 101,
                        "email": "johnson@codexorg.com",
                        "experience": "15 years",
                        "certifications": ["PMP", "AWS Certified Solutions Architect"]
                    },
                    "projects": [
                        {
                            "name": "AI Development",
                            "budget": 500000,
                            "deadline": "2025-12-31",
                            "employees": [
                                {
                                    "id": 201,
                                    "name": "John",
                                    "role": "Software Engineer",
                                    "tasks": [
                                        {"id": 401, "description": "Develop API",
                                            "status": "In Progress"},
                                        {"id": 402, "description": "Write Unit Tests",
                                            "status": "Pending"}
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Marketing",
                    "manager": {
                        "name": "Lee",
                        "id": 103,
                        "email": "lee@codexorg.com",
                        "experience": "10 years",
                        "certifications": ["Google Ads Certified", "HubSpot Inbound Marketing"]
                    }
                }
            ]
        }
    }
```
Consider an organization with departments, projects, employees, and managers. In a single-table design, you can store all these entities in one table, using composite keys to represent relationships.

# Primary Key Design
- **Partition Key (PK):** `OrganizationID` (e.g., `ORG#CodexOrg`)
- **Sort Key (SK):** Composite key to represent the hierarchy (e.g., `DEPT#Engineering`, `PROJ#AI Development`, `EMP#John`, etc.)


# Data Model

| PK                | SK                     | Attributes                                      |
|------------------|----------------------|------------------------------------------------|
| ORG#CodexOrg    | METADATA              | name, location, founded                        |
| ORG#CodexOrg    | DEPT#Engineering      | name, manager (nested object), projects (list of project IDs) |
| ORG#CodexOrg    | DEPT#Marketing        | name, manager (nested object)                  |
| ORG#CodexOrg    | PROJ#AI Development   | name, budget, deadline, employees (list of employee IDs) |
| ORG#CodexOrg    | EMP#John Doe          | id, name, role, tasks (list of tasks)         |
| ORG#CodexOrg    | MGR#Johnson     | id, name, email, experience, certifications    |
| ORG#CodexOrg    | MGR#Lee         | id, name, email, experience, certifications    |

This design allows you to fetch all related data (e.g., all projects in a department) with a single query.

## Access Patterns

### Get Organization Metadata
Query: PK = ORG#CodexOrg AND SK = METADATA

### Get All Departments
Query: PK = ORG#CodexOrg AND SK BEGINS_WITH DEPT#

### Get a Specific Department (e.g., Engineering)
Query: PK = ORG#CodexOrg AND SK = DEPT#Engineering

### Get All Projects in a Department
Query: PK = ORG#CodexOrg AND SK BEGINS_WITH PROJ#

### Get All Employees in a Project
Query: PK = ORG#CodexOrg AND SK BEGINS_WITH EMP#

### Get Manager Details
Query: PK = ORG#CodexOrg AND SK BEGINS_WITH MGR#

## Multiple-Table Design: The RDBMS Hangover

In a **Multiple-Table Design**, each entity is stored in a separate table, similar to a relational database. For example:
- `OrganizationTable`
- `DepartmentTable`
- `ProjectTable`
- `EmployeeTable`

### Disadvantages of Multiple-Table Design

1. **Increased Costs**: Fetching related data requires multiple queries, leading to higher read/write costs as each query consumes capacity units.

2. **Reduced Performance**: DynamoDB does not support joins, requiring multiple queries and application-side data joining, which adds latency and complexity.

3. **Complexity**: Managing multiple tables and relationships in DynamoDB is challenging, requiring additional application logic for joins and data handling.

4. **Inefficient for Hierarchical Data**: Fetching hierarchical data (e.g., all employees in a project) requires multiple queries, which is inefficient.

### Example Use Case
Using the same organization example, you would need to:
1. Query the `DepartmentTable` to get department details.
2. Query the `ProjectTable` to get projects in the department.
3. Query the `EmployeeTable` to get employees in each project.

This approach is not only inefficient but also costly and slow.

## Why I Prefer Single-Table Design

My preference for the **Single-Table Design** is driven by two key factors: **cost** and **performance**.

1. **Cost**:
   - DynamoDB charges based on read/write capacity units. With a single-table design, you minimize the number of operations required to fetch data, reducing costs significantly.
   - Multiple-table designs often require additional queries, which increase costs.

2. **Performance**:
   - Single-table design allows you to fetch all related data in a single query, resulting in faster response times.
   - Multiple-table designs require multiple queries and application-level joins, which introduce latency.



## When to Use Multiple-Table Design
While I advocate for single-table design, there are scenarios where a multiple-table design might make sense:
- **Ad-Hoc Queries**: If your access patterns are unpredictable or frequently changing, multiple tables might offer more flexibility.
- **Data Isolation**: If you need strict isolation between entities (e.g., for security or compliance reasons), multiple tables can help.
- **Legacy Systems**: If you’re migrating from an RDBMS and want to maintain a similar structure, multiple tables might be easier to implement initially.



## Conclusion

Unlock DynamoDB potential by embracing single-table design, optimizing for access patterns, and shifting from a relational mindset to build scalable, cost-effective, and high-performance applications.