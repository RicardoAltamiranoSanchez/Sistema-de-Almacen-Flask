from my_app import app
#Levantamos las configuracion desde nuestro archivo config 
#utilizamos from_pyfile()y solo indicamo el path donde esta indicado el archvico config debe de ir antes del rujn
#app.config.from_pyfile('config.py') solo se usa para referencia el archvio
#para referenciar varios tipos de configuracion es con clases y se utiliza
#from _object("nombre donde esta ubiacado el archivo"."la clase o objeto que va utilizar la configuracion")
app.config.from_object('configuration.DesarrolloConfig')#Debe estar al mimo nivel de run.py el archivo de configuracion

app.run()
#para activa el modo debug o desarrollo
#app.run(debug=True)
#app.config['debug']=True
#app.debug=True
#Solo para arrancar la aplicacion
#El run.py debe estar al mismo nivel que la otra caropete donde esta los modulos por queme marca error
#En la carpte modulo my_app esta el __init__ donde lleva el from flask import Flask 
#desde ahi se importa para los demas archivos
#pip freeze para ver que librerias estan instaladas
#para exportar las librerias que tenemos en el proyecto pip freeze > requerimientos.txt
#documentacion de de consultas de base de datos https://docs.sqlalchemy.org/en/13/orm/query.html https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/
#Libreria para instalar en formulario  y hacer uso de ello pip install Flask-WTF
