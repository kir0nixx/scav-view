from flask import Flask, render_template, url_for, request, redirect
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(32)

SCAV_DATABASE_FILE = 'data/scavs.json'

@app.get('/')
def home():

   return render_template('home.html')

@app.get('/view-all')
def view_all():
   scavs = get_all_scavs()

   return render_template('view-all.html', scavs=scavs)

@app.get('/view-id/<int:id>')
def view(id):
   
   scav_info = get_scav(id)

   return render_template('view-scav.html', scav_info=scav_info)

@app.get('/search')
def display_search():
   
   return render_template('search.html')

@app.post('/search')
def search():
   
   query = request.form.get('query', '')

   return redirect(url_for('search_tags', query=query))

@app.get('/search-query/<query>')
def search_tags(query):
   
    scavs = []

    for scav in get_all_scavs():
        list = scav['tags']

        for i in range(len(list)):
            if scav['tags'][i] == query:
                scavs.append(scav)

    scav_num = len(scavs)

    return render_template('search-query.html', scavs=scavs, scav_num=scav_num, query=query)

def get_all_scavs():
    with open(SCAV_DATABASE_FILE) as f:
      scavs = json.load(f)

    return scavs

def get_scav(id):
   
    found = False

    for scav in get_all_scavs():
      if scav['id'] == id:
        found = True

        scav_info = scav
        return scav_info
      
    if found == False:
        scav_info = {
           "id": id,
           "description": "This scavenger is not found, and likely does not exist",
           "tags": []
        }

        return scav_info
    
app.run(debug=True)