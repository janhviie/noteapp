from flask import Flask, render_template, url_for, redirect, session, request, flash
from flask import jsonify
from flask_marshmallow import Marshmallow
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SECRET_KEY']='secret'

app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://jstdnmclztzjwh:600b13470d5189ebc80ee6e364668a05dc230cfb4631849ba3ddaabc79f83b19@ec2-18-209-187-54.compute-1.amazonaws.com:5432/damvep52h8rubp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
ma=Marshmallow(app)


class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(25), unique=True, nullable=False)
    password=db.Column(db.String(20), nullable=False)
    notes=db.relationship('Note', backref='owner')

class Note(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(25), nullable=False)
    note1=db.Column(db.Text())
    title=db.Column(db.Text())
    owner_id=db.Column(db.Integer, db.ForeignKey('user.id'))

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=User

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=Note


def invalid_credentials(form, field):
    username_entered=form.username.data
    password_entered=field.data
    # check if username exists
    user_obj= User.query.filter_by(username=username_entered).first()
    if user_obj is None:
        raise ValidationError("Username or Password is incorrect")
    elif password_entered != user_obj.password:
        raise ValidationError("Username or Password is incorrect")

class SignupForm(FlaskForm):
    username=StringField('username', validators=[InputRequired(message="Username required"), Length(min=4, max=15)])
    password=PasswordField('password', validators=[InputRequired(message="Password required"), Length(min=6, max=80)])
    confirm_pswd=PasswordField('password',validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])
    submit_button=SubmitField('Sign Up')

    def validate_username(self, username):
        user_obj= User.query.filter_by(username=username.data).first()
        if user_obj:
            raise ValidationError("Username already exists")

class loginForm(FlaskForm):
    username=StringField('username', validators=[InputRequired(message="Username required")])
    password=PasswordField('password', validators=[InputRequired(message="Password required"), invalid_credentials])
    submit_button=SubmitField('Log in')


@app.route('/', methods=['GET', 'POST'])
def signup():
    session["login"]=None
    session["note"]=None
    form=SignupForm()

    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        user=User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash("User created")
    return render_template('signup.html',form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form1=loginForm()
    if form1.validate_on_submit():
        user_obj=User.query.filter_by(username=form1.username.data).first()
        user_schema=UserSchema()
        output=user_schema.dump(user_obj)

        note_obj=Note.query.filter_by(username=form1.username.data).all()
        note_schema=NoteSchema(many=True)
        npoutput=note_schema.dump(note_obj)

        session["output"]=output
        session["notes"]=npoutput
        session["login"]='success'
        session["name"]=form1.username.data

        return redirect(url_for('user'))
    else:
        session["login"]=None
        session["note"]=None

    return render_template('login.html', form1=form1)



@app.route('/user', methods=['GET', 'POST'])
def user():
    if session["login"]== None:
        session["login"]=None
        flash("Not logged in!")
        return redirect(url_for('login'))



    if request.form:
        title=Note(username=session["name"],note1=request.form.get("note"), title=request.form.get("title"))
        db.session.add(title)
        db.session.commit()
    notes = Note.query.filter_by(username=session["name"]).all()
    return render_template("home.html", notes=notes)



@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")

    newnote = request.form.get("newnote")
    oldnote = request.form.get("oldnote")
    note = Note.query.filter_by(title=oldtitle, note1=oldnote).first()
    note.title = newtitle
    note.note1= newnote
    db.session.commit()
    return redirect("/user")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    note1=request.form.get('note')
    note = Note.query.filter_by(title=title, note1=note1).first()
    db.session.delete(note)
    db.session.commit()
    return redirect("/user")

if __name__=='__main__':

    app.run(debug=True)
