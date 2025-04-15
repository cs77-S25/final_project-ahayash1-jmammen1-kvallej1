document.getElementById("submitReview").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default form submission

    let form = document.getElementById("form");
    let title = document.getElementById("title").value;
    let content = document.getElementById("content").value;
    let author = document.getElementById("author").value;
    let major = document.getElementById("major").value;
    let rating5 = document.getElementById("star5").value;
    let rating4 = document.getElementById("star4").value;
    let rating3= document.getElementById("star3").value;
    let rating2 = document.getElementById("star2").value;
    let rating1 = document.getElementById("star1").value;
    let rating = 5;
    // body = JSON.stringify({"title": title, "author": author, "content": content, "major": major, "rating1": rating1, "rating2": rating2, "rating3": rating3, "rating4": rating4, "rating5": rating5}); //deleted "created_at": created_at,
    body = JSON.stringify({"title": title, "author": author, "content": content, "major": major, "rating": rating}); //deleted "created_at": created_at,
    console.log(body)
    //body = {"title": "HIIII"}
    fetch('/new_review', {
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
                window.location.href = "/";
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});
        review = data["review"];
        console.log(review)
        
        window.location.href = "/";
        window.location.replace("reviews");

        let listgrp = document.getElementsByClassName("list-group")[0];
        let a = document.createElement("a");
        a.href = `/review/${review["id"]}`;
        a.className = "list-group-item";
        let h = document.createElement("h5");
        h.appendChild(document.createTextNode(review["title"]));
        let b = document.createElement("p");
        b.appendChild(document.createTextNode(review["content"]));
        let c = document.createElement("p");
        c.appendChild(document.createTextNode(review["author"]));
        let e = document.createElement("p");
        e.appendChild(document.createTextNode(review["major"]));
        let d = document.createElement("p");
        d.appendChild(document.createTextNode(review["created_at"]));
        let f = document.createElement("p");
        f.appendChild(document.createTextNode(review["rating"]));
        a.appendChild(h);
        a.appendChild(b);
        a.appendChild(c);
        a.appendChild(d);
        a.appendChild(e);
        a.appendChild(f);
        listgrp.prepend(a);