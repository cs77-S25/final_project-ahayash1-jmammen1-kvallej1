
let clickedCount = 0;
up_votes = document.getElementById("up_votes")
let up_votes = document.getElementById("up_votes");


up_votes.onclick = function () {
    clickedCount++;
    up_votes.innerHTML = clickedCount;
}