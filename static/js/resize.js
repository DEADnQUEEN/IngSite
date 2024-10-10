let l = document.getElementsByClassName('student-course');

const resizeObserver = new ResizeObserver(_ =>
    {
        for (let i = 0; i < l.length; i++){
            let container = l[i].getElementsByClassName('content-block')[0];
            let height = '100%'
            if (768 < document.getElementsByTagName('body')[0].offsetWidth){
                height = container.getElementsByClassName('visit-blocks')[0].offsetHeight +'px';
            }
            container.setAttribute(
                "style",
                'height: ' + height
            );
        }
    }
)

for (let i = 0; i < l.length; i++){
    let container = l[i].getElementsByClassName('content-block')[0];

    resizeObserver.observe(container);
}


