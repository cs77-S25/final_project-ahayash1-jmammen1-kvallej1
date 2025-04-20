//allows user to filter by whatever the user chooses and updates the page to the correct filter
console.log(window.location.href.charAt(window.location.href.length - 1))
if (window.location.href.charAt(window.location.href.length - 1) == "s") {
    let thing = document.getElementById("order_by").value = ""
}
else {
    let thing = document.getElementById("order_by").value = window.location.href.charAt(window.location.href.length - 1)

}

document.getElementById("submitReview").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default form submission

    let form = document.getElementById("form");
    let title = document.getElementById("title").value;
    let content = document.getElementById("content").value;
    let major = document.getElementById("major").value;
    let selectedRatingInput = document.querySelector('input[name="rating"]:checked');
    let rating = selectedRatingInput ? selectedRatingInput.value : null;

    if (!rating) {
        alert("Please select star rating.")
        return;
    }
    // body = JSON.stringify({"title": title, "author": author, "content": content, "major": major, "rating1": rating1, "rating2": rating2, "rating3": rating3, "rating4": rating4, "rating5": rating5}); //deleted "created_at": created_at,
    let body = JSON.stringify({ "title": title, "content": content, "major": major, "rating": rating }); //deleted "created_at": created_at,
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
            if (data["success"] == false) {
                window.location.href = "/error";
            } else {
                window.location.href = "/reviews";
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});
review = data["review"];
console.log(review)

window.location.href = ["/reviews"];
// window.location.replace("reviews");

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

//reloads the reviews page?
function refreshReviews(review) {
    let review_object = document.getElementById(review.id + "number");
    console.log(review_object);
    review_object.innerText = review.rating;
}

//assists with sorting by the correct filter by selection by the user
async function filterby(element) {
    console.log(element.value);
    window.location.href = "/reviews" + element.value
} 