from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    player = None
    error = None

    if request.method == "POST":

        mode = request.form.get("mode")
        region = request.form.get("region")
        pseudo = request.form.get("pseudo", "").strip()
        action = request.form.get("action")

        url = f"https://mctiers.com/api/v2/mode/{mode}?count=100000"

        try:

            response = requests.get(url)

            print("URL API :", url)
            print("Code API :", response.status_code)

            if response.status_code != 200:
                error = response.text

                return render_template(
                    "index.html",
                    player=player,
                    error=error
                )


            data = response.json()

            players = []


            # Récupération des joueurs
            for tier_name, tier_players in data.items():

                if not isinstance(tier_players, list):
                    continue

                for p in tier_players:

                    if isinstance(p, dict):

                        # On ne remplace pas le tier original
                        p["tier_name"] = tier_name
                        p["mode"] = mode

                        players.append(p)



            # Filtre région
            players = [
                p for p in players
                if p.get("region", "").upper() == region.upper()
            ]


            print("Nombre joueurs :", len(players))


            # Classement des tiers
            def tier_value(tier):

                tier = str(tier).upper()

                if "1" in tier:
                    return 1

                if "2" in tier:
                    return 2

                if "3" in tier:
                    return 3

                if "4" in tier:
                    return 4

                if "5" in tier:
                    return 5

                return 99



            # Tri
            players.sort(
                key=lambda p: (
                    tier_value(p.get("tier_name")),
                    int(p.get("pos", 999999))
                )
            )


            # Rang
            for i, p in enumerate(players):
                p["rank"] = i + 1



            # Recherche
            if action == "search":

                result = [
                    p for p in players
                    if p.get("name", "").lower() == pseudo.lower()
                ]

                if result:
                    player = result[0]

                else:
                    error = "Joueur introuvable"



            # Random
            elif action == "random":

                if players:

                    random.shuffle(players)

                    player = players[0]

                else:

                    error = "Aucun joueur trouvé"



        except Exception as e:

            error = str(e)
            print("ERREUR :", e)



    return render_template(
        "index.html",
        player=player,
        error=error
    )



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
