from flask_security import RegisterForm, LoginForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from flask_wtf import FlaskForm


# UTILIZACION DE SUPER PARA NO SUSTITUIR FLASK-SECURITY
# MODULO SEGURIDAD --------------------------------------
class CustomRegisterForm(RegisterForm):
    def __init__(self, *args, **kwargs):
        super(CustomRegisterForm, self).__init__(*args, **kwargs)
        # Personalizamos las etiquetas (labels)
        self.email.label.text = "Correo electrónico para Jassence"
        self.password.label.text = "Crea tu contraseña"
        self.password_confirm.label.text = "Confirma tu contraseña"
        # Personalizamos los mensajes de error o placeholders si quieres
        self.email.render_kw = {"placeholder": "ejemplo@correo.com"}

class CustomLoginForm(LoginForm):
    
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.email.label.text = "Correo electrónico"
        self.password.label.text = "Contraseña"
        self.email.description = "El correo es necesario para iniciar sesión."



# --------------------------------------------------------------------------------

class PerfilValidacionForm(FlaskForm):
    nombre = StringField(validators=[DataRequired(), Length(min=2, max=50)])
    apellidos = StringField(validators=[DataRequired(), Length(min=2, max=50)])
    # Regex para exactamente 10 dígitos (ajusta según tu país)
    telefono = StringField(validators=[
        DataRequired(), 
        Regexp(r'^\d{10}$', message="El teléfono debe tener 10 dígitos.")
    ])
    correo = StringField(validators=[DataRequired(), Email()])