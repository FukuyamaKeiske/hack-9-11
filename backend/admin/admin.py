from flask import Flask, redirect, url_for, render_template, request
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.pymongo import ModelView
from wtforms import form, fields
from db_lib import db_client
import os

app = Flask(__name__, template_folder=os.path.abspath('templates'))
app.secret_key = 'supersecretkey'

# Определение классов форм для создания и редактирования записей


class UserForm(form.Form):
    username = fields.StringField('Username')
    phone_number = fields.StringField('Phone Number')
    role = fields.StringField('Role')
    created_at = fields.DateTimeField('Created At')
    updated_at = fields.DateTimeField('Updated At')


class BusinessForm(form.Form):
    name = fields.StringField('Name')
    created_at = fields.DateTimeField('Created At')
    updated_at = fields.DateTimeField('Updated At')


class TaskForm(form.Form):
    title = fields.StringField('Title')
    description = fields.TextAreaField('Description')
    role = fields.StringField('Role')
    due_date = fields.DateTimeField('Due Date')
    status = fields.StringField('Status')
    created_at = fields.DateTimeField('Created At')
    updated_at = fields.DateTimeField('Updated At')

# Определение классов ModelView с явным указанием полей и форм


class UserView(ModelView):
    column_list = ('username', 'phone_number',
                   'role', 'created_at', 'updated_at')
    form = UserForm


class BusinessView(ModelView):
    column_list = ('name', 'created_at', 'updated_at')
    form = BusinessForm


class TaskView(ModelView):
    column_list = ('title', 'description', 'role', 'due_date',
                   'status', 'created_at', 'updated_at')
    form = TaskForm

# Класс для главной страницы админ-панели с поддержкой аутентификации


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not self.is_accessible():
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login', methods=('GET', 'POST'))
    def login_view(self):
        print(1)
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            # Здесь добавьте логику проверки пользователя
            if username == 'admin' and password == 'password':
                return redirect(url_for('.index'))
        return render_template('login.html')

    def is_accessible(self):
        # Здесь добавьте логику проверки доступа
        return True


admin = Admin(app, name='Construction Admin', template_mode='bootstrap3', index_view=MyAdminIndexView())
# Добавление моделей в админ-панель
admin.add_view(UserView(db_client.users_collection, 'Users'))
admin.add_view(BusinessView(db_client.businesses_collection, 'Businesses'))
admin.add_view(TaskView(db_client.tasks_collection, 'Tasks'))

