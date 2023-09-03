import sqlalchemy as sq
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from models import create_tables, Publisher, Book, Stock, Shop, Sale
import json, os

def json_to_db():
    metadata = MetaData()
    file_path = f'{os.getcwd()}\\tests_data.json'
    with open(file_path) as f:
        json_data = json.load(f)
        f.close()
    for i in json_data:
        mytable = Table(i["model"], metadata, autoload_with=engine)
        dict_val = i["fields"]
        dict_val["id"] = i["pk"]
        session.execute(mytable.insert(), dict_val)
        session.commit()

def publisher_stat(publisher):
    '''
    select  a.title, c.name, d.price, d.date_sale from book as a 
	join stock as b on a.id = b.id_book
	join shop as c on b.id_shop = c.id
	join sale as d on b.id = d.id_stock
	join publisher as e on a.id_publisher = e.id 
	where e.name = 'No starch press'
    '''
    q = select(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.name == publisher)
    # print(q)
    res = session.execute(q).all()
    lens = []
    for i in range(0, len(res[0])):
        lens.append(0)
    for i in res:
        for v in range(0, len(i)):
            lens[v] = len(str(i[v])) if len(str(i[v])) > lens[v] else lens[v]
    for c in res:
        print(f'{{0:<{lens[0]}}} | {{1:<{lens[1]}}} | {{2:<{lens[2]}}} | {{3}}'.format(*c))
    print('\n')


login = '' # Введите логин пользователя БД
password = '' # Введите пароль пользователя БД
db = '' # Введите имя БД
DSN = f"postgresql://{login}:{password}@localhost:5432/{db}"
engine = sq.create_engine(DSN)
create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()

json_to_db()

publisher_stat('O’Reilly')
publisher_stat('Pearson')
publisher_stat('Microsoft Press')
publisher_stat('No starch press')

session.close()
