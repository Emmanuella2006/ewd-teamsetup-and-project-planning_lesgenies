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
Building on the Week 1 setup, Week 2 focuses on designing and implementing the relational database that stores all MoMo transaction data. The schema was derived directly from the MoMo XML structure and covers five entities: Users, Transactions, Transaction_Categories, User_Permission, and System_Log.

Entity Relationship Diagram
The full ERD is available at docs/erd_diagram.png.
The diagram uses crow's foot notation and clearly marks all primary keys (PK), foreign keys (FK), and relationship cardinalities.

Database Schema
The schema includes the following tables:
-Users — stores sender and receiver information (name, phone number, account balance)
-Transactions — the central table linking users, categories, amounts, timestamps, and raw SMS data
-Transaction_Categories — lookup table for transaction types (Money Received, Payment, Bank Deposit, Airtime, Transfer)
-User_Permission — junction table resolving the many-to-many relationship between Users and Transaction_Categories
-System_Log — audit trail for XML ingestion events per transaction

SQL Setup
The full setup script is at database/database_setup.sql. It includes DDL statements for all tables, foreign key constraints, indexes, and sample data.

JSON Examples
JSON schemas for all entities are at examples/json_schemas.json, showing how relational data is serialized for API responses.
