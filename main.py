from flask import Flask,render_template,request,redirect,url_for,flash,session


app = Flask(__name__)
app.secret_key="mykey1234567"


@app.route('/')
def home():
    name = "Dewal "
    isValid=True
    return render_template('index.html',name=name,isvalid=True)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    contactDetails={
        "ram":{"email":"info@abc.com","phone":"9843795345"},
        "shyam":{"email":"info@abc.com","phone":"9843795345"}
    }
    return render_template('contact.html',details=contactDetails)

@app.route('/login',methods=['POST','GET'])
def login():
    user='admin'
    password='dwl#4321'
    if request.method=='POST':
        username = request.form['username']
        pwd = request.form['password']

        if user==username and pwd==password:
            session['user']=username #setting session user
            session['email']= 'abc@gmail.com'
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html')
    else:
        return redirect('/login')
    
@app.route('/signup', methods=['POST','GET'])
def signup():
    errors=[]
    if request.method == "POST":
        #username=request.form['username']#data aayena vane error dinxa
        username=request.form.get('username').strip() #yesma data aayena vane null dinxa

        password=request.form['password'].strip()
        email=request.form['email'].strip()
        if not username:
            errors.append("Username is required.")
        if not password:
            errors.append("Password is required.")
        elif len(password)<8 :
            errors.append("Password should be 8 or more characters.")
        if not email:
            errors.append("Email is required.")
        elif "@" not in email:
            errors.append("Input valid email.")
        if not errors:
            flash("LOgin Sucessfully")
            #return f" Username: {username} Password: {password} Email: {email}"    
            return redirect(url_for('login'))
    return render_template('signup.html', errors=errors)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__=="__main__":
    app.run(debug=True)