##lo importamos de esta manera ya que db es una variable global
from my_app import db
#db.models es para crear un modelo de pasamos como parametro estos valores es por default
from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField,HiddenField
from wtforms.validators import InputRequired ,EqualTo
#importamos el check password para revisar si la contraseña esta bien por que esta encryptada
#y el generate password es para encryptar la contraseña
from werkzeug.security import check_password_hash,generate_password_hash

from decimal import Decimal
#importamos el Enum para poner los roles y hacer las columnas de tipo Enum
from sqlalchemy import Enum
#Importamos el tipo de dato para utilizarlo despues
import enum
#Creamos una clase para pode usar los enum y hacer los roles para crear las columnas
class rolUsuario(enum.Enum):
    regular=1
    adminstrador=2
    


class Usuarios(db.Model):
    ___table___='Usuarios'#Definimos elnombre de nuestra tabla con 3 guiones bajo
#db.Column es para definir si es una columna y adentro de poneoms los valores o el tipo de dato que van a tener    
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(255))
    passwordHash=db.Column(db.String(255))
    rol=db.Column(Enum(rolUsuario))
    #implemnetacions para falsl_login solol as funciones con valores boleanosn de ven de tipo property
    @property
    def is_authenticated(self):#Espara la autenticatio 
        return True
    @property
    def is_active(self):#para ver si esta conectado 
        return True
    @property
    def is_anonymous(self):#Si hay usuario anonimos
        return False
   #Aqui lo deje sin el  @property por que me mara error de str en autenticacion
    def get_id(self):#Solo obtener el id
        return str(self.id)
    
    
    
    
#Creamos en rol por defecto
    def __init__(self,nombre,passwordHash,rol=rolUsuario.regular):#Es solo el constructor
        self.nombre=nombre
        self.passwordHash=generate_password_hash(passwordHash)
        self.rol=rol
#Creamos la funcion para verificar si esta correcto el password
#debmoes hacer referencia al self y despue metemo self.de nuetro password y el password es el que no esta registrando    
    def check_password(self,password):
        return check_password_hash(self.passwordHash,password)
        
    def __repr__(self):#Es como lo vamos a mostra al momento de pedir el objeto en consola
        return '<Producto %r>' % (self.nombre)

#Creamos el formulario de producto
class FormularioLogin(FlaskForm):#de pasamoss la importacion  anuestra clase para crear el formulario
    nombreUsuario=StringField('nombre',validators=[InputRequired()])#de Indicamos que va ser de tipo string validator es para vadilar el campo loimportamos wtform
    password=PasswordField('contraseña',validators=[InputRequired()])
    #creamos un parametro de next para proteger la ruta y usar los flask next
    #el hidden es para mostrar un elemento oculto
    nextLogin=HiddenField('nextLogin')
    
class FormularioRegistro(FlaskForm):#de pasamoss la importacion  anuestra clase para crear el formulario
    #El EqualTo es para buscar el campo que va verificar si es igual y de enviamos un mensaje si esta incorrecto
    nombreUsuario=StringField('nombre',validators=[InputRequired()])#de Indicamos que va ser de tipo string validator es para vadilar el campo loimportamos wtform
    password=PasswordField('contraseña',validators=[InputRequired(),EqualTo('confirmarPassword', message='La contraseña no coiciden')])
    confirmarPassword= PasswordField('Debe confirmar contraseña')    
    #PasswordFiel es para crear un input de tipo password
#documentacion de  relacionde muchos a uno https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#one-to-many-relationships
#documentacion para confirmar constreña