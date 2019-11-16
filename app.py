from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import Column, Boolean, Integer, String
import http.client


app = Flask(__name__)

#tell app we in dev mode
app.config["DEBUG"] = True


#secret ket to encode wt token
app.config['SECRET KEY'] = 'beredevtestkey'
#CONNECTING TO A DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foo.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#creating my tabes in db
class Contacts(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    cell = Column(Integer)
    email = Column(String(50))


@app.route('/', methods=['GET'])
def home():

    return render_template('home.html')

@app.route('/menu', methods=['GET'])
def menu():

    return render_template('index.html')

@app.route('/', methods=['POST'])
def login():

    admins = { 'eli@bere.com':'Bere',
           'ashpen@sms.com':'6666',
           'bob@sms.com':'1592'}

    email = request.form.get('email')
    passwd = request.form.get('password')

    
    if email in admins:                               #chex to see if email input == one in list admins
        if admins[email]== passwd:                   #chex if login email in admin == pwd entered
            return render_template('index.html')
        elif admins[email] != passwd:
            #failed
            return render_template('failed.html')

    elif email not in admins :
        #failed func
        return render_template('failed.html')


@app.route('/send', methods=['POST']) #specifying endpoinTS
def sendmessage():

    message = request.form.get('message')
    reciep = request.form.get('reciever')
    org = request.form.get('org_name')

    my_list = message.split()
    final_message = "%20".join(my_list) #i%20%love%20you%20

    

    conn = http.client.HTTPConnection("api.msg91.com")

    conn.request("GET", "/api/sendhttp.php?sender={}&route=4&mobiles={}&authkey=206256AUdO3HxGi0h75ac5eb7a&encrypt=&country=27&message={}".format(org,reciep,final_message))

    #res = conn.getresponse()
    #data = res.read()

    #res = data.decode("utf-8")
    return render_template('sent.html')


@app.route('/bulk', methods=['POST']) #specifying endpoinTS
def bulksend():
    org_name = request.form.get('name')
    message = request.form.get('message')
    grup = request.form.get('group')

    my_list = message.split()
    final_message = "%20".join(my_list) #i%20%love%20you%20

    contacts = Contacts.query.all() #taking all rows in db

    if contacts:
        for contact in contacts:
            reciep = contact.cell
            conn = http.client.HTTPConnection("api.msg91.com")
            conn.request("GET", "/api/sendhttp.php?sender={}&route=4&mobiles={}&authkey=206256AUdO3HxGi0h75ac5eb7a&encrypt=&country=27&message={}".format(org_name,reciep,final_message))
        return render_template('sent.html')


@app.route('/add', methods=['POST']) #specifying endpoinTS
def add_reciep():

    name = request.form.get('name')
    reciep = request.form.get('reciever')
    email = request.form.get('email')

    newRecipient = Contacts(name=name,cell=reciep,email=email)
    db.session.add(newRecipient)
    db.session.commit()
    return render_template('added.html')


if __name__ == "__main__":
    app.run()
    db.create_all()