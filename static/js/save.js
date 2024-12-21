function collect_data_from(sel_class) {
    let values = document.querySelectorAll('.' + sel_class + ':not(.id)')
    let data = {}

    for (let i = 0; i < inputs.length; i++){
        let col_type = values[i].classList[1];
        let input;
        if (values[i].classList.contains('combobox')){
            input = values[i].querySelector('input:checked');
            col_type += '_id'
        }
        else {
            input = values[i].querySelector('input')
        }

        if (input === undefined || input.value.length === 0){
            return undefined;
        }
        data[col_type] = input.value;
    }
    return data;
}


let buttons = document.querySelectorAll('.table-button');

function save(el_class) {
    let data = collect_data_from(el_class);

    if (data === undefined){
        return;
    }

    data['id'] = document.querySelector('.' + el_class + '.id > input:checked')

    let xhr = new XMLHttpRequest();

    xhr.open(
        "POST",
        '/admin/save/' + document.querySelector('a#model-name').textContent
    )

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
