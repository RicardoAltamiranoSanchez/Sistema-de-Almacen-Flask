from flask import Blueprint,render_template,request,redirect,url_for,flash,get_flashed_messages,session
from werkzeug.exceptions import abort
from my_app.DB.database import db
from sqlalchemy.sql.expression import not_,or_ #importamos elnot y el or
from my_app.models.Usuario.modelsUsuario import Usuarios,FormularioLogin,FormularioRegistro
#importaciones de flask_login
from flask_login import  login_user,logout_user,current_user,login_required
#Importamos este metodo por que la importacion de rlask-login esta ene el init
from my_app import login_manager

Fusuario=Blueprint('Fusuario',__name__)#pasamos el nombre de la aplicacion en el __name__ el primer parametro es como lo vamos a importar como asiganrla el nombre a un variable
#hacemos la funcion apra el login user
@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(user_id)
    

   
#Formulario
@Fusuario.route('/RegistroUsuario',methods=['GET','POST'])
def RegistroUsuario():
    formulario=FormularioRegistro()#(meta={ 'csrf':False})#quitamos el token para poder hacer la peticion sin problema mas adelan lo pondremos el token sirve para protegernos de los ataques del exterior
    
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


@Fusuario.route('/Login',methods=['GET','POST'])
def Login():
      #Es un  metod de flask_login dice si el usairo ya esta autenticatdo es como usar la s cookies te la la informacion del usaurio autehnticado
    if current_user.is_authenticated:
            flash('El usuario ya esta autenticado ')
            return redirect(url_for('producto.Inicio'))
            
    formulario=FormularioLogin()#(meta={ 'csrf':False})#quitamos el token para poder hacer la peticion sin problema mas adelan lo pondremos el token sirve para protegernos de los ataques del exterior
    
    if formulario.validate_on_submit():#Es par verficar si dio submit al boton o si es una peticion post
       #hacemos un apeticion de usuario si existe y con query .filter_by pedimos la verificacion con parametros o campors
       #que este dnetro dela base dedatos y first que solo nos entregue el primer nombre   
      usuarioExiste=Usuarios.query.filter_by(nombre=formulario.nombreUsuario.data).first()
      #Verificamo si el usuario existe y si el password es correcto para esso usamos lafuncion de check
      #paara verificar ya que el password esta encryptado
      #Debemos primero llamar al usuario que vamoss a revisar sus datos y despues usar el check-password
      if usuarioExiste and usuarioExiste.check_password(formulario.password.data):
            #ya que utilizamos el falsk login y lo verificamos usamos la funcion de login_user que hicimos al inicio
            login_user(usuarioExiste)#el get_id no de be ponerse properyty por que marcar erro de str
            flash('Bienvenido de Nuevo'+usuarioExiste.nombre)
            next=request.form['nextLogin']#obtenemos el valor de la url que es el next
            # if not is_safe_url(next):#vemos si es segura la url o que nos mande un abort 
            #       return abort(400)
                  #nos direcciona a una de las dos con or
            return redirect(next or url_for('producto.Inicio'))
            
           
      else:
             flash('Incorrecto el nombre de Usuario o Password','danger')
       
     
    if formulario.errors:
          flash(formulario.errors,'danger')#de pasamos los errores si hay alguno dange es para decir que es un error lo muestra asi 
       
    #print(get_flashed_messages())#Obtemos todos los mensajes hechos con el metodo flash
    return render_template('usuario/login.html',formulario=formulario)


@Fusuario.route('/cerrarSesion')
def CerrarSession():
      #para cerrar la senccion en  metodo de flask_login
      logout_user()
      return redirect(url_for('Fusuario.Login'))


#Aqui usamos los decorador de flask_login si no esta authentiado no puede acceder a ella
@Fusuario.route('/Protegida')
#Esta la ponemos ya qu e un metodo que sirve que si esta autehnticado pueda hacer ala vista es para proteger la vista
@login_required
def Protegido():
      return 'Vista que solo los autenticados pueden ver'
