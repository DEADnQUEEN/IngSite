function add(el_class) {
    let xhr = new XMLHttpRequest();
    let inputs = document.querySelectorAll("." + el_class + " > *:not(#id)");

    let data = {
        'table': document.title,
        'model-content': {}
    }

    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].value.length === 0){
            return;
        }

        data['model-content'][inputs[i].name] = inputs[i].value;
        if (inputs[i].type === 'number') {
            data['model-content'][inputs[i].name] = Number(inputs[i].value);
        }
    }

    xhr.open("POST", '/admin/add')

    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.setRequestHeader('X-CSRFToken', document.querySelector('[name=csrfmiddlewaretoken]').value);

    xhr.send(JSON.stringify(data));
}
