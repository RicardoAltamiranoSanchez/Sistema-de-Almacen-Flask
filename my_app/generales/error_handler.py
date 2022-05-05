from my_app import app
from flask import render_template
#con errorhandler podemos manejar los errores de la aplicacion o cuando no existe una pagina
#se debe poner un parametro afuerza por eso la e
@app.errorhandler(404)
def NoExisteLaPagina(e):
    return render_template('generales/404.html',e=e),404
    
#este es para el error 503 error del servidor
#Añadimos la Exception es propiop de python para que nos muestre el error
#Y enviamos los parametros con la e de tipo error y la mostrabamos dentro de la plantilla
@app.errorhandler(Exception)
def ErrorDelServidor(e):
    return render_template('generales/503.html',e=e),503