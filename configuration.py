class BaseConfig(object):
    'Base configuracion'
    SECRET_KEY = 'Key'
    DEBUG = True
    TESTING = False
    #WTF_CSRF_TIME_LIMIT =10 #ponemos el tiempo limite del token que expire
    RECAPTCHA_PUBLIC_KEY='6LffHtEUAAAAAI_KcKj6Au3R-bwhqRhPGe-WhHq_'
    RECAPTCHA_PRIVATE_KEY='6LffHtEUAAAAAJdHhV9e8yLOSB12rm8WW8CMxN7X'
    #dohttps://flask-wtf.readthedocs.io/en/stable/config/ de wtform
class ProduccionConfig(BaseConfig):
    'Produccion configuracion'
    DEBUG = False
class DesarrolloConfig(BaseConfig):
    'Desarrollo configuracion'
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'Desarrollo key'#llave secreta para el token
    #configuracion para el mail-flask 
    MAIL_SUPPRESS_SEND=False#es para activar los envios de correo aunque estemos en prueba o testinen true
    MAIL_SERVER='smtp.mailtrap.io'
    MAIL_PORT= 2525
    MAIL_USERNAME = '59d3d4679c1e52'
    MAIL_PASSWORD = '2a5e7643382e12'
    MAIL_DEFAULT_SENDER :"pruebaPython@gmail.com"
    MAIL_USE_TLS= True
    MAIL_USE_SSL = False
    
    
    
    #documentacion de google Recaptcha con flask https://flask-wtf.readthedocs.io/en/stable/