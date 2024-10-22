document.addEventListener("DOMContentLoaded", function() {
    const textElement = document.getElementById("dyslexia-text");
    const stopShuffleButton = document.getElementById('stop-shuffle-btn');
    const homeButton = document.getElementById('home-btn');
    let shuffleInterval;
    const originalText = textElement.innerText; // Store the original text

    const words = textElement.innerText.split(" ");
    textElement.innerHTML = words.map(word => `<span class="word">${word}</span>`).join(" ");

    function shuffleWord(word) {
        if (word.length <= 1) return word;
        const arr = word.split('');
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr.join('');
    }

    function shuffleLetters() {
        const wordElements = document.querySelectorAll('.word');
        wordElements.forEach(wordElement => {
            wordElement.innerText = shuffleWord(wordElement.innerText);
        });
    }

    // Start shuffling letters every 0.5 seconds
    shuffleInterval = setInterval(shuffleLetters, 500);

    // Stop shuffling when "Stop Shuffle" button is clicked
    stopShuffleButton.addEventListener('click', function() {
        clearInterval(shuffleInterval);  // Stop the shuffling

        // Revert the text to the original content and remove animation
        textElement.innerText = originalText;

        // Remove animation class from the words
        const wordElements = document.querySelectorAll('.word');
        wordElements.forEach(wordElement => {
            wordElement.style.animation = 'none';
        });
    });

    // Redirect to homepage when "Go to Home" button is clicked
    homeButton.addEventListener('click', function() {
        window.location.href = "/"; // Change this to the actual path of your homepage
    });
});
