# Scrapy Parser

## Requirements

- Python 3.12 or higher
- MySQL or MariaDB
- Redis 7.0 or higher

## Installation

### 1. Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Setup

```bash
cp .env.example .env
```
Edit the .env file.
You can set LOG_CHANNEL=debug to log to the console, or file to log to a file.
You can also configure the number of CONCURRENT_REQUESTS.

### 4. Proxy
Add proxy file to the root of the project. 
Make sure the filename matches the value set in the .env file

### 5. Database Setup

1) Connect to MySQL server:

```bash
mysql -u root -p
```

2) Create the database:

```bash
CREATE DATABASE parser CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
```

3) Exit MySQL:

```bash
exit
```

4) Run the import command (for PowerShell):

```bash
Get-Content dump.sql | mysql -u root -p parser
```

If the above command didn’t work, follow these steps:

5) Open your command prompt (cmd).

6) Navigate to the project directory, for example:

```bash
cd path\to\your\project
```

7) Run the import command:

```bash
mysql -u root -p parser < dump.sql
```

### 6. Run app
```bash
python3 add_start_url.py
scrapy crawl kreuzwort
```