from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import url_postgres
import psycopg2

engine = create_engine(url_postgres)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


    









