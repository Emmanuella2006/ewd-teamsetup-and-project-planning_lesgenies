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
<img width="1418" height="702" alt="image" src="https://github.com/user-attachments/assets/11edecbf-ffa3-4190-b431-b34543878b5b" />

>>>>>>> 940069952a15e4b72ad430402fd4d51e08e26e71
Database Design

Database Overview
Building on the team setup and project planning, the database design fo focuses on designing and implementing the relational database that stores all MoMo transaction data. The schema was derived directly from the MoMo XML structure and covers five entities: Users, Transactions, Transaction_Categories, User_Permission, and System_Log.

Entity Relationship Diagram
The full ERD is available at docs/erd_diagram.png.
The diagram uses crow's foot notation and clearly marks all primary keys (PK), foreign keys (FK), and relationship cardinalities.

Database Schema
The schema includes the following tables:
Users — stores sender and receiver information (name, phone number, account balance)
Transactions — the central table linking users, categories, amounts, timestamps, and raw SMS data
Transaction_Categories — lookup table for transaction types (Money Received, Payment, Bank Deposit, Airtime, Transfer)
User_Permission — junction table resolving the many-to-many relationship between Users and Transaction_Categories
System_Log — audit trail for XML ingestion events per transaction
SQL Setup
The full setup script is at database/database_setup.sql. It includes DDL statements for all tables, foreign key constraints, indexes, and sample data.
JSON Examples
JSON schemas for all entities are at examples/json_schemas.json, showing how relational data is serialized for API responses.


**Database Design and implementationn**

Database Overview
Building on the team setup and project planning, the database design and implementation focuses on designing and implementing the relational database that stores all MoMo transaction data. The schema was derived directly from the MoMo XML structure and covers five entities: Users, Transactions, Transaction_Categories, User_Permission, and System_Log.

**Entity Relationship Diagram**
The full ERD is available at docs/erd_diagram.png.
The diagram was built using Miro and uses crow's foot notation to express cardinality. It clearly marks all primary keys (PK) and foreign keys (FK) across all five entities.

<img width="842" height="720" alt="image" src="https://github.com/user-attachments/assets/3c90e58c-276b-4e98-b595-aa358c468398" />

  
Entities and what they represent:

Users:stores every participant in a transaction, whether as a sender or receiver. Key attributes include user_id (PK), full_name, phone_number, and account_balance.

Transactions:the central table of the schema. Links senders and receivers from the Users table, assigns a category, and stores the amount, fee, timestamp, and the original raw SMS body for auditing.

Transaction_Categories:a lookup table for transaction types such as Money Received, Payment, Bank Deposit, Airtime, and Transfer. Keeping categories in a separate table means new types can be added without touching the core schema.

User_Permission:a junction table that resolves the many-to-many relationship between Users and Transaction_Categories. It uses a composite primary key (user_id + category_id) and a boolean is_allowed flag to control which transaction types each user can perform.

System_Log:tracks every processing event during XML ingestion, recording which service centre handled the transaction, the protocol used, and the status code returned.

Relationships:
<img width="1009" height="407" alt="image" src="https://github.com/user-attachments/assets/821e904f-44fe-413b-ba97-5118c2f8487c" />


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


THE BASIC AUTHENTICATION FUNCTIONALITY
 - The basic authentication helps protect the protected resources and requires a username and password to access.
 - When the user access the resource without a password, the server challenges the client with status_code 401 Unauthorised
 - The password and username are either saved in the database or hardcoded. When the user inputs the password to login, The username is combined with the password using a semicolon and is encoded into  base64 format.
 - When the user sends a new request containing the Authorisation header, it checks whether the header Authorisation starts with "Basic". It then decodes it and checks whether it matches to the saved password and username.
 - If the password and the username matches, a response is provided with the requested data, else, it returns an error paage with status code 401. Therefore anyone packet-sniffing an unencrypted http network, they can easily copy the base64 string and decode it back to plain text and get the username and password in seconds.

 - No expiration - Basic authentication credentials do not expoire normally unless you chanhge the password yourself which makes it even more susceptible to interceptions.

 - Username and password entry with every single request - This is where the user is expected to send the username and password every time they make a request which makes it prone to interception by malicious individuals. Once one request is intercepted, the username and password is obtained through the base64 string which is later decoded and this compromises the system.


STRONGER AUTHENTICATION ALTERNATIVES:
JWT (JSON Web Tokens) - This is where the user logs in once and the server generates a signed, time-locked tocken which the clienf can send this token instead of username and password for all future requests.

 - The token expires automatically - such as the github classic tokens
 - Contains custom permissions by the user
 - The server doesn't need to check the database every single time a request is made.

OAuth 2.0 - This is a token-exchange frameworks that delegates authentication to a dedicated provider such as Google, AuthO
 - This ensures that the app never interacts with the user's actual password meaning more security for the users credentials even in cases of app's security risks
 - Supports features such as the multi-factor authentication(MFA) and granulaar API scopes
