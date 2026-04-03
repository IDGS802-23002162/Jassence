from flask_security import RegisterForm, LoginForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


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