document.getElementById("search-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const response = await fetch("/search", {
        method: "POST",
        body: formData,
    });

    const data = await response.json();
    const resultSection = document.querySelector(".result_section")
    let responseDiv = document.createElement("div");

    if (data.length == 0){
        responseDiv.innerHTML += "No data found";

        resultSection.innerText = responseDiv;
        
    };

        responseDiv.innerHTML += "Found";
        resultSection.innerHTML = responseDiv;
})
