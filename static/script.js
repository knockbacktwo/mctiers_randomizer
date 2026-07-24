function startRandomAnimation(playerList, finalPlayer) {

    const card = document.querySelector(".card");

    if (!card || !playerList || !finalPlayer) {
        return;
    }

    let count = 0;

    const animation = setInterval(() => {

        const randomPlayer =
            playerList[Math.floor(Math.random() * playerList.length)];

        card.innerHTML = `
            <h2>${randomPlayer.name}</h2>
            <p>Tier ${randomPlayer.tier}</p>
            <p>Rang #${randomPlayer.rank}</p>
        `;

        count++;

        if (count >= 25) {

            clearInterval(animation);

            card.innerHTML = `
                <h2>🎉 ${finalPlayer.name}</h2>
                <p>Tier ${finalPlayer.tier}</p>
                <p>Rang #${finalPlayer.rank}</p>
            `;

        }

    }, 100);

}
