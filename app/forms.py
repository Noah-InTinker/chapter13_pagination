
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, \
    BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email,\
    EqualTo, ValidationError
from app.models import User

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Edit Profile')

    def __init__(self, original_username, *args, **kwargs) -> None:
        super(EditProfileForm, self).__init__(*args,**kwargs)
        self.original_username = original_username
        
    def validate_username(self, username):
        if self.username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first
            if user is not None:
                raise ValidationError('Please use a different username.')
    

class AddProductForm(FlaskForm):
    """Product Form"""
    product_name = StringField('Product Name', validators=[DataRequired(), Length(1, 63)])
    product_description = TextAreaField('Product Description', validators=[DataRequired()])
    stock_available = SelectField('Stock Available', choices=[
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)
    ])
    submit = SubmitField('Add Product')
    
 

class RegisterForm(FlaskForm):
    """Register Form"""
    username = StringField('Username', validators=[DataRequired(), Length(1, 63)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('Register')


    def validate_username(self, username):
        """Validate new user username"""
        user = User.query.filter_by(username.data).first
        if user is not None:
            raise ValidationError('Pleas use a different username.')

    def validate_email(self, email):
        """Validate new user email"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField('Username', validators=[DataRequired(), Length(1, 63)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')



class PostForm(FlaskForm):
    """Comment form"""
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Post')