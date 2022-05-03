from flask import Flask,redirect,url_for
#para usar el flask login
from flask_login import LoginManager,current_user,logout_user
# para usar los decoradores y crear nuestro propios decoradores  es propio de python
from functools import wraps
#utilizamos el blueprint 
#primero hacemos la configuracion de la base de datos para que no halla conflicto despues
#despues importamos la vista  y por el ultiom el blueprint para que no halla confilicto enla creacion 
#primero creamos la app flask 
app=Flask(__name__)
#creamos el decorador antes de la vista 
#Creamos un decorador para que solo el usuario adminstrador pueda entrar
def Rol_Admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
    #Si es diferente o no es adminstrador cerramos session y lo redirigimos al Fusuario.login al login
    #current_user.rol.value es la funcion que hicimos en la autenticacion y obtenemos elvalor del usuario cuando entra en el login    
        if current_user.rol.value !="administrador":
              #para cerrar la senccion en  metodo de flask_login
           logout_user()
           return redirect(url_for('Fusuario.Login'))
            
        # if g.user is None:
        #     return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


#para utilizr y  importar el flask login
login_manager = LoginManager()
login_manager.init_app(app)#Iniciamos el ogin manager en el init
#indicamos donde esta la vista de Login para hacer los metodos o lo tome ahi
#Este tambien sirve para el flask_login login_required
login_manager.login_view = "Fusuario.Login"

#ya cuando halla terminado de cargar todo lo mandamos a llamar la creacion de datos
#despues importamos la base de datos donde hicimos un modulo

from my_app.DB.database import db

#Importamos las vistas o donde estan las peticiones get put post etc
from my_app.productos.productos import producto #importamos desde la ubicacion de la carpte y el nombre que de pusimos
from my_app.productos.categorias import categoria
#from my_app.autentication.Usuario import usuario
#IMportacion para el usso de flask login
from my_app.fautentication.FUsuario import Fusuario
#Importamos flask ya que despues de aqui lo vamos a importar a los demas archivo no olcidar
#utilizamos blueprint debemos registrar la vista de pasamos en nombre del archivo o vista

#Documnetacion de para usar el falsk login
#https://flask-login.readthedocs.io/en/latest/
#para intalar la libreria con pip install flask-login
app.register_blueprint(producto)
app.register_blueprint(categoria)
#app.register_blueprint(usuario)
app.register_blueprint(Fusuario)
#la ultimo mandamos a llamar y crear ala base de datos si no existe
db.create_all()

@app.template_filter('doble')
def doble_filter(n:int):
    return n*2
# documentacion para decoradores https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/