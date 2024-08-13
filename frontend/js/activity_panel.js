const createPostButton = document.querySelector('.inspire-us-button');
const createButtonModal = document.querySelector('.create-post');
const closeModalButton = document.querySelector('.btn-cancel');
const overlay = document.querySelector('.overlay');

if (window.location.pathname === '/') {

    document.querySelector('select[name="post_type"]').addEventListener('change', function () {
        if (this.value === 'event') {
            document.getElementById('event-fields').style.display = 'flex';
            document.getElementById('text-fields').style.display = 'none';
        } else {
            document.getElementById('event-fields').style.display = 'none';
            document.getElementById('text-fields').style.display = 'block';
        }
    });

    document.addEventListener('DOMContentLoaded', function () {
        const postTypeSelect = document.querySelector('select[name="post_type"]');
        if (postTypeSelect.value === 'event') {
            document.getElementById('event-fields').style.display = 'flex';
            document.getElementById('text-fields').style.display = 'none';
        } else {
            document.getElementById('event-fields').style.display = 'none';
            document.getElementById('text-fields').style.display = 'block';
        }
    });


    createPostButton.addEventListener('click', () => {
        createButtonModal.classList.add('open')
    })

    closeModalButton.addEventListener('click', (e) => {
        e.preventDefault();
        createButtonModal.classList.remove('open')
    })

    overlay.addEventListener('click', (e) => {
        if (e.target.classList.contains('overlay')) {
            createButtonModal.classList.remove('open')
        }

    })

}


document.addEventListener("DOMContentLoaded", function () {
    const commentCounters = document.querySelectorAll(".comment-counter");

    commentCounters.forEach(function (counter) {
        counter.addEventListener("click", function () {
            const postId = this.getAttribute("data-post-id");
            const commentsSection = document.getElementById("comments-section-wrapper-" + postId);
            if (commentsSection.style.display === "none" || commentsSection.style.display === "") {
                commentsSection.style.display = "block";
            } else {
                commentsSection.style.display = "none";
            }
        });
    });
});
