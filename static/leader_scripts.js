function toggleLeader(element) {
    if (element.innerText === "") {
        element.innerText = "領先方";
        element.style.backgroundColor = "yellow";
        element.style.color = "black";
    } else {
        element.innerText = "";
        element.style.backgroundColor = "";
        element.style.color = "black";
    }
}