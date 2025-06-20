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
    query = request.args.get('search', '').strip().lower()
    min_power_input = request.args.get('min_power', '').strip()
    no_results = False

    if query:
        heroes = [h for h in heroes if query in h['name'].lower()]

    if min_power_input:
        try:
            min_power = int(min_power_input)
            filtered = []
            for h in heroes:
                power = h.get('powerstats', {}).get('power')
                if isinstance(power, int) and power >= min_power:
                    filtered.append(h)
            heroes = filtered
        except ValueError:
            pass  

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
    return """
        <h1>404 Hero Not Found</h1>
        <p>The hero you are looking for does not exist.</p>
        <a href="/" class="back-button">Back to All Heroes</a>
    """, 404

if __name__ == '__main__':
    app.run(debug=True)



