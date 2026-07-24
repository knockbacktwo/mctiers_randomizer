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


            for tier, tier_players in data.items():

                if not isinstance(tier_players, list):
                    continue


                for p in tier_players:

                    if isinstance(p, dict):

                        p["tier"] = tier
                        p["mode"] = mode

                        players.append(p)



            players = [

                p for p in players

                if p.get("region", "").upper()
                == region.upper()

            ]



            def tier_value(tier):
                tier = str(tier).upper()
            
                if "1" in tier:
                    return 1
                elif "2" in tier:
                    return 2
                elif "3" in tier:
                    return 3
                elif "4" in tier:
                    return 4
                elif "5" in tier:
                    return 5
            
                return 99
            
            
            players.sort(
                key=lambda p: (
                    tier_value(p.get("tier")),
                    int(p.get("pos", 999999))
                )
            )


            for i, p in enumerate(players):

                p["rank"] = i + 1




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



            elif action == "random":

                if players:

                    player = random.choice(players)

                else:

                    error = "Aucun joueur trouvé"



        except Exception as e:

            error = str(e)

            print(e)



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
