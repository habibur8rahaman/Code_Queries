from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

file_path= os.path.abspath(os.getcwd())+"\queries.db"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


class Query(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        query = Query(title=title, desc=desc)
        db.session.add(query)
        db.session.commit()

    allqueries = Query.query.all()
    return render_template('index.html', allqueries=allqueries)

@app.route("/show")
def products():
    allqueries = Query.query.all()
    print(allqueries)
    return "<p>Products page</p>"

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        allqueries = Query.query.filter_by(sno=sno).first()
        allqueries.title = title
        allqueries.desc = desc
        db.session.add(allqueries)
        db.session.commit()
        return redirect("/")

    allqueries = Query.query.filter_by(sno=sno).first()
    return render_template('update.html', allqueries=allqueries)


@app.route("/delete/<int:sno>")
def delete(sno):
    allqueries = Query.query.filter_by(sno=sno).first()
    db.session.delete(allqueries)
    db.session.commit()
    return redirect("/")


@app.route("/comment/<int:sno>", methods=['GET', 'POST'])
def comment(sno):
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        allqueries = Query.query.filter_by(sno=sno).first()
        allqueries.title = title
        allqueries.desc = desc
        db.session.add(allqueries)
        db.session.commit()
        return redirect("/")

    allqueries = Query.query.filter_by(sno=sno).first()
    return render_template('comment.html', allqueries=allqueries)



if __name__ == "__main__":
    app.run(debug=True, port=8000)
