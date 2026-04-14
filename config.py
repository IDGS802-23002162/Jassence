class Config(object):
    # Pega aquí el primer código que generaste en la consola
    SECRET_KEY = 'a6a829e46805dc91df70860e8a1c340c9e1c37ba94d7c5368dc3e94db12cec5b' 
    SESSION_COOKIE_SECURE = False

    # Configuración obligatoria para Flask-Security con Bcrypt
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = '6e47d58074bd4b614a3ceca9628941a20484f96c92f924abb315b2715f389ae6' 

    # LOGIN
    SECURITY_LOGIN_USER_TEMPLATE = 'modulos_front/seguridad/login.html'
    SECURITY_AUTO_LOGIN_AFTER_REGISTER = False
    SECURITY_POST_LOGIN_VIEW = '/check-role'
    

    # REGISTER
    SECURITY_REGISTERABLE = True 
    SECURITY_REGISTER_USER_TEMPLATE = 'modulos_front/seguridad/registrar.html'
    SECURITY_POST_REGISTER_VIEW = '/login'
    SECURITY_POST_LOGOUT_VIEW = '/'

    # ==========================================
    # TRADUCCIONES DE MENSAJES (Flask-Security)
    # ==========================================
    SECURITY_MSG_USER_DOES_NOT_EXIST = ("Usuario o contraseña incorrectos", "error")
    SECURITY_MSG_INVALID_PASSWORD = ("Usuario o contraseña incorrectos", "error")
    SECURITY_MSG_PASSWORD_NOT_SET = ("Usuario o contraseña incorrectos", "error")
    
    # Errores de Registro
    SECURITY_MSG_EMAIL_ALREADY_ASSOCIATED = ("Este correo ya está registrado en Jassence", "error")
    
    # Errores de Acceso
    SECURITY_MSG_LOGIN = ("Por favor, inicia sesión para acceder a esta sección", "info")
    SECURITY_MSG_UNAUTHORIZED = ("No tienes permisos para ver esta página", "error")
    
    # Errores de validación de campos (Si no usas custom forms, estos ayudan)
    SECURITY_MSG_PASSWORD_MISMATCH = ("Las contraseñas no coinciden", "error")
    SECURITY_MSG_PASSWORD_INVALID_LENGTH = ("La contraseña debe tener al menos 8 caracteres", "error")

    # ==========================================
    # CONFIGURACIÓN DE CORREO Y 2FA
    # ==========================================
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'jassencemail@gmail.com' # Pon tu correo real aquí
    MAIL_PASSWORD = 'xtigliyhujoqmylz' # La contraseña de aplicación
    MAIL_DEFAULT_SENDER = 'jassencemail@gmail.com'

    # Banderas del 2FA
    SECURITY_TWO_FACTOR = True
    SECURITY_TWO_FACTOR_REQUIRED = True
    SECURITY_TWO_FACTOR_ENABLE_METHODS = ['email'] 
    SECURITY_TWO_FACTOR_ALWAYS_VALIDATE = True
    SECURITY_TWO_FACTOR_VERIFY_CODE_TEMPLATE = 'modulos_front/seguridad/verificar_2fa.html'
    SECURITY_TWO_FACTOR_SETUP_TEMPLATE = 'modulos_front/seguridad/setup_2fa.html'

    SECURITY_TOTP_SECRETS = {"1": "0e9302c2c754a48cdbbe112326ecaf789ccb7c52d967dc2f3bb496efb72736d2"} 
    SECURITY_TOTP_ISSUER = "Jassence"


    # ==========================================
    # CONFIGURACIÓN DE RECUPERACION CONTRASEÑA
    # ==========================================

    SECURITY_RECOVERABLE = True
    SECURITY_RESET_PASSWORD_WITHIN = "1 hours"
    SECURITY_EMAIL_SUBJECT_PASSWORD_RESET = "Cambio de contraseña Jassence"
    SECURITY_FORGOT_PASSWORD_TEMPLATE = 'modulos_front/seguridad/olvidar_password.html'
    SECURITY_RESET_PASSWORD_TEMPLATE = 'modulos_front/seguridad/resetear_password.html'

    
    # ==========================================
    # CONFIGURACIÓN DE TIMEOUT - APP.PY
    # ==========================================
    PERMANENT_SESSION_LIFETIME = 31536000 
    SESSION_REFRESH_EACH_REQUEST = True
    SECURITY_RECOV_REMEMBER_ME = True 
    SECURITY_REMEMBER_SALT = '8f92b7c4e1a0d3f2b6e5d9c8a7b1f0e492d3c5b7a1f8e9d2c6b4a0f1e2d3c4b5' 

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://jassence_app:jassence_password_$@127.0.0.1/jassencebd'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Operación diaria de Jassence: No usar root