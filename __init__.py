from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)      


                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def mongraphique2():
    return render_template("histogramme.html")

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route("/commits/")
def MaPremiereAPI2():
    return render_template("commits.html")



@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route('/github/')
def github():
    response2 = urlopen('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    raw_content = response2.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for commit in json_content:
        commit_info = commit.get('commit', {})
        author_info = commit_info.get('author', {})
        results.append({
            'author': author_info.get('name'),
            'date': author_info.get('date')
            
        })
        
    return jsonify(results=results)

def commits_data():
    response3 = urlopen('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    raw_content = response3.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    
    # Dictionary to count commits per minute
    commits_per_minute = {i: 0 for i in range(60)}
    
    for commit in json_content:
        commit_info = commit.get('commit', {})
        author_info = commit_info.get('author', {})
        date_str = author_info.get('date')
        
        if date_str:
            date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minute = date_object.minute
            
            commits_per_minute[minute] += 1

    # Convert the dictionary to a list of tuples
    results = [{'minute': k, 'commits': v} for k, v in sorted(commits_per_minute.items())]
    
    return jsonify(results=results)



if __name__ == "__main__":
  app.run(debug=True)
