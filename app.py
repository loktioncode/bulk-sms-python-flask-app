from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_mail import Mail, Message
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

#send email to admin for join request
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'elishabere5@gmail.com'
app.config['MAIL_PASSWORD'] = 'CATHRINE1995'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)


#creating my tabes in db
class Contacts(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    cell = Column(Integer)
    email = Column(String(50))
    org = Column(Integer)

class User(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    cell = Column(Integer)
    email = Column(String(50))
    state = Column(Boolean)
    password = Column(String(50))




@app.route('/', methods=['GET'])
def home():

    return render_template('login.html')


@app.route('/admin', methods=['GET'])
def admin():

    users = User.query.all()

    return render_template('admin.html',users=users)


@app.route('/index', methods=['GET'])
def menu():

    users = User.query.all()

    return render_template('index.html',users=users)



@app.route('/', methods=['POST'])
def login():

    admins = {'sudo@app.com':'Bere'}

    email = request.form.get('email')
    passwd = request.form.get('password')

    #admins = User.query.filter_by(name=name).first()
    users = User.query.all()

    if email in admins:                             #chex to see id u are admin
        if admins[email]== passwd:                   #chex if login email in admin == pwd entered
            return redirect(url_for('admin'))

    elif email not in admins :
        pass

    for user in users:
        admins[user.email] = user.password 
        
    if email in admins:                             #chex to see if email input == one in list admins
        if admins[email]== passwd:                   #chex if login email in admin == pwd entered
            return redirect(url_for('menu'))
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
    reciep = request.form.get('tel')
    email = request.form.get('email')
    belongs_to  = request.form.get('group')

    newRecipient = Contacts(name=name,cell=reciep,email=email, org=belongs_to) 
    db.session.add(newRecipient)
    db.session.commit()
    return render_template('added.html')

@app.route('/', methods=['POST'])
def contact_us():
    msg = Message('Hello', sender = 'elishabere5@gmail.com', recipients = ['elishabere4@gmail.com'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)



    return f'sent'

@app.route('/newuser', methods=['POST'])
def add_user():
    #adding system users
    name = request.form.get('name')
    email = request.form.get('email')
    state = False
    cell = request.form.get('tel')
    password = request.form.get('password')

    newUser = User(name=name, cell=cell, email=email, state=state, password=password) 
    db.session.add(newUser)
    db.session.commit()

    return redirect(url_for('menu'))





if __name__ == "__main__":
    app.run(debug=True)
    