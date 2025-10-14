

function renderBODS(){
    const el = document.getElementById("ownership-data");
    if (!el) return;
    const bods = JSON.parse(el.dataset.bods);
    console.log(bods)
    const data = [bods.statements]


    try {
    const container = document.getElementById("graph-container");
    container.innerHTML = "";
    const imagesPath = "";
    const labelLimit = 8;

    const viz = BODSDagre.draw({
        data, container, imagesPath, labelLimit
    });
    } catch(err){
        console.error("Failed to parse JSON", err, bods)
    }
}


document.addEventListener("htmx:afterSwap", (evt) => {
    if (evt.target.querySelector("#ownership-data")){
        renderBODS();
 }
});

