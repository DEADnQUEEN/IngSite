const bind = document.querySelectorAll('.filter-column')
const last_content = []

for (let i = 0; i < bind.length; i++){
    last_content.push('');
    bind[i].addEventListener(
        'input',
        () => {
            let found = 'content-row';
            if (last_content[i].length < bind[i].value.length){
                found += '-filtered'
            }
            let rows = document.querySelectorAll('.' + found);

            for (let j = 0; j < rows.length; j++){
                rows[j].className = 'content-row'
                if (rows[j].getElementsByTagName('input')[i].value.includes(bind[i].value)){
                    rows[j].className += '-filtered'
                }
            }

            last_content[i] = bind[i].value;
        }
    )
}


