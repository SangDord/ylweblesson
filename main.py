from flask import Flask, url_for, request

app = Flask(__name__)


@app.route('/')
def root():
    return "Миссия Колонизация Марса"


@app.route('/index')
def index():
    return "И на Марсе будут яблони цвести!"


@app.route('/promotion')
def promotion():
    promotion_text = ['Человечество вырастает из детства.',
                      'Человечеству мала одна планета.',
                      'Мы сделаем обитаемыми безжизненные пока планеты.',
                      'И начнем с Марса!',
                      'Присоединяйся!']
    return '</br>'.join(promotion_text)


@app.route('/image_mars')
def image_mars():
    return f'''<!DOCTYPE html>
                <html lang="en">
                    <head>
                        <meta charset="utf-8">
                        <title>Привет, Марс!</title>
                    </head>
                    <body>
                        <h1>Жди нас, Марс!</h1>
                        <figure>
                            <img src="{url_for('static', filename='img/mars.png')}">
                            <figcaption>
                                Вот она какая, красная планета.
                            </figcaption>
                        </figure>
                    </body>
                </html>'''
                

@app.route('/promotion_image')
def promotion_image():
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <title>Колонизация</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet"
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                    crossorigin="anonymous">
                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}">
                  </head>
                  <body>
                    <h1>Жди нас, Марс!</h1>
                    <img src="{url_for('static', filename='img/mars.png')}"
                        alt="Здесь Марс!" width="300">
                    <div class="alert alert-dark" role="alert">
                        <h2> Человечество вырастает из детства </h2>
                    </div>
                    <div class="alert alert-success" role="alert">
                        <h2> Человечеству мала одна планета. </h2>
                    </div>
                    <div class="alert alert-secondary" role="alert">
                        <h2> Мы сделаем обитаемыми безжизненные пока планеты. </h2>
                    </div>
                    <div class="alert alert-warning" role="alert">
                        <h2> И начнем с Марса! </h2>
                    </div>
                    <div class="alert alert-danger" role="alert">
                        <h2> Присоединяйся! </h2>
                    </div>
                  </body>
                </html>'''
                

@app.route('/astronaut_selection', methods=['POST', 'GET'])
def astronaut_selection():
    content = f'''
        <!DOCTYPE html>
        <html lang="en">
            <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
            crossorigin="anonymous">
            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
            <title>Отбор астронавтов</title>
            </head>
            <body>
            <div class="header">
                <h1>Анкета претендента</h1>
                <h3>на участие в миссии</h3>
            </div>
            <div>
                <form class="login_form" method="post" enctype="multipart/form-data">
                    <div class="form-group">
                        <input type="text" class="form-control" id="lastname" placeholder="Введите фамилию" name="lastname">
                        <input type="text" class="form-control" id="firstname" placeholder="Введите имя" name="firstname">
                    </div>
                    </br>
                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                    <div class="form-group">
                        <label>Какое у вас образование?</label>
                        <select class="form-control" id="edutypeSelect" name="edutype">
                            <option>Начальное общее</option>
                            <option>Основное общее</option>
                            <option>Среднее общее</option>
                            <option>Среднее профессиональное</option>
                            <option>Высшее образование I</option>
                            <option>Высшее образование II</option>
                            <option>Высшее образование III</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Какие у Вас есть профессии?</br></label>
                        <div class="form-check">
                            <input type="checkbox" class="form-check-input" name="profession" id="engineer-researcher" value="engineer-researcher">
                            <label for="engineer-researcher">Инженер-исследователь</label>
                        </div>
                        <div class="form-check">
                            <input type="checkbox" class="form-check-input" name="profession" id="engineer-builder" value="engineer-builder"/>
                            <label for="engineer-builder">Инженер-строитель</label>
                        </div>
                        <div class="form-check">
                            <input type="checkbox" class="form-check-input" name="profession" id="engineer-terraforming" value="engineer-terraforming"/>
                            <label for="engineer-terraforming">Инженер по терраформированию</label>
                        </div>
                        <div class="form-check">
                            <input type="checkbox" class="form-check-input" name="profession" id="cyber-engineer" value="cyber-engineer"/>
                            <label for="cyber-engineer">Кибер инженер</label>
                        </div>
                        <div class="form-check">
                            <input type="checkbox" class="form-check-input" name="profession" id="life-support-engineer" value="life-support-engineer"/>
                            <label for="life-support-engineer">Инженер жизнеобеспечения</label>
                        </div>
                        <div class="form-check">
                            <input type="checkbox" class="form-check-input" name="profession" id="meteorologist" value="meteorologist"/>
                            <label for="meteorologist">Метеоролог</label>
                        </div>
                        <div class="form-check">
                            <input type="checkbox" class="form-check-input" name="profession" id="astrogeologist" value="astrogeologist"/>
                            <label for="astrogeologist">Астрогеолог</label>
                        </div>
                        <div class="form-check">
                            <input type="checkbox" class="form-check-input" name="profession" id="glaciologist" value="glaciologist"/>
                            <label for="glaciologist">Гляциолог</label>
                        </div>
                        <div class="form-check">
                            <input type="checkbox" class="form-check-input" name="profession" id="pilot" value="pilot"/>
                            <label for="pilot">Пилот</label>
                        </div>                       
                        <div class="form-check">
                            <input type="checkbox" class="form-check-input" name="profession" id="navigator" value="navigator"/>
                            <label for="navigator">Штурман</label>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="form-check">Укажите пол</label>
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                            <label class="form-check-label" for="male">
                            Мужской
                            </label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                            <label class="form-check-label" for="female">
                            Женский
                            </label>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="about">Почему вы хотите принять участие в миссии?</label>
                        <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="photo">Приложите фотографию</label>
                        <input type="file" class="form-control-file" id="photo" name="file">
                    </div>
                    <div class="form-group form-check">
                        <input type="checkbox" class="form-check-input" id="acceptRules" name="ready">
                        <label class="form-check-label" for="acceptRules">Готовы остаться на Марсе?</label>
                    </div>
                    <button type="submit" class="btn btn-primary">Отправить</button>
                </form>
            </div>
            </body>
        </html>'''
    if request.method == 'GET':
        return content
    elif request.method == 'POST':
        data = {}
        for key in ['lastname', 'firstname', 'edutype', 'profession', 'sex', 'about', 'ready']:
            data[key] = request.form.get(key)
        data['file'] = request.files['file']
        print(data)
        return "<h1>Анкета отправлена!<h1>"


@app.route('/choice/<planet_name>')
def planet_choice(planet_name):
    planets = {'Марс': ['Это планета близка к земле;',
                        'На ней много необходимых ресурсов;',
                        'На ней есть вода и атмосфера;',
                        'На ней есть небольшое магнитное поле;',
                        'Наконец, она просто красива!']} #  можно добавить при необходимости ровно 5 причин
    alerts_color = ['alert-light', 'alert-success', 'alert-secondary','alert-warning', 'alert-danger']
    if planet_name in planets.keys():
        data = '\n'.join([f'<div class="alert {alerts_color[i]}" role="alert"><h3>{planets[planet_name][i]}</h3></div>'
                          for i in range(len(planets[planet_name]) % 6)])
        content = f'''
            <!doctype html>
            <html lang="en">
                <head>
                    <meta charset="utf-8">
                    <title>Колонизация</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet"
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                    crossorigin="anonymous">
                </head>
                <body>
                    <h1>Мое предложение: {planet_name}</h1>
                    {data}
                    </div>
                </body>
            </html>'''
        return content
    else:
        return f'Данных о планете {planet_name} пока нет!'


@app.route('/results/<nickname>/<int:level>/<float:rating>')
def result_selection(nickname, level: int, rating: float):
    content = f'''
        <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8">
                    <title>Колонизация</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet"
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                    crossorigin="anonymous">
                </head>
                <body>
                    <h1>Результаты отбора</h1>
                    <h2>Претендента на участие в миссии {nickname}:</h2>
                    <div class="alert alert-success" role="alert">
                        <h2>Поздравляем! Ваш рейтинг после {level} этапа отбора</h2>
                    </div>
                    <h3>составляет {rating}!</h3>
                    <div class="alert alert-warning" role="alert">
                        <h2>Желаем удачи!</h2>
                    </div>
                </body>
            </html>'''
    return content


if __name__ == "__main__":
    app.run(port=8080, host='127.0.0.1')
