show_div = div_id => {
    const div = document.getElementById(div_id)
    if(div.style.display === 'none'){
        div.style.display = 'block'
    }
    else{
        div.style.display = 'none'
    }

}

large_image = img_id => {
    const img = document.getElementById(img_id);
    if(img.style.width === "95%"){
        img.style.width = "60%";
    }
    else{
        img.style.width = "95%";
    }
}