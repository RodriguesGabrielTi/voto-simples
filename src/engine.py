from sqlalchemy import create_engine

database = open('database.db', 'a+')
engine = create_engine('sqlite:///database.db', echo=True)

