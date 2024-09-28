let payment_blocks = document.getElementsByClassName('payment-blocks');

for (let i = 0; i < payment_blocks.length; i++){
    let scroll = payment_blocks[i].getElementsByClassName('scroll-div')[0];
    let scroll_bar = payment_blocks[i].getElementsByClassName('scroll-bar')[0];
    let thumb = scroll_bar.getElementsByClassName('scroll-thumb')[0];

    let buttons = scroll_bar.getElementsByClassName('scroll-button');

    for (let j = 0; j < buttons.length; j++){
        if (buttons[j].classList.contains('up')){
            buttons[j].addEventListener(
                'click', () => {
                    scroll.scrollTo({
                        'top': scroll.scrollTop - ((scroll.scrollHeight - scroll.offsetHeight) / 10)
                    })
                }
            );
        }
        if (buttons[j].classList.contains('down')){
            buttons[j].addEventListener(
                'click', () => {
                    scroll.scrollTo({
                        'top': scroll.scrollTop + ((scroll.scrollHeight - scroll.offsetHeight) / 10)
                    })
                }
            );
        }
    }

    scroll.addEventListener(
        "scroll",
        () => {
            thumb.setAttribute('style', 'height: ' + (scroll.scrollTop / (scroll.scrollHeight - scroll.offsetHeight) * 100) + "%;")
        }
    );
}
