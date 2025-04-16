
let clickedCount = 0;
let up_votes = document.getElementById("up_votes")



pic_votes.onclick = function () {
    clickedCount++;
    up_votes.innerHTML = clickedCount;
}