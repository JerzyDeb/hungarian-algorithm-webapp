blur_body = form => {
    document.getElementById("opacity-div").style.display = 'block'
    const divs = document.querySelectorAll("body > *:not(.top-form)")
    divs.forEach( div => {
        div.style.filter = 'blur(2px)'
    })
    document.getElementById(form).style.display = 'block'
}
unBlur_body = (form, form1) => {
    document.getElementById(form1).reset()
    document.getElementById("opacity-div").style.display = 'none'
    const divs = document.querySelectorAll("body > *:not(.top-form)")
    divs.forEach( div => {
        div.style.filter = 'none'
    })
    document.getElementById(form).style.display = 'none'
}

function submit_form(event){
    let decision = confirm('Plan utworzy się na podstawie wcześniej uzupełnionych danych pracowników. Upewnij się, że wprowadziłeś je prawidłowo, Jeżeli liczba pracowników i zadań różnią się od siebie to zostaną utworzone nowe rekordy.')
    if(!decision)  event.preventDefault()
}

if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}
