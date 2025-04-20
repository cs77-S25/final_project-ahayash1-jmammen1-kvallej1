document.getElementById("submitDiscussion").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default form submission
    // let form = document.getElementById("form");
    let title = document.getElementById("title").value;
    let content = document.getElementById("content").value;
    let course = document.getElementById("course").value;

    body = JSON.stringify({ "title": title, "content": content, "course": course }); //deleted "created_at": created_at,
    console.log(body)
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
            if (data["success"] == false) {
                window.location.href = "/error";
            } else {
                // form.reset();
                window.location.href = "/discussions";
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});

discussion = data["discussion"];
console.log(discussion)

window.location.replace("/discussions");

let listgrp = document.getElementsByClassName("list-group")[0];
let a = document.createElement("a");
a.href = `/discussion/${discussion["id"]}`;
a.className = "list-group-item";
let h = document.createElement("h5");
h.appendChild(document.createTextNode(discussion["title"]));
let b = document.createElement("p");
b.appendChild(document.createTextNode(discussion["content"]));
let d = document.createElement("p");
d.appendChild(document.createTextNode(discussion["created_at"]));
a.appendChild(h);
a.appendChild(b);
a.appendChild(d);
listgrp.prepend(a);


document.addEventListener("DOMContentLoaded", function () {
    window.upvote = async function (event, element) {
        event.preventDefault();
        console.log(element.id);

        const response = await fetch(`/upvote/${element.id}`, {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
        });
        const data = await response.json();
        console.log(data);
        refreshDiscussions(data.discussion);
    };
    function refreshDiscussions(discussion) {
        const el = document.getElementById(discussion.id + "number");
        console.log(el);
        if (el) {
            el.innerText = discussion.up_votes;
        }
    }
});

var select = document.getElementById("order_by");
for (var i = 0; i < select.options.length; i++) {
    if (select.options[i].value == c) {
        select.options[i].selected = true;
    }
    console.log(select)
}