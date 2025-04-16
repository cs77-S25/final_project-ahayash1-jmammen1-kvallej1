
// let clickedCount = 0;
// let up_votes = document.getElementById("up_votes")



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