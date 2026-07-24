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
            print(data)

            players = []


            # Récupération des joueurs

            for tier, tier_players in data.items():

                if not isinstance(tier_players, list):
                    continue


                for p in tier_players:

                    if isinstance(p, dict):

                        p["tier"] = tier
                        p["mode"] = mode

                        players.append(p)



            print("Total joueurs :", len(players))


            # Filtre région

            players = [

                p for p in players

                if p.get("region", "").upper()
                == region.upper()

            ]


            print("Joueurs région :", len(players))



            # Classement région

            players.sort(
                key=lambda p: (
                    int(p.get("tier", 99)),
                    int(p.get("pos", 9999))
                )
            )


            for i, p in enumerate(players):

                p["rank"] = i + 1




            # Recherche

            if action == "search":


                result = [

                    p for p in players

                    if p.get("name", "").lower()
                    == pseudo.lower()

                ]


                if result:

                    player = result[0]


                else:

                    error = "Joueur introuvable"



            # Random

            elif action == "random":


                if players:

                    player = random.choice(players)

                else:

                    error = "Aucun joueur trouvé"



                print("Joueur choisi :", player)



        except Exception as e:

            error = str(e)

            print("Erreur :", e)



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

