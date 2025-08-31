from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
#pip install sqlalchemy


#Replace USERNAME,PASSWORD, HOST, PORT, DBNAME with the info from config (or your own info)
engine = create_engine('mysql+pymysql://USERNAME:PASSWORD@HOST:PORT/DBNAME')

#Sessions allow you to interface with the DB from VS
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Card(Base):
    _tablename_ = 'Cards'
    card_id = Column(Integer, primary_key=True, nullable = False)
    card_name = Column(String(50), nullable=False)
    card_desc = Column(String(),nullable=False)
    card_type = Column(String(), nullable=False)
    
    def __init__(self, name, desc, type):
        self._name = name
        self._desc = desc
        self._type = type

    def __str__(self):
        return self._name
    
    @property
    def name(self):
        return self._name

    @property
    def desc(self):
        return self._desc

    @property
    def type(self):
        return self._type

Base.metadata.create_all(engine)
