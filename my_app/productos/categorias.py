#from my_app import app
#importamos el app que esta en run.py desla carpteta inicial como si estuvieramos haciendo uncontrolador

#utilizamos el blueprint para registrar el modulo lo importamos el blueprint
from flask import Blueprint,render_template,request,redirect,url_for,flash,get_flashed_messages

from werkzeug.exceptions import abort
#importamos el modelos de la base de datos para usarla ne la visa
from my_app.models.modelCategoria.categoria import Categorias
from my_app.DB.database import db
from sqlalchemy.sql.expression import not_,or_ #importamos elnot y el or
from my_app.models.modelCategoria.categoria import FormularioCategoria
from flask_login import login_required
from my_app import Rol_Admin,mail
from flask_mail import Message

from collections import namedtuple #importamos para crear una tupla de collections

categoria=Blueprint('categoria',__name__)#pasamos el nombre de la aplicacion en el __name__ el primer parametro es como lo vamos a importar como asiganrla el nombre a un variable

#el before reques es para que haga primero esto antes que lo demas
#y verifica si esta authenticado el usuario para entrar ala plantilla con login_required()
@categoria.before_request
@login_required
#Este es el decorador que hicimos en el init de la app para verificar si es usuario admin
@Rol_Admin
def Construtor():
    pass


@categoria.route('/categoria')
@categoria.route('/categoria/<int:page>')
def Inicio(page=1):
    #para enviar el mensaje esto solo es una prueba para ver si funciona el recipients es para indicar a cual se lo vamos a enviar
    #si envia pero el proxy de con la lap que trabajo no me deja XD 
    msg=Message('Hola Flask!!..',recipients=['pruebaflask@gmail.com'])
    #el body es elc cuerpo del mensaje
    #importamos el mail que tenemos en el init y enviamos en mensaje en send(msg)
    msg.body="Que pedo"
    mail.send(msg)
     #categoria=Categorias.query.all()#obtemos todos los categoria y query espara hacer consultas en la base de datos
     #Esto es para poder paginar la pagina mostar mas paginas y que no todo este desosrdenado con categoria.query.paginate adentro de indicamos las paginas o valor de donde va empezar el paginado
     #el 5 es numero de elementos que se va mostrar en la parte de frente enviamos los items osea todo los elemnteos categoria.items
    return  render_template('categoria/index.html',categorias=Categorias.query.paginate(page,5))#lo mandamos ala plantilla html

@categoria.route('/detalle-categoria/<int:id>')#de ponemos el valor int  por que en defautl esta en string
def Detalle(id):
    categoria=Categorias.query.get_or_404(id)#con query.get(id )obtenmos el valor de un elemento con get_or_404 indica que si no existe el elemento que me muestre la pagina 404
   
    return render_template('categoria/show.html',categoria=categoria)      

@categoria.route('/filtro')
@categoria.route('/filtro/<int:id>')
def Filtro(id):
    categoria=Categorias.get(id)
   
    return render_template('categoria/filtro.html',categoria=categoria)
#para el uso de los filtros documentacion  https://jinja.palletsprojects.com/en/2.10.x/templates/#list-of-builtin-filters
#ruta http://127.0.0.1:5000/filtro/4
#para crear nuestro propiso filtros
@categoria.app_template_filter('iva')#indicamos la app  asi nombramos nuestra app con app=flask() y el app_template_filter es por defecto para creaer un nuevo filtro
def iva_filter(categoria):#de pasamos en objeto odicionario pra hacer la validacion
    if(categoria):
        return  categoria['price']*0.20
    return 'Sin precio papu'

#Formulario
@categoria.route('/crear-categoria',methods=['GET','POST'])
def Crear():
    formulario=FormularioCategoria()#(meta={ 'csrf':False})#quitamos el token para poder hacer la peticion sin problema mas adelan lo pondremos el token sirve para protegernos de los ataques del exterior
    if formulario.validate_on_submit():#Es par verficar si dio submit al boton o si es una peticion post
        p=Categorias(request.form['nombre'])
        db.session.add(p)
        db.session.commit()
        flash('Categorias creado con exito!!')
        return redirect(url_for('categoria.Crear'))
    if formulario.errors:
          flash(formulario.errors,'danger')#de pasamos los errores si hay alguno dange es para decir que es un error lo muestra asi 
       
    #print(get_flashed_messages())#Obtemos todos los mensajes hechos con el metodo flash
    return render_template('categoria/crear.html',formulario=formulario)



##con request obtemos los valor que estan en el formulario igual que node solo ponermos el id que queremos
#lo pusimos en comentarios este es solo la misma funcon de Crear pero lo metimos juntos para ahorrar codigo
##@categoria.route('/crear-categoria',methods=['POST'])
#def CrearProducto():
#    p=Categorias(request.form['nombre'],request.form['precio'])
#    db.session.add(p)
#    db.session.commit()
#    flash('Producto creado con exito!!')#flash es para crear un mensaje con si fuera un alert
#    return redirect(url_for('categoria.Crear'))#lo redirigimos al al funcion de get ponemos le modulo y la funcion en donde queremos redigir des pues de termianr la ejecucion

