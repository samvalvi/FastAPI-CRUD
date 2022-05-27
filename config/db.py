from sqlalchemy import create_engine, MetaData

engine = create_engine('mysql+pymysql://root:Meli8462@localhost:3306/crud_api')

meta = MetaData()

conn = engine.connect()
