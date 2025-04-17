document.getElementById("submitForm").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default form submission

  
 
    let content = document.getElementById("content").value;
   
   
    body = JSON.stringify({"content": content}); 
    console.log(body)
  
    fetch('/discussion_comment', {
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
        comment = data["comment"];
        console.log(comment)
        
        window.location.href = "/";
        window.location.replace("discussions");

        let listgrp = document.getElementsByClassName("list-group")[0];
        let a = document.createElement("a");
        a.href = `/discussion/${comment["id"]}`;
        a.className = "list-group-item";
       
        let b = document.createElement("p");
        b.appendChild(document.createTextNode(comment["content"]));
      
     
        
        a.appendChild(b);
       
     
        listgrp.prepend(a);