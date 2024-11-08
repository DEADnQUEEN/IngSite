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

let mails = document.querySelectorAll("#mail");

for (let i = 0; i < mails.length; i++) {
    inputs[i].addEventListener(
        "keyup",
        () => {
            mails[i].value = mails[i].value.replace(/[^а-яА-Яa-zA-Z]/g, "");
            mails[i].focus();
            mails[i].setSelectionRange(mails[i].value.length, mails[i].value.length);
        }
    );
}