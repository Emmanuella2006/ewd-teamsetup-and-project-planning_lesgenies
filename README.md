## Project Description
A fullstack application that processes MoMo SMS data in XML format, 
cleans and categorizes it, stores it in a relational database, and 
visualizes it through a frontend dashboard.

## Team Members
- Fidelis Mwiti
- Honnete Nishimwe
- Emmanuella Gacuti

## Project Structure

├── README.md
├── .env.example
├── requirements.txt
├── index.html
├── web/
│   ├── styles.css
│   ├── chart_handler.js
│   └── assets/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── db.sqlite3
│   └── logs/
├── etl/
│   ├── config.py
│   ├── parse_xml.py
│   ├── clean_normalize.py
│   ├── categorize.py
│   ├── load_db.py
│   └── run.py
├── api/
├── scripts/
└── tests/

## Scrum Board;
https://github.com/users/Emmanuella2006/projects/2/views/1

## Architecture Diagram
This is the link to our architecture diagram; https://miro.com/app/board/uXjVHVg6t7c=/
<img width="1780" height="865" alt="image" src="https://github.com/user-attachments/assets/737d3bae-a5c0-444d-ae57-3d06a6dfb418" />

**Database Desig and implementationn**
Database Overview
Building on the team setup and project planning, the database design and implementation focuses on designing and implementing the relational database that stores all MoMo transaction data. The schema was derived directly from the MoMo XML structure and covers five entities: Users, Transactions, Transaction_Categories, User_Permission, and System_Log.

**Entity Relationship Diagram**
The full ERD is available at docs/erd_diagram.png.
The diagram was built using Miro and uses crow's foot notation to express cardinality. It clearly marks all primary keys (PK) and foreign keys (FK) across all five entities.

Entities and what they represent:

Users — stores every participant in a transaction, whether as a sender or receiver. Key attributes include user_id (PK), full_name, phone_number, and account_balance.
Transactions — the central table of the schema. Links senders and receivers from the Users table, assigns a category, and stores the amount, fee, timestamp, and the original raw SMS body for auditing.
Transaction_Categories — a lookup table for transaction types such as Money Received, Payment, Bank Deposit, Airtime, and Transfer. Keeping categories in a separate table means new types can be added without touching the core schema.
User_Permission — a junction table that resolves the many-to-many relationship between Users and Transaction_Categories. It uses a composite primary key (user_id + category_id) and a boolean is_allowed flag to control which transaction types each user can perform.
System_Log — tracks every processing event during XML ingestion, recording which service centre handled the transaction, the protocol used, and the status code returned.

Relationships:
RelationshipCardinalityMeaningUsers → Transactions (sender)1 : ManyOne user can send many transactionsUsers → Transactions (receiver)1 : ManyOne user can receive many transactionsTransaction_Categories → Transactions1 : ManyOne category groups many transactionsUsers ↔ Transaction_CategoriesMany : ManyResolved by the User_Permission junction tableTransactions → System_Log1 : ManyOne transaction can generate multiple log entries
<img width="847" height="724" alt="image" src="https://github.com/user-attachments/assets/4710ba00-ee1c-4fe8-8a51-6876fc90994e" />


**Database Schema**

The schema includes the following tables:
**Users** :stores sender and receiver information (name, phone number, account balance)

**Transactions**:the central table linking users, categories, amounts, timestamps, and raw SMS data

**Transaction_Categories**:lookup table for transaction types (Money Received, Payment, Bank Deposit, Airtime, Transfer)

**User_Permission**:junction table resolving the many-to-many relationship between Users and Transaction_Categories

**System_Log**:audit trail for XML ingestion events per transaction



**SQL Setup**
The full setup script is at database/database_setup.sql. It includes DDL statements for all tables, foreign key constraints, indexes, and sample data.

**JSON Examples**
JSON schemas for all entities are at examples/json_schemas.json, showing how relational data is serialized for API responses.
