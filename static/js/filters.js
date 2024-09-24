const bind = document.querySelectorAll('.filter-column')
const last_content = []

function checker(index, rec) {
    console.log(rec, index)
    let found = 'content-row';
    if (last_content[index].length > bind[index].value.length){
        found += '-hidden'
    }

    let rows = document.querySelectorAll('.' + found);

    for (let j = 0; j < rows.length; j++){
        rows[j].className = 'content-row'
        if (!rows[j].getElementsByTagName('input')[index].value.includes(bind[index].value)){
            rows[j].className += '-hidden'
        }
    }

    if (last_content[index].length > bind[index].value.length){
        let inputs = document.querySelectorAll('.filter-column');
        console.log(inputs)
        for (let j = 0; j < index; j++){
            if (inputs[j].value.length !== 0){
                    checker(j, true);
                    console.log(j)
            }
        }
        console.log('half');
        for (let j = index + 1; j < inputs.length; j++){
            if (inputs[j].value.length !== 0){
                checker(j, true);
                console.log(j)
            }
        }
    }

    last_content[index] = bind[index].value;
}

for (let i = 0; i < bind.length; i++){
    last_content.push('');

    bind[i].addEventListener(
        'input',
        () => {
            checker(i, false);
        }
    )
}


