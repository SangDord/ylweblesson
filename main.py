from flask import Flask, render_template, redirect, flash
from loginform import LoginForm
from galeryform import GaleryForm
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ylweblesson_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/img/galery/extra'
app.config['GALERY_STORAGE'] = 'static/img/galery'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('base.html', title=title)


@app.route('/training/<prof>')
def training_prof(prof):
    return render_template('training_prof.html', prof=prof)


@app.route('/list_prof/<list>')
def list_prof(list):
    prof_list = ['инженер-исследователь',
                 'пилот',
                 'строитель',
                 'экзобиолог',
                 'врач',
                 'инженер по терраформарованию',
                 'климатолог',
                 'специалист по радиационной защите',
                 'астрогеолог',
                 'инженер жизнеобеспечения',
                 'метеоролог',
                 'оператор марсохода',
                 'киберинженер',
                 'штурман',
                 'пилот дронов']
    return render_template('list_prof.html', list=list, prof_list=prof_list)


@app.route('/answer')
@app.route('/auto_answer')
def auto_answer():
    params = {}
    params['title'] = 'Анкета'
    params['surname'] = input('Введите фамилию| ')
    params['name'] = input('Введите имя| ')
    params['education'] = input('Какое у вас образование?| ')
    params['profession'] = input('Какая у вас профессия?| ')
    params['sex'] = input('Ваш пол?| ')
    params['motivation'] = input('Ваша мотивация?| ')
    params['ready'] = input('Готовы ли вы остаться на Марсе?| (y/n) ').lower() == 'y'
    for k, v in params.items():
        if not v and k != 'ready':
            params[k] = 'None'
    return render_template('auto_answer.html', **params)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Аварийный доступ', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/distribution')
def distribution():
    astr_list = ['Ридли Скотт',
                 'Энди Уир',
                 'Марк Уотни',
                 'Венката Капур',
                 'Тедди Сандерс',
                 'Шон Бин']
    return render_template('distribution.html', astr_list=astr_list)


@app.route('/table/<sex>/<age>')
def table(sex, age):
    try:
        is_adult = int(age) >= 21
        if int(age) <= 0:
            raise ValueError
    except ValueError:
        is_adult = 'None'
    return render_template('table.html', sex=sex, is_adult=is_adult)


@app.route('/galery', methods=['GET', 'POST'])
def galery():
    form = GaleryForm()
    pics = [i for i in os.listdir(app.config['GALERY_STORAGE']) if i != 'extra']
    if form.validate_on_submit() and form.picture.data:
        if allowed_file(form.picture.data.filename):
            picname = secure_filename(form.picture.data.filename)
            picpath = os.path.join(app.config['UPLOAD_FOLDER'], picname)
            form.picture.data.save(picpath)
        else:
            print('flash')
            flash('Extension not allowed.', 'error')
    extra_pics = os.listdir(app.config['UPLOAD_FOLDER'])
    all_pics = pics + extra_pics
    return render_template('galery.html', title='Красная планета', form=form, 
                           pics=pics, extra_pics=extra_pics, all_pics=all_pics)
    
    
if __name__ == "__main__":
    app.run(port=8080, host='127.0.0.1')