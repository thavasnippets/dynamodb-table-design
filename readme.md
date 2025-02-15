# DynamoDB NoSQL Design: Single-Table vs. Multiple-Table Approach

NoSQL databases like Amazon DynamoDB have become very popular in recent years because they are fast, scalable, and flexible. However, many developers who switch from traditional relational databases (RDBMS) make the mistake of designing DynamoDB tables the same way they would in a relational database. This can result in poor performance, higher costs, and not fully using DynamoDB’s capabilities.

In this article, I want to discuss the two primary approaches to DynamoDB design: **Single-Table Design** and **Multiple-Table Design**. I’ll also explain why my preference leans heavily toward the **Single-Table Approach**, primarily due to its cost-effectiveness and performance benefits.

---

## The NoSQL Mindset: Breaking Free from RDBMS

NoSQL databases like DynamoDB are fundamentally different from relational databases. While RDBMS relies on normalization, joins, and complex relationships, NoSQL databases are designed for scalability, high performance, and flexibility. DynamoDB, in particular, is built to handle massive workloads with low latency, but only if you design your schema with its strengths in mind.

A common mistake developers make is treating DynamoDB like an RDBMS. They create multiple tables, normalize data, and attempt to replicate relational joins using multiple queries. While this approach might feel familiar, it often results in:

- **Increased Costs**: Multiple queries and read/write operations can quickly add up.
- **Reduced Performance**: Joins and multiple queries introduce latency.
- **Complexity**: Managing multiple tables and relationships becomes cumbersome.

To truly harness the power of DynamoDB, you need to embrace the NoSQL mindset and design your schema around access patterns, not relationships.

---

## Single-Table Design: The DynamoDB Way

In a **Single-Table Design**, all entities (e.g., organizations, departments, employees, projects) are stored in a single table. This approach leverages DynamoDB’s composite primary keys (partition key + sort key) to model hierarchical relationships and optimize for specific access patterns.

### Advantages of Single-Table Design

1. **Cost-Effective**: Fetching related data requires fewer read/write operations, reducing requests and costs in a pay-per-request model.

2. **High Performance**: Queries are faster since all related data is in one table, eliminating the need for joins or multiple queries.

3. **Scalability**: Single-table design optimizes DynamoDB’s partitioning and scaling, ensuring seamless performance with growing data and traffic.

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
| ORG#TechCorp    | METADATA              | name, location, founded                        |
| ORG#TechCorp    | DEPT#Engineering      | name, manager (nested object), projects (list of project IDs) |
| ORG#TechCorp    | DEPT#Marketing        | name, manager (nested object)                  |
| ORG#TechCorp    | PROJ#AI Development   | name, budget, deadline, employees (list of employee IDs) |
| ORG#TechCorp    | EMP#John Doe          | id, name, role, tasks (list of tasks)         |
| ORG#TechCorp    | MGR#Johnson     | id, name, email, experience, certifications    |
| ORG#TechCorp    | MGR#Lee         | id, name, email, experience, certifications    |

This design allows you to fetch all related data (e.g., all projects in a department) with a single query.

## Access Patterns

### Get Organization Metadata
Query: PK = ORG#TechCorp AND SK = METADATA

### Get All Departments
Query: PK = ORG#TechCorp AND SK BEGINS_WITH DEPT#

### Get a Specific Department (e.g., Engineering)
Query: PK = ORG#TechCorp AND SK = DEPT#Engineering

### Get All Projects in a Department
Query: PK = ORG#TechCorp AND SK BEGINS_WITH PROJ#

### Get All Employees in a Project
Query: PK = ORG#TechCorp AND SK BEGINS_WITH EMP#

### Get Manager Details
Query: PK = ORG#TechCorp AND SK BEGINS_WITH MGR#

---

## Multiple-Table Design: The RDBMS Hangover

In a **Multiple-Table Design**, each entity is stored in a separate table, similar to a relational database. For example:
- `OrganizationTable`
- `DepartmentTable`
- `ProjectTable`
- `EmployeeTable`

### Disadvantages of Multiple-Table Design

1. **Increased Costs**:
   - Fetching related data requires multiple queries, increasing read/write costs.
   - Each query consumes capacity units, which can add up quickly.

2. **Reduced Performance**:
   - Joins are not supported in DynamoDB, so you need to perform multiple queries and join data in your application.
   - This introduces latency and complexity.

3. **Complexity**:
   - Managing multiple tables and relationships becomes challenging.
   - Requires additional application logic to handle joins and relationships.

4. **Inefficient for Hierarchical Data**:
   - Fetching hierarchical data (e.g., all employees in a project) requires multiple queries, which is inefficient.

### Example Use Case
Using the same organization example, you would need to:
1. Query the `DepartmentTable` to get department details.
2. Query the `ProjectTable` to get projects in the department.
3. Query the `EmployeeTable` to get employees in each project.

This approach is not only inefficient but also costly and slow.

---

## Why I Prefer Single-Table Design

My preference for the **Single-Table Design** is driven by two key factors: **cost** and **performance**.

1. **Cost**:
   - DynamoDB charges based on read/write capacity units. With a single-table design, you minimize the number of operations required to fetch data, reducing costs significantly.
   - Multiple-table designs often require additional queries, which increase costs.

2. **Performance**:
   - Single-table design allows you to fetch all related data in a single query, resulting in faster response times.
   - Multiple-table designs require multiple queries and application-level joins, which introduce latency.

---

## When to Use Multiple-Table Design

While I advocate for single-table design, there are scenarios where a multiple-table design might make sense:
- **Ad-Hoc Queries**: If your access patterns are unpredictable or frequently changing, multiple tables might offer more flexibility.
- **Data Isolation**: If you need strict isolation between entities (e.g., for security or compliance reasons), multiple tables can help.
- **Legacy Systems**: If you’re migrating from an RDBMS and want to maintain a similar structure, multiple tables might be easier to implement initially.

---

## Conclusion

DynamoDB is a powerful NoSQL database, but its true potential is unlocked only when you design your schema with its strengths in mind. While the familiarity of RDBMS might tempt you to use a multiple-table design, the **Single-Table Approach** is the way to go for most use cases. It offers significant advantages in terms of cost, performance, and scalability.

As developers, we need to break free from the relational mindset and embrace the NoSQL way of thinking. By designing your DynamoDB schema around access patterns and leveraging single-table design, you can build highly scalable, cost-effective, and performant applications.
