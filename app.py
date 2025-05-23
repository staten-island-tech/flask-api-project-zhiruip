from flask import Flask, render_template, request, abort
import requests

app = Flask(__name__)
API_URL = "https://akabab.github.io/superhero-api/api/all.json"

def fetch_heroes():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return sorted(response.json(), key=lambda x: x['name'])
    except Exception as e:
        print(f"Error fetching heroes: {e}")
        return []

@app.route('/')
def index():
    heroes = fetch_heroes()
    query = request.args.get('search', '').lower()
    no_results = False

    if query:
        heroes = [h for h in heroes if query in h['name'].lower()]
        no_results = len(heroes) == 0

    return render_template("index.html", heroes=heroes, no_results=no_results)

@app.route('/hero/<int:hero_id>')
def hero(hero_id):
    try:
        hero_data = requests.get(f"https://akabab.github.io/superhero-api/api/id/{hero_id}.json").json()
        return render_template("hero.html", hero=hero_data)
    except Exception:
        abort(404)

@app.errorhandler(404)
def not_found(e):
    return "<h1>404 Hero Not Found</h1>", 404

if __name__ == '__main__':
    app.run(debug=True)
