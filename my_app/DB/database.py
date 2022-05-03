from flask_sqlalchemy import SQLAlchemy
from my_app import app


#lo mostramos como false para que no muestre la advertencia creo que es igual que node para poder modificar los path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS ']=False
#configuracion de la base de datos con mysql
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:root@localhost:3306/Almacen"
#creamos una nueva variable llamada db y de pasamos elvalor de SQLALCHEMY(app)
db=SQLAlchemy(app)


##configuraciones para diferentipos de base de datos
#SQLITE
#sqlite:///database.db
#MYSQL 
#mysql+pymysql://user:password@ip:port/db_name
#POSTGRES
#postgresql+psycopg2://user:password@ip:port/db_name
#MSSQL
#mssql+pyodbc://user:password@dsn_name
#ORACLE
#oracle+cx_oracle://user:password@ip:port/db_name