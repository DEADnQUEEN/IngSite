function add_row() {
    if (document.querySelector('.filter-column#id:placeholder-shown') == null){
        return;
    }

    if (document.querySelectorAll('.content-row-filtered').length > 0){
        return;
    }

    if (document.querySelectorAll('.filter-column:not(#id):placeholder-shown').length !== 0){
        return;
    }

    let inputs = document.querySelectorAll('.filter-column:not(#id):not(:placeholder-shown)');
    let data = {
        'table': document.title,
        'model-content': {}
    }
    for (let i = 0; i < inputs.length; i++){
        if (inputs[i].type === 'number'){
            data['model-content'][inputs[i].placeholder] = Number(inputs[i].value)
        }
        else {
            data['model-content'][inputs[i].placeholder] = inputs[i].value
        }
    }

    let xhr = new XMLHttpRequest()

    xhr.open("POST", '/admin/add')

    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.setRequestHeader('X-CSRFToken', document.querySelector('[name=csrfmiddlewaretoken]').value);

    xhr.send(JSON.stringify(data));
}
