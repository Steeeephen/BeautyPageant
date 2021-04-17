from flask import Flask, render_template

import os

hints = [
  'hint1',
  'hint2',
  "hint3",
  'hint4',
  'hint5'
]

app = Flask(__name__, template_folder='templates', static_folder="static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# Home Page
@app.route('/')
def start():
  return render_template(
    'home.html', 
    text='Data Team Beauty Pageant', 
    # Show button
    show='visible', 
    gif='https://media3.giphy.com/media/3h3CIZJWcrlEjPwq1t/giphy.gif')


# Rules of the game
@app.route('/rules')
def rules():
  return render_template('rules.html')


# Start of round, showing the hint
@app.route('/round/<num>')
def round(num):
  if num == '6':
    return render_template(
      'home.html', 
      text='Thanks For Playing!', 
      show='invisible', 
      gif='https://media4.giphy.com/media/26tOZ42Mg6pbTUPHW/giphy.gif')
  rule = hints[int(num)-1]

  return render_template('round.html', rule=rule, num=num)


# Images of contestants
@app.route('/home/<num>')
def home(num):
  images_path = os.path.join(
    'static',
    f'round_{num}')

  images = os.listdir(images_path)

  links = {}
  for i, image in enumerate(images):
    image_name = image.split('.')[0].replace('_', ' ').title()

    # Spaces
    image = image.replace(' ', '%20')

    links[f'link{i}'] = os.path.join(
        '/static',
        f'round_{num}',
        image)

    links[f'name{i}'] = image_name
  links['round'] = int(num)+1
  
  return render_template('test.html', **links)


# Stops page from caching static images, otherwise the photos for each round may not get shown
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

app.run()