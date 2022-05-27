from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String, Integer
from config.db import meta, engine

users = Table("users", meta,
              Column("userID", Integer, primary_key=True),
              Column("name", String(255)),
              Column("email", String(255)),
              Column("password", String(100)))

meta.create_all(engine)
