# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 12:39:44 2019

@author: Krishna, Abhigna, Lucy
"""
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import redirect

app = Flask(__name__)
db_file = "sqlite:///job.db"

app.config["SQLALCHEMY_DATABASE_URI"] = db_file
db = SQLAlchemy(app);

#Database model for Jobs
class Jobs(db.Model):
    ids = db.Column(db.Integer,
          primary_key=True)
    
    name = db.Column(db.String(80), 
           nullable=False,
           unique=True)
    
    author = db.Column(db.String(80), 
           nullable=False)
    
    year = db.Column(db.Integer,
           nullable=False)
    
    rating = db.Column(db.Integer,
           nullable=False)
    
    def __repr__(self):
        return "<Name: {}>".format(self.name)
    
db.create_all() #Creates DB Tables

@app.route("/", methods=["GET", "POST"])#Main
def home():
    try:
        jobSts = Jobs.query.limit(50).all()
    except:
        print("Error in reading the Job Names!")
    return render_template("home.html", jobSts=jobSts)

@app.route("/add", methods=["GET", "POST"])
def add(): #Adds the Job Details
    try:
        if request.form:
            names = Jobs(name=request.form.get("addname"), author="krishna", year=2020, rating=5)
            db.session.add(names)
            db.session.commit()
    except:
        print("Error in adding the Name!")
    return redirect("/")

@app.route("/delete/<title>", methods=["GET", "POST"])
def delete(title): #Deletes Job Details
    try:
        job = Jobs.query.filter_by(name=title).first()
        db.session.delete(job)
        db.session.commit()
    except:
        print("Error in deleting the Name!")
    return redirect("/")

@app.route("/edit", methods=["GET", "POST"])
def edit(): #Edits or updates the Job Details
    try:
        if request.form:
                newname = request.form.get("newtitle")
                oldname = request.form.get("oldtitle")
                job = Jobs.query.filter_by(name = oldname).first()
                job.name = newname
                db.session.commit()
    except:
        print("Error in editing the Job Name!")
    return redirect("/")

@app.route("/search", methods=["GET", "POST"])
def search(): #Search the Job Details
    try:
        if request.form:
            searchname = request.form.get("searchname")
            jobSts = Jobs.query.filter_by(name=searchname).limit(50).all()
    except:
        print("Error in searching the Job Name!")
    return render_template("home.html", jobSts=jobSts)
       
if __name__ == "__main__" :
    app.run(debug=True) # Runs the main class