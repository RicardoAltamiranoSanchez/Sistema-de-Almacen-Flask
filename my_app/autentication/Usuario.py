from flask import Blueprint,render_template,request,redirect,url_for,flash,get_flashed_messages,session
from werkzeug.exceptions import abort
from my_app.DB.database import db
from sqlalchemy.sql.expression import not_,or_ #importamos elnot y el or
from my_app.models.Usuario.modelsUsuario import Usuarios,FormularioLogin,FormularioRegistro
usuario=Blueprint('usuario',__name__)#pasamos el nombre de la aplicacion en el __name__ el primer parametro es como lo vamos a importar como asiganrla el nombre a un variable

#Formulario
@usuario.route('/RegistroUsuario',methods=['GET','POST'])
def RegistroUsuario():
    formulario=FormularioRegistro(meta={ 'csrf':False})#quitamos el token para poder hacer la peticion sin problema mas adelan lo pondremos el token sirve para protegernos de los ataques del exterior
    
    if formulario.validate_on_submit():#Es par verficar si dio submit al boton o si es una peticion post
       #hacemos un apeticion de usuario si existe y con query .filter_by pedimos la verificacion con parametros o campors
       #que este dnetro dela base dedatos y first que solo nos entregue el primer nombre   
      usuarioExiste=Usuarios.query.filter_by(nombre=formulario.nombreUsuario.data).first()
      if usuarioExiste :
            flash('Este Usuario ya existe registre otro','danger')
      else:
             #con data obtenemos el valor dentro del input conmo un value en javascript
            u=Usuarios(formulario.nombreUsuario.data,formulario.password.data)
            db.session.add(u)
            db.session.commit()
            flash('Usuario creado con exito!!')
            return redirect(url_for('usuario.RegistroUsuario'))
    if formulario.errors:
          flash(formulario.errors,'danger')#de pasamos los errores si hay alguno dange es para decir que es un error lo muestra asi 
       
    #print(get_flashed_messages())#Obtemos todos los mensajes hechos con el metodo flash
    return render_template('usuario/crearUsuario.html',formulario=formulario)


@usuario.route('/Login',methods=['GET','POST'])
def Login():
    formulario=FormularioLogin(meta={ 'csrf':False})#quitamos el token para poder hacer la peticion sin problema mas adelan lo pondremos el token sirve para protegernos de los ataques del exterior
    
    if formulario.validate_on_submit():#Es par verficar si dio submit al boton o si es una peticion post
       #hacemos un apeticion de usuario si existe y con query .filter_by pedimos la verificacion con parametros o campors
       #que este dnetro dela base dedatos y first que solo nos entregue el primer nombre   
      usuarioExiste=Usuarios.query.filter_by(nombre=formulario.nombreUsuario.data).first()
      #Verificamo si el usuario existe y si el password es correcto para esso usamos lafuncion de check
      #paara verificar ya que el password esta encryptado
      #Debemos primero llamar al usuario que vamoss a revisar sus datos y despues usar el check-password
      if usuarioExiste and usuarioExiste.check_password(formulario.password.data):
            #session es un metodo de flask es para guardar los valores y poder usarlo despues como las cookies
            session['nombre']=usuarioExiste.nombre
            session['rol']=usuarioExiste.rol.value#usamos el value para obtener el valor por que no podemos enviar en string
            session['id']=usuarioExiste.id
            flash('Bienvenido de Nuevo'+usuarioExiste.nombre)
            return redirect(url_for('producto.Inicio'))
            
           
      else:
             flash('Incorrecto el nombre de Usuario o Password','danger')
       
     
    if formulario.errors:
          flash(formulario.errors,'danger')#de pasamos los errores si hay alguno dange es para decir que es un error lo muestra asi 
       
    #print(get_flashed_messages())#Obtemos todos los mensajes hechos con el metodo flash
    return render_template('usuario/login.html',formulario=formulario)


@usuario.route('/cerrarSesion')
def CerrarSession():
      #sesssion pop es para eliminar la session o la cokkies que tenemos registradaos
      
      session.pop('nombre')
      session.pop('rol')
      session.pop('id')
      return redirect(url_for('usuario.Login'))



