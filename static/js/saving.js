function update(input_field) {
    input_field.classList.add('changed');
    input_field.parentNode.parentNode.parentNode.querySelectorAll('button')[0].classList.add('save-button');
}
