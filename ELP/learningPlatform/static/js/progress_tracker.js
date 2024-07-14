document.addEventListener("DOMContentLoaded", function() {
    const progressBars = document.querySelectorAll('.progress-bar');

    progressBars.forEach(bar => {
        const progress = bar.getAttribute('aria-valuenow');
        bar.style.width = `${progress}%`;
    });

    const enrollButtons = document.querySelectorAll('.btn-enroll');

    enrollButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const courseId = this.getAttribute('data-course-id');

            fetch(`enroll_course/${courseId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'enrolled') {
                    const progressTracker = document.querySelector(`.progress-tracker[data-course-id="${courseId}"]`);
                    const progressBar = progressTracker.querySelector('.progress-bar');
                    progressBar.style.width = `0%`;
                    progressBar.setAttribute('aria-valuenow', '0');
                    progressBar.textContent = '0%';
                    progressTracker.style.display = 'block';
                    this.textContent = 'Already Enrolled';
                    this.disabled = true;
                    this.classList.add('btn-secondary');
                    this.classList.remove('btn-outline-primary');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
