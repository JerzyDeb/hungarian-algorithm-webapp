const size = document.getElementById("size")
const inputs = document.querySelectorAll('input[name="type"]');

inputs.forEach( input => {
    input.addEventListener("change", () => {
        if(input.value === 'own'){
            document.getElementById('form-for-own-values').style.display = 'block'
            document.getElementById('form-for-team-values').style.display = 'none'
        }
        else{
            document.getElementById('form-for-own-values').style.display = 'none'
            document.getElementById('form-for-team-values').style.display = 'block'
        }
    })
})

size.addEventListener('change', () => {
    write_inputs(size.value)
})

write_inputs = size => {

    const form = document.getElementById("own-values")
    const inputs = form.querySelectorAll('input[type="number"]');
    const submits = form.querySelectorAll('button[type="submit"]');
    const var1   = form.getElementsByTagName('br');

    for(let i = var1.length; i--;) {
        var1[i].remove();
    }
    inputs.forEach(input => {
        input.remove()
    })
    submits.forEach(submit => {
        submit.remove()
    })
    const elem = document.getElementById("elements")
    elem.remove()
    for(let x = 0; x < size; x++){
        for(let y = 0; y < size; y++){
            let field = document.createElement("input");
            field.type = "number"
            field.min = 0
            field.step = "any"
            field.required = true
            field.name = "array"+x.toString()+y.toString()
            form.appendChild(field)
        }
        let br = document.createElement("span");
        br.innerHTML = "<br/>";
        form.appendChild(br);
    }
    let br = document.createElement("span");
    br.innerHTML = "<br/>";
    form.appendChild(br);

    let elements = document.createElement("input");
    elements.type = "hidden"
    elements.id = "elements"
    elements.name = "elements"
    elements.value = size
    form.appendChild(elements)
    if(size > 0) {
        let submit = document.createElement("button")
        submit.type = "submit";
        submit.className = "animated-button"
        submit.innerHTML = "OBLICZ"
        form.appendChild(submit)
    }
}
