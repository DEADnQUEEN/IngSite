function update(input_field) {
    input_field.classList.add('changed');
    input_field.parentNode.parentNode.parentNode.querySelectorAll('button')[0].classList.add('save-button');
}

function save(el_class){
    let xhr = new XMLHttpRequest();
    let inputs = document.querySelectorAll("." + el_class + " > *");

    let data = {
        'table': document.title,
        'model-content': {}
    }

    for (let i = 0; i < inputs.length; i++) {
        data['model-content'][inputs[i].name] = inputs[i].value;
        if (inputs[i].type === 'number') {
            data['model-content'][inputs[i].name] = Number(inputs[i].value);
        }
    }

    xhr.open("POST", '/admin/save')

    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.setRequestHeader('X-CSRFToken', document.querySelector('[name=csrfmiddlewaretoken]').value);

    xhr.send(JSON.stringify(data));
}

