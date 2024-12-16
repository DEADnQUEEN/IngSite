function save(el_class, con) {
    let inputs = document.querySelectorAll('.' + el_class + ':not(.id)');
    let id = document.querySelector('.' + el_class + '.id > input:checked');
    let data = {
        'id': id.value
    }

    for (let i = 0; i < inputs.length; i++){
        let col_type = inputs[i].classList[1];
        let input;
        if (inputs[i].classList.contains('combobox')){
            input = inputs[i].querySelector('input:checked');
            col_type += '_id'
        }
        else {
            input = inputs[i].querySelector('input')
        }

        if (input === undefined || input.value.length === 0){
            return;
        }

        data[col_type] = input.value;
    }

    let xhr = new XMLHttpRequest();

    xhr.open("POST", '/admin/' + con + '/' + window.location.href.split('/')[window.location.href.split('/').length - 1])

    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.setRequestHeader('X-CSRFToken', document.querySelector('[name=csrfmiddlewaretoken]').value);

    xhr.onload = () => {
        if (xhr.status === 200){
            console.log(xhr.response)
            return;
        }
        console.log('Error ' + xhr.status)
    }

    xhr.send(JSON.stringify(data));
}
