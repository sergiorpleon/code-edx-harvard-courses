from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from app.forms import LoginForm, RegisterForm, UserForm
from app.models import User, Role
from app.helpers import requires_access_level
from flask_login import login_user, logout_user, login_required
from flask_login import current_user
from app import db
#from helpers import login_required

user_bp = Blueprint('user', __name__)


@user_bp.route('/users/<int:user_id>')
def user_detail(user_id):
    # Aquí iría la lógica para mostrar los detalles de un usuario
    return render_template('user_detail.html', user_id=user_id)




"""
    if form.validate_on_submit():
        name = form.name.data
        new_greeting = Greeting(name=name)
        db.session.add(new_greeting)
        db.session.commit()
        flash(f'¡Hola, {name}!')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)
"""

@user_bp.route('/login', methods=["GET", "POST"])
def login():
    """Log user in"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Successful login.', 'success')
            
            return redirect(request.args.get("next") or url_for("event.index"))
        else:
            flash('Incorrect email or password.', 'danger')
    else:
        print(form.errors)
    return render_template('login.html', form=form)


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('event.index'))


@user_bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('The email is already registered. Choose another.', 'warning')
            return redirect(url_for('user.register'))
        if User.query.filter_by(name=form.name.data).first():
            flash('The username is already registered. Choose another.', 'warning')
            return redirect(url_for('user.register'))
        
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        default_role = Role.query.first()
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password, id_role=default_role.id)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Successful registration. Now you can log in.', 'success')
        return redirect(url_for('user.login'))
    
    return render_template('register.html', form=form)


@user_bp.route('/users')
@requires_access_level('administrator')
@login_required
def list_users():
    users = User.query.all()  # Obtiene todos los eventos de la base de datos
    return render_template('users.html', users=users)  # Pasa la lista de eventos a la plantilla


@user_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@requires_access_level('administrator')
@login_required
def edit_user(user_id):
    # Get user by ID and load data into form
    user = User.query.get_or_404(user_id)  
    form = UserForm(obj=user)

    if form.validate_on_submit():
        if form.email.data != user.email and User.query.filter_by(email=form.email.data).first():
            flash('The email is already registered. Choose another.', 'warning')
            return redirect(url_for('user.register'))
        if form.name.data != user.name and User.query.filter_by(name=form.name.data).first():
            flash('The username is already registered. Choose another.', 'warning')
            return redirect(url_for('user.register'))

        # Update event attributes with form data
        user.name = form.name.data
        user.email = form.email.data
        user.id_role = form.role.data
        
        # Save changes to the database
        db.session.commit() 
        

        flash('User updated successfully.', 'success')
        return redirect(url_for('user.list_users'))  
    
    form.role.data = user.id_role

    return render_template('update_user.html', form=form)

@user_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@requires_access_level('administrator')
@login_required
def delete_user(user_id):
    if current_user.id == user_id:
        flash('You dont can delete yourself.', 'warning')
        return redirect(url_for('user.list_users'))
    
    # Get user by ID
    user = User.query.get_or_404(user_id)
    
    # Delete user of session and Save changes to the database
    db.session.delete(user)
    db.session.commit()

    flash('User successfully deleted.', 'success')
    return redirect(url_for('user.list_users')) 


@user_bp.route('/view_user/<int:user_id>')
@requires_access_level('administrator')
@login_required
def view_user(user_id):
    # Get user by ID
    user = User.query.get_or_404(user_id)
    
    return render_template('view_user.html', user=user)
