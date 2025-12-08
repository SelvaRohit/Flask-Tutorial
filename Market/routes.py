from Market import app,db,login_manager
from flask import render_template,redirect,url_for, flash, request
from Market.models import Item,User
from Market.forms import RegisterForm,LoginForm,PurchaseItemForm
from flask_login import login_user, logout_user, login_required, current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# print("hello")
@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')
@app.route('/about/<username>')
def about_page(username):
    return f'<h1>This is the about page of {username}'
@app.route('/market',methods=['GET','POST'])
@login_required
def market_page():
    purchase_form=PurchaseItemForm()
    if request.method == 'POST':
        purchased_item=request.form.get('purchased_item')
        p_item_object=Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations you have purchased the {p_item_object.name} for {p_item_object.price}$",category='success')
            else:
                flash(f"Unfortunately, you don't have money to buy {p_item_object.name}",category='danger')
            return redirect(url_for('market_page'))
    if request.method =='GET':
        items = Item.query.filter_by(owner=None)
        print(items)
        return render_template('market.html',items=items,purchase_form=purchase_form)

@app.route('/register',methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create=User(UserName=form.username.data,
                            email_address=form.email_address.data,
                            password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create) #sets the session, current user and remembers.
        flash(f'Account created Successfully! You are logged in as: {user_to_create.UserName}',category='success')
        

        return redirect(url_for('market_page'))
    if form.errors !={}: #If there are not error from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}',category='danger')
            # pass
    return render_template('register.html', form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(UserName=form.username.data).first()
        # The first() method is used to get the object of the User from the database
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user) #sets the session, current user and remembers.
            flash(f'Success! You are logged in as: {attempted_user.UserName}',category='success')
            return redirect(url_for('market_page'))
        else:
            flash(f'Username/Password is incorrect! Please try again',category='danger')

    return render_template('login.html',form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'You have been logged out!!!',category='info')
    return redirect(url_for('home_page'))