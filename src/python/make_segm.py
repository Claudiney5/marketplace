import os
import sqlalchemy
import argparse
import pandas as pd
import datetime

# endereço do projeto
BASE_DIR = os.path.dirname(os.path.abspath('__file__'))  # 'path.dirname' = diretório pai
DATA_DIR = os.path.join(BASE_DIR, 'data')  # 'join' une BASE_DIR com os argumentos
SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')

# parser de data para fazer a foto
parser = argparse.ArgumentParser()
parser.add_argument('--date_end', '-e', help='data de fim da extração (xxxx-xx-xx)', default='2018-06-01')
args = parser.parse_args()


date_end = args.date_end
ano = int(date_end.split("-")[0]) - 1
mes = int(date_end.split("-")[1])
date_init = f"{ano}-{mes}-01"

# importa a Query
with open(os.path.join(SQL_DIR, 'segments.sql')) as query_file:
    query = query_file.read()
query = query.format(date_init=date_init,
                     date_end=date_end)

# ABRINDO a conexão com o banco de dados
str_connection = 'sqlite:///{path}'    # para BANCO DE DADOS sqlite
connection = sqlalchemy.create_engine(
    str_connection.format(path=os.path.join(DATA_DIR, 'olist.db')))


create_query = f'''
create table TB_SELLER_SEGMENT as
{query}
;'''

insert_query = f'''
delete from TB_SELLER_SEGMENT where DT_SEGMENT = '{date_end}';
insert into TB_SELLER_SEGMENT 
{query}
;'''

try:
    connection.execute(create_query)
except:
    for q in insert_query.split(";")[:-1]:
        connection.execute(q)
