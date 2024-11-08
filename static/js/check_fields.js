function on_input_func(input_field) {
    if (input_field.classList.contains('init')){
        input_field.classList.remove('init');
    }
}

let phone = document.getElementById('phone');
let prev = ''
phone.addEventListener(
    'input',
    () => {
        if (prev.length === 0) {
            phone.value = "+7" + phone.value;
        }
        prev = phone.value
        if (prev.length === 2) {
            phone.value = '';
            prev = phone.value
        }
    }
)
phone.addEventListener(
    'keyup',
    () => {
        phone.value = phone.value.replace(/[^0-9+]/g, "");
        phone.focus();
        phone.setSelectionRange(phone.value.length, phone.value.length);
    }
)