document.addEventListener("DOMContentLoaded", () => {
    const fromText = document.querySelector(".from-text");
    const toText = document.querySelector(".to-text");
    const exchangeIcon = document.querySelector(".exchange");
    const srcSelect = document.querySelector(".src-select");
    const tgtSelect = document.querySelector(".tgt-select");
    const icons = document.querySelectorAll(".row i");
    const translateBtn = document.querySelector("button");

    exchangeIcon.addEventListener("click", () => {
        let tempText = fromText.value;
        let tempLang = srcSelect.value;
        fromText.value = toText.value;
        toText.value = tempText;
        srcSelect.value = tgtSelect.value;
        tgtSelect.value = tempLang;
    });

    fromText.addEventListener("keyup", () => {
        if (!fromText.value) {
            toText.value = "";
        }
    });

    translateBtn.addEventListener("click", () => {
        let text = fromText.value.trim();
        let translateFrom = srcSelect.value;
        let translateTo = tgtSelect.value;
        if (!text) return;
        toText.setAttribute("placeholder", "Translating...");
        let apiUrl = `/translate?text=${text}&from=${translateFrom}&to=${translateTo}`;
        fetch(apiUrl)
            .then((res) => res.json())
            .then((data) => {
                toText.value = data.translated_text;
                srcSelect.value = data.source_language;
                tgtSelect.value = data.target_language;
                toText.setAttribute("placeholder", "Translation");
            });
    });

    icons.forEach((icon) => {
        icon.addEventListener("click", ({ target }) => {
            if (!fromText.value || !toText.value) return;
            if (target.classList.contains("fa-copy")) {
                if (target.id == "from") {
                    navigator.clipboard.writeText(fromText.value);
                } else {
                    navigator.clipboard.writeText(toText.value);
                }
            } else {
                let utterance;
                if (target.id == "from") {
                    utterance = new SpeechSynthesisUtterance(fromText.value);
                    utterance.lang = srcSelect.value;
                } else {
                    utterance = new SpeechSynthesisUtterance(toText.value);
                    utterance.lang = tgtSelect.value;
                }
                speechSynthesis.speak(utterance);
            }
        });
    });
});




