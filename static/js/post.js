
// let clickedCount = 0;
// let up_votes = document.getElementById("up_votes")
console.log(window.location.href.charAt(window.location.href.length - 1))
if (window.location.href.charAt(window.location.href.length - 1) == "s") {
  let thing = document.getElementById("order_by").value = ""
}
else {
  let thing = document.getElementById("order_by").value = window.location.href.charAt(window.location.href.length - 1)

}

// pic_votes.onclick = function () {
//     clickedCount++;
//     up_votes.innerHTML = clickedCount;
//     console.log(clickedCount)
// }

async function upvote(element) {
  console.log(element.id);
  await fetch(`/upvote/${element.id}`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((responseJSON) => {
      // do stuff with responseJSON here...

      console.log(responseJSON);
      refreshDiscussions(responseJSON.discussion);
    });
}
function refreshDiscussions(discussion) {
  let discussion_object = document.getElementById(discussion.id + "number");
  console.log(discussion_object);

  discussion_object.innerText = discussion.up_votes;
}


async function filterby(element) {
  console.log(element.value);

  window.location.href = "/discussions" + element.value



} 