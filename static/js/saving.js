function send_row_request(row_sender) {
    let xhr = new XMLHttpRequest();

    let table_body = document.getElementById('main-table-body');
    let path = window.location.href.split('/');

    let inputs = table_body.children[row_sender].getElementsByTagName('input');

    let data = {
        'table': path[path.length - 1],
        'id': Number(table_body.children[row_sender].getElementsByTagName('a')[0].textContent)
    }

    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].classList.contains('changed')) {
            if (inputs[i].type === 'number'){
                data[inputs[i].placeholder] = Number(inputs[i].value)
            }
            else {
                data[inputs[i].placeholder] = inputs[i].value
            }
            inputs[i].classList.remove('changed')
        }
    }

    document.getElementById('row-sender-' + row_sender).classList.remove('save-button');

    xhr.open("POST", '/admin/save')

    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.setRequestHeader('X-CSRFToken', document.querySelector('[name=csrfmiddlewaretoken]').value);

    xhr.send(JSON.stringify(data));
}

function update(input_field) {
    input_field.classList.add('changed');
    input_field.parentNode.parentNode.parentNode.querySelectorAll('button')[0].classList.add('save-button');
}

function save_table() {
    let buttons = document.getElementsByClassName('save-line');
    for (let i = 0; i < buttons.length; i++){
        buttons[i].click();
    }
}
