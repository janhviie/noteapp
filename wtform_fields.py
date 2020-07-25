# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
#
#
#
# def invalid_credentials(form, field):
#     username_entered=form.username.data
#     password_entered=field.data
#     # check if username exists
#     user_obj= User.query.filter_by(username=username_entered).first()
#     if user_obj is None:
#         raise ValidationError("Username or Password is incorrect")
#     elif password_entered != user_obj.password:
#         raise ValidationError("Username or Password is incorrect")
#
# class SignupForm(FlaskForm):
#     username=StringField('username', validators=[InputRequired(message="Username required"), Length(min=4, max=15)])
#     password=PasswordField('password', validators=[InputRequired(message="Password required"), Length(min=4, max=80)])
#     confirm_pswd=PasswordField('password',validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])
#     submit_button=SubmitField('Sign Up')
#
#     def validate_username(self, username):
#         user_obj= User.query.filter_by(username=username.data).first()
#         if user_obj:
#             raise ValidationError("Username already exists")
#
# class loginForm(FlaskForm):
#     username=StringField('username', validators=[InputRequired(message="Username required")])
#     password=PasswordField('password', validators=[InputRequired(message="Password required"), invalid_credentials])
#     submit_button=SubmitField('Log in')
