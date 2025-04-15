document.getElementById("submitForm").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default form submission

    let form = document.getElementById("form");
    let title = document.getElementById("title").value;
    let content = document.getElementById("content").value;
    let author = document.getElementById("author").value;
    let course = document.getElementById("course").value;
    let upvotes = document.getElementById("upvotes").value;
    body = JSON.stringify({"title": title, "author": author, "content": content, "course": course}); //deleted "created_at": created_at,
    //body = {"title": "HIIII"}
    fetch('/new_discussion', {
        method: 'POST',
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json"
        },
        body: body
    })
        .then(response => response.json()) // Adjust based on expected response
        .then(data => {
            console.log("Success:", data);
            if(data["success"]==false){
                window.location.href = "/error";
            } else{
                // form.reset();
                window.location.href = "/";
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});
        discussion = data["discussion"];
        console.log(discussion)
        
        window.location.href = "/";
        window.location.replace("discussions");

        let listgrp = document.getElementsByClassName("list-group")[0];
        let a = document.createElement("a");
        a.href = `/discussion/${discussion["id"]}`;
        a.className = "list-group-item";
        let h = document.createElement("h5");
        h.appendChild(document.createTextNode(discussion["title"]));
        let b = document.createElement("p");
        b.appendChild(document.createTextNode(discussion["content"]));
        let c = document.createElement("p");
        c.appendChild(document.createTextNode(discussion["author"]));
        let d = document.createElement("p");
        d.appendChild(document.createTextNode(discussion["created_at"]));
        a.appendChild(h);
        a.appendChild(b);
        a.appendChild(c);
        a.appendChild(d);
        listgrp.prepend(a);

async function upvote(element){
    console.log(element.id);
    await fetch('/upvote/${element.id}', {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
    })
    .then((response) => response.json())
    .then((responseJSON) => {
        refreshDiscussions(responseJSON.discussion)
    })
}

function refreshDiscussions(discussion){
    let discussion_object = document.getElementById(discussion.id + "number");
    discussion_object.innerText = discussion.upvotes;
}