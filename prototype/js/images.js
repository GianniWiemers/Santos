document.querySelectorAll(".img").forEach(x => {
    let container = document.createElement("div");
    container.classList.add("container")

    let image = document.createElement("img");
    image.classList.add("player")
    image.src = '/images/santacat.png';
    image.addEventListener('click', function(){
        toggleSelected();
    });

    function toggleSelected(){
        if (x.classList.contains("selected")) {
            x.classList.remove("selected");
        } else {
            x.classList.add("selected");
        }
    }

    container.appendChild(image)
    x.appendChild(container)
})

let opponentimage = document.createElement("img");
opponentimage.classList.add("opponent")
opponentimage.src = '/images/santacat.png';
document.querySelector("#opponent").appendChild(opponentimage);
