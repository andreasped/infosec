from email import message
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FormField, TextAreaField, FileField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Regexp
from app import app, query_db

# defines all forms in the application, these will be instantiated by the template,
# and the routes.py will read the values of the fields
# TODO: Add validation, maybe use wtforms.validators??
# TODO: There was some important security feature that wtforms provides, but I don't remember what; implement it



class LoginForm(FlaskForm):
    username = StringField('Username', render_kw={'placeholder': 'Username'}, validators=[DataRequired()])
    password = PasswordField('Password', render_kw={'placeholder': 'Password'}, validators=[DataRequired()])
    remember_me = BooleanField('Remember me') # TODO: It would be nice to have this feature implemented, probably by using cookies
    submit = SubmitField('Sign In')

def is_username(form,field):
    user = field.data
    users = query_db("SELECT username from users WHERE username='{}'".format(user))
    if len(users) != 0:
        raise ValidationError('Username is taken')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', render_kw={'placeholder': 'First Name'}, validators=[DataRequired(), Length(min=2, max=20), Regexp("[A-Za-z]")])
    last_name = StringField('Last Name', render_kw={'placeholder': 'Last Name'}, validators=[DataRequired(), Length(min=2, max=20),Regexp("[A-Za-z]")])
    username = StringField('Username', render_kw={'placeholder': 'Username'}, validators=[DataRequired(), Length(min=2, max=20), is_username])
    password = PasswordField('Password', render_kw={'placeholder': 'Password'}, validators=[DataRequired(), Regexp("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", message = "Password must be 8 characters or longer, have a uppercase letter, a lowercase letter, at least one digit and at least one special character!")])
    confirm_password = PasswordField('Confirm Password', render_kw={'placeholder': 'Confirm Password'}, validators=[EqualTo('password', message='Passwords must match')])
    submit1 = SubmitField('Sign Up')
    


class IndexForm(FlaskForm):
    login = FormField(LoginForm)
    register = FormField(RegisterForm)

class PostForm(FlaskForm):
    content = TextAreaField('New Post', render_kw={'placeholder': 'What are you thinking about?'}, validators=[Length(max=200, message="Max 200 characters")])
    image = FileField('Image')
    submit = SubmitField('Post')

class CommentsForm(FlaskForm):
    comment = TextAreaField('New Comment', render_kw={'placeholder': 'What do you have to say?'}, validators=[Length(max=200, message="Max 200 characters")])
    submit = SubmitField('Comment')

class FriendsForm(FlaskForm):
    username = StringField('Friend\'s username', render_kw={'placeholder': 'Username'})
    submit = SubmitField('Add Friend')

class ProfileForm(FlaskForm):
    education = StringField('Education', render_kw={'placeholder': 'Highest education'}, validators=[Regexp("[A-Za-z]", message="This field can only contain letters!"), Length(max=100, message="Max 100 characters")])
    employment = StringField('Employment', render_kw={'placeholder': 'Current employment'}, validators=[Regexp("[A-Za-z]"), Length(max=100, message="Max 100 characters")])
    music = StringField('Favorite song', render_kw={'placeholder': 'Favorite song'},  validators=[Regexp("[\w\[\]`!@#$%\^&*()={}:;<>+'-]*"), Length(max=100, message="Max 100 characters")])
    movie = StringField('Favorite movie', render_kw={'placeholder': 'Favorite movie'},  validators=[Regexp("[\w\[\]`!@#$%\^&*()={}:;<>+'-]*"), Length(max=100, message="Max 100 characters")])
    nationality = StringField('Nationality', render_kw={'placeholder': 'Your nationality'},  validators=[Regexp("[A-Za-z]"), Length(max=100, message="Max 100 characters")])
    birthday = DateField('Birthday')
    submit = SubmitField('Update Profile')
