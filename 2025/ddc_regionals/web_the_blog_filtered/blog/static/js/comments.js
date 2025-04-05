
async function loadComments() {
    let response = await fetch("/comments");
    let comments = await response.json();
    let commentList = document.getElementById("comment-list");
    commentList.innerHTML = "";
    comments.forEach(comment => {
        let newComment = document.createElement("li");
        newComment.className = "comment";
        newComment.innerHTML = sanitizeHTML(comment);
        commentList.appendChild(newComment);
    });
}

async function addComment() {
    let input = document.getElementById("comment-input");
    let commentText = input.value.trim();
    if (commentText !== "") {
        let response = await fetch("/comment", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ comment: commentText })
        });
        if (response.ok) {
            input.value = "";
            loadComments();
        }
    }
}

window.onload = loadComments;