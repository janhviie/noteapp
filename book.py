from flask import Flask
from flask import render_template , url_for, redirect, session, request, flash


from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SECRET_KEY']='secret'


app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:jp101@localhost/appnew'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Book(db.Model):
    title=db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
def __repr__(self):
        return "<Title: {}>".format(self.title)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.form:
        book=Book(title=request.form.get("title"))
        db.session.add(book)
        db.session.commit()
    books = Book.query.all()
    return render_template("home.html", books=books)

@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    book = Book.query.filter_by(title=oldtitle).first()
    book.title = newtitle
    db.session.commit()
    return redirect("/home")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/home")
if __name__=='__main__':

    app.run(debug=True)
