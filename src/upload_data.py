import os  #  miscellaneous operating system interfaces
import pandas as pd
import sqlalchemy 

# para banco de dados em servidor:
"""user = 'eu' #login
password = 'segredo' # senha
host = 'database-1.fim_do_mundo.us-east.rds.ficcao.amazonaws.com' # ip/host/dns
port = '3306' # port
bd_str_connection = 'mysql+pymysql://{user}:{password}@{host}:{port}'"""

# para BANCO DE DADOS sqlite
str_connection = 'sqlite:///{path}'

BASE_DIR = os.path.dirname(os.path.abspath('__file__')) # 'path.dirname' = diretório pai
DATA_DIR = os.path.join(BASE_DIR, 'data')  #  'join' une os argumentos

# CAPTURANDO APENAS OS ARQUIVOS .csv DA PASTA DATA_DIR
## Forma 1
'''files_names = os.listdir(DATA_DIR)  # 'listdir' lista tudo o que ele encontra no diretório
correct_files = []
for i in files_names:
    if i.endswith('.csv'):
        correct_files.append(i)'''

## Forma 2 (Pythônica - list comprehesion ou compressão de lista)
files_names = [i for i in os.listdir(DATA_DIR) if i.endswith('.csv')]

# ABRINDO a conexão com o banco de dados
connection = sqlalchemy.create_engine(
    str_connection.format(path=os.path.join(DATA_DIR, 'olist.db')))

# Agora vamos importar estes dados e exportar para um BANCO DE DADOS
for i in files_names:
    df_tmp = pd.read_csv(os.path.join(DATA_DIR, i))
    table_name = 'tb_' + i.strip('.csv').replace('olist_', '').replace('_dataset', '')
    df_tmp.to_sql(table_name, 
                    connection,     # passando a tabela e a conexão (arquivo DB)
                    if_exists='replace',
                    index=False) 

