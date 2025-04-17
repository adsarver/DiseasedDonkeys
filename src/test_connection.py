from sqlalchemy import create_engine, inspect

username = "root"
password = "root"
host = "localhost"
port = "3306"
database = "CS440"

connection_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(connection_url)

try:
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if tables:
        print("Tables in CS440:")
        for table in tables:
            print(table)
    else:
        print("No tables found in CS440.")
except Exception as e:
    print("Connection failed:", e)
