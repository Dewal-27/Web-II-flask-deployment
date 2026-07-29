from flask import Flask,render_template, redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/root'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(150),nullable=False)
    status=db.Column(db.Integer, nullable=False)

class Posts(db.model):
    __tablename__='posts'
    id=db.Column(db.Integer,primary_key=True)
    heading=db.Column(db.String(400),nullable=False)
    sub_heading=db.Column(db.String(250),nullable=False)
    posted_date=db.Column(db.datetime,default=datetime.utcnow)
    post_by=db.Column(db.Integer,db.ForeignKey('user_id'))
    description=db.Column9(db.Text)
    status=db.Column(db.Integer)

    user=db.relationship('Users',back_populates='posts')

@app.route('/')
def home():
    #user=Users.query.all() #this is for showing all active and inacive status
    #user=Users.query.limit(3).all()#display first 3 data
    q='w'
    users=Users.query.filter(Users.username.like(f"%{q}%")).all()#used for search
    #user=Users.query.offset(3).all()# display except first 3 data
    #users=Users.query.filter(Users.status==1).order_by(Users.username.desc()).all()#filter by ststus, 
    #filter order by username in decsending order
    return render_template('index.html',users=users)
    '''
    try:
        #Correct usage of raw SQL
        db.session.execute(text('SELECT 1'))
        return "MySQL Connection Sucessful!"
    except Exception as e:
        return f"Connection Failed: {str(e)}"
    '''
@app.route('/adduser',methods=['GET','POST'])
def adduser():
    if request.method=='POST':
        user=Users(
            username=request.form['username'],
            password=request.form['password'],
            status=request.form['status']
        )
        db.session.add(user)
        db.session.commit()        
        return redirect("/")
    return render_template('adduser.html')

@app.route('/deleteUser')
def deleteUser():
    user=Users
    db.session.delete(user)

@app.route('/updateuser/<int:id>', methods=['GET','POST'])
def updateuser(id):
    users=Users.query.get(id)
    if request.method=="POST":
        users.username=request.form['username']
        users.password=request.form['password']
        db.session.commit()
        return redirect('/')
    return render_template('updateUser.html', user=users)

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