#funcion de editar
#@categoria.route('/editar-categoria/<int:id>')
#def Editar(id):
#    categoria=Categorias.query.get_or_404(id)
#    return render_template('categoria/editar.html',categoria=categoria)
#Creamos una nueva ruta no importa la ruta pero si el id y el methos ya que la utilizamos
#en el html en action para referenciar al modulo y la funcions solo nos interesa el proceso de la funcion
@categoria.route('/actualizar-categoria/<int:id>',methods=['GET','POST'])
def Actualizar(id):
    categoria=Categorias.query.get_or_404(id)
    formulario=FormularioCategoria()#(meta={ 'csrf':False})#quitamos el token para poder hacer la peticion sin problema mas adelan lo pondremos el token sirve para protegernos de los ataques del exterior
   #mandamos a llamar el productos es el nombre que definimos en categoira models  productos=db.relationship('Productos', backref='categoria',lazy='select')
    print(categoria.productos)
    #creamos una tupla para crear el formulario dinamico y  de ponemos los valores que en el archivo de models del formulario
    group=namedtuple('group',['postal','telefono','dirrecion'])
    #creas tres tuplas con el id de group con datos llenados solo para realizar pruebas
    g1=group('414','5534343434','cuactemoc')
    g2=group('543','4465343465','nezahualcoyotl')
    g3=group('512','4465343465','Coyoacan')
    #nos creaamos un objeto con un vector no se si es una lista  para despues llamarlo en data del formulario
    #donde esta el campo del mismo nombre 
    telefonos={'telefonos':[g1,g2,g3]}
    
    formulario=FormularioCategoria(data=telefonos)
    #para eliminar elementos de un formulario con delete
    del formulario.formularioList
    #pasamos datos del formulario a un objeto
    c=Categoria(name ="Cate 1")
    
    if request.method == 'GET': #para cada vez que entre el usuario pueda tomar el valor en los inputs del proudco y los muestre
        formulario.nombre.data=categoria.nombre#ponemos el valor del categoria del id en el input
        formulario.id_formulario.data=categoria.id #obtenemos el valor de id de la base de datos y lo igualamos al campo oculto para poder actualizar y hacer que la funcion no marque error
    if formulario.validate_on_submit():#Es par verficar si dio submit al boton o si es una peticion post
         categoria.nombre=formulario.nombre.data#se puede obteneer el valor directamente ya que usarmo el wtform 
         formulario.populate_obj(c)
         print(c.nombre)
         db.session.add(categoria)
         db.session.commit()
         flash("Registro Actualizado con Exito")
         return redirect(url_for('categoria.Inicio'))#con  redirect se usa el modulo y la funcion para redirigir a otra pagina
    if formulario.errors:
        flash("No se puede Actualizar el Prodcuto",'danger')
    return render_template('categoria/editar.html',formulario=formulario,categoria=categoria)        


@categoria.route('/eliminar-categoria/<int:id>')
def Eliminar(id):
    categoria=Categorias.query.get_or_404(id) 
    db.session.delete(categoria)
    db.session.commit()
    flash('Categorias Elimnada con exito!!')
    return redirect(url_for('categoria.Inicio'))
    
          
@categoria.route('/test')
def test():
    #p=Categorias.query.limit(2).all() Obtenemos todos los elementos pero  con el limit lo limitamos a dos
    #p=Categorias.query.limit(2).first() nos da el primer valor con first
    #p=Categorias.query.order_by(Categorias.id:desc()).all() nos devuelve los valor pero los ordenamos enforma descendente 
    #p=Producto.query.get({"id":"1"}) obtenemos el valor con el id solo se pude con get usar el id 
    #p=Producto.query.filter_by(name="categoria 1").all() nos devuelve el valor del nombre categoria 1 con filter_by para buscar el valor a travez d eotro parametro que n sea el id
    #p=Producto.query.filter(Producto.id > 1).all() para indicar operaciones debemo poner filter operacones de menor o mayor
    #p=Producto.query.filter_by(nombre="Producto 1",id=1).first() de pones dos condiciones para que nos traiga el valor de especificamos la coma seria como un and
    #p=Producto.query.filter_by(Producto.nombre.like('P%')).all() buscamos por el nombre que empieze por la letra P y que nos traiga todos los elementos
    #p=Producto.query.filter(not_(Producto.id > 1)).all()lo usamos para negar las cosas hacer a inversa 
    #p=Producto.query.filter(or_(Producto.id > 1,Producto.name=="Producto 1"))all() si una de las dos condiciones se cumple se ejecuta
    #para crear un registro en la base de datos
    #Crear nuevo registro
    #p=Categorias("categoria 5",80.49)
    #db.session.add(p)#Creamos un nuevos registro con session.add debemos importar el db
    #db.session.commit()#Guaradamos el nuevo registro en la vase de datos despues de agregado
    #
    ##Actualizamos el nuevo registro
    #p=Categorias.query.filter_by(nombre="Producto 1")#primero buscamos el registro que vamos a actualizar 
    #p.nombre="ProductoActualizado"#Despues lo actualziamos en la base de datos
    #db.session.add(p)
    #db.session.commit()
    ##Eliminamos un registro con delete
    #p=Categorias.query.filter_by(id=1)#Buscamos el registro 
    #db.session.delete(p)#Eliminaos el registro 
    #db.session.commit()#guardamos los cambios en la base de datos
    return 'Pruebas con consultas query'

