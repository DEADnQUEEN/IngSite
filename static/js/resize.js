let l = document.getElementsByClassName('student-course');

const resizeObserver = new ResizeObserver(_ =>
    {
        for (let i = 0; i < l.length; i++){
            let container = l[i].getElementsByClassName('content-block')[0];
            container.setAttribute(
                "style",
                'height: ' + container.getElementsByClassName('visit-blocks')[0].offsetHeight +'px'
            );
        }
    }
)

for (let i = 0; i < l.length; i++){
    let container = l[i].getElementsByClassName('content-block')[0];

    resizeObserver.observe(container);
}


