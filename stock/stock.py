import requests
import datetime as dt
import json
from flask import Flask ,request ,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///person.db'

db =SQLAlchemy(app)

stock_url =''
intra_day =''

class Person(db.Model):
    id =db.Column(db.Integer ,primary_key=True)
    data =db.Column(db.String(50) ,nullable=False)

@app.route('/',methods=['GET' ,'POST']) 
def main():
    if request.method =='POST':

        quote = request.form.get('quote')
        f=0

        if quote:
            r =requests.get(stock_url.format(quote)).json()
            if 'Message' in r.keys():
                f=1
            else:
                person_obj =Person(data =str(r['data'][0]['price']))
                db.session.add(person_obj)
                db.session.commit()

    person = Person.query.all()
    stock_data=[]
    for i in person:
        stock_data.append(i.data)
    
    return render_template('index.html',stock_data=stock_data)
    
if __name__=='main':
    app.run()



