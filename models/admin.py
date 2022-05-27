from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String, Integer
from config.db import meta, engine

admins = Table("admins", meta,
               Column("adminID", Integer, primary_key=True),
               Column("name", String(255)),
               Column("email", String(255)),
               Column("password", String(100)))

meta.create_all(engine)
