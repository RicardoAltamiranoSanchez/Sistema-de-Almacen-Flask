##lo importamos de esta manera ya que db es una variable global
from my_app import db
#db.models es para crear un modelo de pasamos como parametro estos valores es por default
from flask_wtf import FlaskForm
from wtforms import StringField 
from wtforms.validators import InputRequired 
from decimal import Decimal
class Categorias(db.Model):
    ___table___='categorias'#Definimos elnombre de nuestra tabla con 3 guiones bajo
#db.Column es para definir si es una columna y adentro de poneoms los valores o el tipo de dato que van a tener    
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(255))
    #hacemos la relacion de uno a muchos primero ponermos el nombre el la clase de modelo de la tabla Productos
    #Despues como lo vamos a indenticar puede ser caulquier nombre asi lo vamos a llamar y el lazy es el tipo de consulta
    productos=db.relationship('Productos', backref='categoria',lazy='select')
   
    def __init__(self,nombre):#Es solo el constructor
        self.nombre=nombre
  
    def __repr__(self):#Es como lo vamos a mostra al momento de pedir el objeto en consola
        return '<Producto %r>' % (self.nombre)

#Creamos el formulario de producto
class FormularioCategoria(FlaskForm):#de pasamoss la importacion  anuestra clase para crear el formulario
    nombre=StringField('nombre',validators=[InputRequired()])#de Indicamos que va ser de tipo string validator es para vadilar el campo loimportamos wtform
#documentacion de  relacionde muchos a uno https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#one-to-many-relationships