# ============================================================
# SQLAlchemy - Database Connection with an ORM Engine
# ============================================================
# Connection string format:
#   Dialect+Driver://Username:Password@Host:Port/Database
#
# This example uses MySQL with mysql-connector-python.
# Update the credentials and host to match your environment.
# ============================================================

from sqlalchemy import create_engine, text

database_url = "mysql+mysqlconnector://username:password@remote_host:3306/your_database"

engine = create_engine(database_url)

with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM your_table LIMIT 5"))
    for row in result:
        print(row)
