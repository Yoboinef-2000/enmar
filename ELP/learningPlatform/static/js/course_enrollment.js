document.addEventListener('DOMContentLoaded', function () {
    const enrollButtons = document.querySelectorAll('.btn-enroll');

    enrollButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const courseId = this.getAttribute('data-course-id');
            const url = this.getAttribute('href');

            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (response.ok) {
                    this.textContent = 'Already Enrolled';
                    this.classList.remove('btn-outline-primary');
                    this.classList.add('btn-secondary');
                    this.setAttribute('disabled', true);
                } else {
                    alert('Enrollment failed. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Enrollment failed. Please try again.');
            });
        });
    });
});
