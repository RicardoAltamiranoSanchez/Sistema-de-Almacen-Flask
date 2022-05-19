##lo importamos de esta manera ya que db es una variable global
from my_app import db
#db.models es para crear un modelo de pasamos como parametro estos valores es por default
from flask_wtf import FlaskForm,RecaptchaField#recaptcha de google
from wtforms import StringField,HiddenField,FormField,FieldList#list para crear el formulario lo importamos
from wtforms.validators import InputRequired,ValidationError#ValidationError es para poder crear Nuestras propias funciones de validaciones 
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
        
# #Hacemos una funcion para hacer validaciones si ya existe la categoria
# def ExisteCategoria(form, field):
# #buscamos si existe con el nombre el field es el nombre del campo que se va a validar
#     existe=Categorias.query.filter_by(nombre=field.data).first()
#     if existe:
#        #Creamos un mensaje si ya existe la categoria
#         raise ValidationError("Esta Categoria ya existe: %s registra otra diferente" % field.data)
#Esta funcion tiene dos validaciones el contain es la longitud del la categoria 
#el like es igual que en base de datos busco las concidencias desde el inicio y el final 
#Y retornamos la funcion de _ExisteCategoria en la otro funcion es como la primera funcion que hicimos
#lo que cambia es la validacion de la logintud de la categoria para desactivarla solo de ponemos false
def ExisteCategoria(contain=True):
    def _ExisteCategoria(form ,field):
        #es para ver el id de la categoria print(form.id_formulario.data+"Categoriaaaa")
        if contain:
             existe=Categorias.query.filter(Categorias.nombre.like("%"+field.data+"%")).first()
        else:
             existe=Categorias.query.filter(Categorias.nombre.like(field.data)).first()
        #validacion cuando queremos crear un registro con el mismo nombre     
        if existe and form.id_formulario.data == "":
            raise ValidationError("Esta Categoria ya existe: %s registra otra diferente" % field.data)
        #validacion para actualizar el mismo nombre en la categoria con el mismo id no con otro
        if existe and form.id_formulario.data and existe.id !=int(form.id_formulario.data):
             raise ValidationError("Esta Categoria ya existe: %s registra otra diferente" % field.data)
    return _ExisteCategoria    

 #Creamos un formulario hijo y todo de esto se hereda al otro formulario de
class FormularioTelefono(FlaskForm):#de pasamoss la importacion  anuestra clase para crear el formulario
       telefono=StringField('Telefono')
       postal=StringField('Postal')
       dirrecion=StringField('Dirrecion')


#Creamos el formulario de producto
# hacemos herenencia de primer formulario y podemos usarlo todos sus componentes normales
# asi administramos mejor nuestro formulario
class FormularioCategoria(FormularioTelefono):#de pasamoss la importacion  anuestra clase para crear el formulario
    nombre=StringField('nombre',validators=[InputRequired(),ExisteCategoria()] )#de Indicamos que va ser de tipo string validator es para vadilar el campo loimportamos wtform
    id_formulario=HiddenField('id_formulario')
#Construir multiples campos de formulario de forma dinamica
    telefonos=FieldList(FormField(FormularioTelefono))
    recaptcha=RecaptchaField()#esto ya es de flask para utilizar el Recaptcha de google para evitar el spam
    #podemos crear una lista de elemnetos de un formulario para
    formularioList=FormField(FormularioTelefono)
#El HiddenField es de tipo de dato oculto    
#documentacion de  relacionde muchos a uno https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#one-to-many-relationships
#documentacion para crear nuestra propias validaciones https://wtforms.readthedocs.io/en/stable/validators/
