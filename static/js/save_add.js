function save_add(el_class, con) {
    console.log(el_class, con)
    // let selector = "." + el_class + " > *"
    // if (con === 'add'){
    //     selector += ":not(#id)"
    // }
    // let inputs = document.querySelectorAll(selector);
    // let data = {}
    //
    // for (let i = 0; i < inputs.length; i++) {
    //     if (inputs[i].value.length === 0){
    //         return;
    //     }
    //
    //     data[inputs[i].name] = inputs[i].value;
    //     if (inputs[i].type === 'number') {
    //         data[inputs[i].name] = Number(inputs[i].value);
    //     }
    // }
    //
    // let xhr = new XMLHttpRequest();
    //
    // xhr.open("POST", '/admin/' + con + '/' + document.title)
    //
    // xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    // xhr.setRequestHeader('X-CSRFToken', document.querySelector('[name=csrfmiddlewaretoken]').value);
    //
    // xhr.send(JSON.stringify(data));
}
