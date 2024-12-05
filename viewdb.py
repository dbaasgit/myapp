from sqlalchemy import create_engine, inspect

# Connect to the database
engine = create_engine("sqlite:///papers.db")

# Use SQLAlchemy's inspector to list tables
inspector = inspect(engine)
tables = inspector.get_table_names()

print("Tables in the database:")
print(tables)

# Loop through each table and print its columns
for table in tables:
    print(f"\nColumns in the '{table}' table:")
    columns = inspector.get_columns(table)
    for column in columns:
        print(f" - {column['name']} ({column['type']})")


