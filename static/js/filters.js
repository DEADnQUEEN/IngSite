let table_rows = document.getElementById('main-table-body').children;

function table_filter(input) {
    let collection = document.getElementsByClassName('column-' + input.name)
    for (let i = 0; i < collection.length; i++){
        table_rows[i + 1].className = 'content-row-filtered'
        if (collection[i].getElementsByTagName('input')[0].value.includes(input.value)){
            console.log(collection[i])
            table_rows[i + 1].className = 'content-row'
        }
    }
}

function table_filter_id(input) {
    let collection = document.getElementsByClassName('column-' + input.name)
    for (let i = 0; i < collection.length; i++){
        table_rows[i + 1].className = 'content-row-filtered'
        if (collection[i].getElementsByTagName('a')[0].textContent.includes(input.value)){
            console.log(collection[i])
            table_rows[i + 1].className = 'content-row'
        }
    }
}
