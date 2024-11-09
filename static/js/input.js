let inputs = document.querySelectorAll("#name, #surname, #father-name");

for (let i = 0; i < inputs.length; i++) {
    inputs[i].addEventListener(
        "keyup",
        () => {
            inputs[i].value = inputs[i].value.replace(/[^а-яА-Яa-zA-Z]/g, "");
            inputs[i].focus();
            inputs[i].setSelectionRange(inputs[i].value.length, inputs[i].value.length);
        }
    );
}