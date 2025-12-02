from Market import app,db
from flask import render_template,redirect,url_for, flash
from Market.models import Item,User
from Market.forms import RegisterForm,LoginForm

# print("hello")
@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')
@app.route('/about/<username>')
def about_page(username):
    return f'<h1>This is the about page of {username}'
@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html',items=items)

@app.route('/register',methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create=User(UserName=form.username.data,
                            email_address=form.email_address.data,
                            password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors !={}: #If there are not error from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}',category='danger')
            # pass
    return render_template('register.html', form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    form=LoginForm()
    return render_template('login.html',form=form)