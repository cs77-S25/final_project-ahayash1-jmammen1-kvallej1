
let clickedCount = 0;
up_votes = document.getElementById("up_votes")
let num_votes = document.getElementById("num_votes");


up_votes.onclick = function () {
    clickedCount++;
    num_votes.innerHTML = clickedCount;
}