document.addEventListener('DOMContentLoaded', function() {
    const nextLessonBtn = document.querySelector('.action-btn.next');
    if (nextLessonBtn) {
        nextLessonBtn.addEventListener('click', function(event) {
            event.preventDefault();
            window.location.href = nextLessonBtn.getAttribute('href');
        });
    }
});


