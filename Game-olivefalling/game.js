// static/game.js

$(document).ready(function() {
    var canvas = document.getElementById("gameCanvas");
    var ctx = canvas.getContext("2d");

    var player = {
        x: canvas.width / 2 - 25,
        y: canvas.height - 120,
        width: 50,
        height: 100
    };

    var apples = [];
    var score = 0;

    var touchesGauche = false;
    var touchesDroite = false;

    document.addEventListener('keydown', function(event) {
        if (event.key === 'ArrowLeft') {
            touchesGauche = true;
        } else if (event.key === 'ArrowRight') {
            touchesDroite = true;
        }
    });

    document.addEventListener('keyup', function(event) {
        if (event.key === 'ArrowLeft') {
            touchesGauche = false;
        } else if (event.key === 'ArrowRight') {
            touchesDroite = false;
        }
    });

    function dessiner() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Dessiner le joueur
        ctx.drawImage(personnageImage, player.x, player.y, player.width, player.height);

        // Dessiner les pommes
        for (var i = 0; i < apples.length; i++) {
            var apple = apples[i];
            ctx.drawImage(pommeImage, apple.x, apple.y, 30, 30);
        }

        // Afficher le score
        ctx.fillStyle = "#000";
        ctx.font = "20px Arial";
        ctx.fillText("Score: " + score, 10, 30);
    }

    function mettreAJourCanvas() {
        if (touchesGauche && player.x > 0) {
            player.x -= 5;
        }
        if (touchesDroite && player.x + player.width < canvas.width) {
            player.x += 5;
        }

        // Déplacer les pommes
        for (var i = 0; i < apples.length; i++) {
            var apple = apples[i];
            apple.y += 5; // Ajustez la vitesse de chute des pommes

            // Vérifier la collision avec le joueur
            if (
                player.x < apple.x + 30 &&
                player.x + player.width > apple.x &&
                player.y < apple.y + 30 &&
                player.y + player.height > apple.y
            ) {
                apples.splice(i, 1);
                score += 1; // Incrémenter le score lorsqu'une pomme est ramassée
            }
        }

        // Générer une nouvelle pomme aléatoire
        if (Math.random() < 0.02) {
            apples.push({
                x: Math.random() * (canvas.width - 30),
                y: 0
            });
        }

        dessiner();
    }

    var personnageImage = new Image();
    personnageImage.src = "gm.png";
    var pommeImage = new Image();
    pommeImage.src = "apple.png";

    setInterval(mettreAJourCanvas, 1000 / 60); // Mettre à jour à environ 60 FPS
});
