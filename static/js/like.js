document.addEventListener('DOMContentLoaded', (event) => {
    const likeButtons = document.querySelectorAll('.like-btn');
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const requestId = this.getAttribute('data-request-id');
            fetch(`/like/${requestId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.likes !== undefined) {
                    this.querySelector('.badge').innerText = data.likes;
                    if (data.liked) {
                        this.innerHTML = `Unlike <span class="badge badge-light">${data.likes}</span>`;
                    } else {
                        this.innerHTML = `Like <span class="badge badge-light">${data.likes}</span>`;
                    }
                } else {
                    alert(data.error);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    const commentLikeButtons = document.querySelectorAll('.comment-like-btn');
    commentLikeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            fetch(`/like_comment/${commentId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.likes !== undefined) {
                    this.querySelector('.badge').innerText = data.likes;
                    if (data.liked) {
                        this.innerHTML = `Unlike <span class="badge badge-light">${data.likes}</span>`;
                    } else {
                        this.innerHTML = `Like <span class="badge badge-light">${data.likes}</span>`;
                    }
                } else {
                    alert(data.error);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
