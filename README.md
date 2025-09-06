# PostgreSQL Multi-Table Data Initialization

This project is a **Python-based PostgreSQL database initializer** that creates tables, inserts test data, and validates records. It uses **threading** to insert data into multiple tables (`users`, `products`, and `orders`) concurrently, saving time.

---

## Project Overview

- **Database**: PostgreSQL  
- **Tables**:
  - `users`: Stores user information (`id`, `name`, `email`)
  - `products`: Stores product details (`id`, `name`, `price`)
  - `orders`: Stores order records (`id`, `user_id`, `product_id`, `quantity`)
- **Features**:
  - Creates tables only if they don't already exist.
  - Inserts data only if a record with the same `id` is not present.
  - Validates data for missing fields, negative prices, and invalid order quantities.
  - Uses **threading** for concurrent data insertion.

---

## Requirements

- Python 3.11+  
- PostgreSQL installed and running  
- `.config.yml` file containing your PostgreSQL credentials:

```env
host=your_host
database=your_database_name
password=your_password
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <project-directory>
```

### 2. Create a Virtual Environment

```bash
python.exe -m venv venv
```

### 3. Activate Virtual Environment

**Windows**:
```bash
venv\Scripts\activate
```

### 4. Install Dependencies

Make sure you have a `requirements.txt` file that includes required packages like `psycopg2` and `python-dotenv`.

```bash
pip install -r requirements.txt
```

---

## How to Run the Project

```bash
python ./connection_file_db.py
```

---

## Project Structure

```plaintext
project/
├── connection_file_db.py    # Main script to initialize DB and insert data
├── requirements.txt         # Python dependencies
├── config.yml                    # Database credentials
└── README.md                # Project documentation
```

---

##  Example Output

```plaintext
Tables created successfully.
Inserted into users: (1, 'Alice', 'alice@example.com')
Invalid product price: (10, 'Earbuds', -50.00)
Invalid order quantity: (9, 9, 1, -1)
```

---

##  Key Highlights

- Lightweight and beginner-friendly project to learn database automation with Python.
- Demonstrates PostgreSQL integration, data validation, and multi-threading.
- Easy to extend for larger applications or production workflows.

---

##  Requirements.txt

```txt
psycopg2-binary==2.9.7
python-dotenv==1.0.0
```

---

##  Configuration

Create a `config.yml` file in your project root with the following variables:

```env
# Database Configuration
host=localhost
database=your_database_name
user=your_username
password=your_password
port=5432
```

---

##  Data Validation Features

- **Users Table**: Validates that name and email are not empty
- **Products Table**: Ensures price is not negative
- **Orders Table**: Checks that quantity is positive
- **Duplicate Prevention**: Prevents insertion of records with existing IDs

---

##  Threading Implementation

The project uses Python's `threading` module to:
- Insert data into multiple tables simultaneously
- Improve performance for large datasets
- Maintain thread safety with proper connection handling

---
