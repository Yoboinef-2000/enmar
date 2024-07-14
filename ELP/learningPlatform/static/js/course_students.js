document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-lesson-btn');
    const messageButtons = document.querySelectorAll('.message-student-btn');
    const removeButtons = document.querySelectorAll('.remove-student-btn');
    
    // Add event listeners to buttons
    deleteButtons.forEach(button => button.addEventListener('click', handleDeleteLesson));
    messageButtons.forEach(button => button.addEventListener('click', handleMessageStudent));
    removeButtons.forEach(button => button.addEventListener('click', handleRemoveStudent));

    function handleDeleteLesson(event) {
        const lessonId = event.target.dataset.lessonId;
        showConfirmationDialog('Are you sure you want to delete this lesson?', () => {
            deleteLesson(lessonId);
        });
    }

    function handleMessageStudent(event) {
        const studentId = event.target.dataset.studentId;
        showMessageDialog(studentId);
    }

    function handleRemoveStudent(event) {
        const studentId = event.target.dataset.studentId;
        showConfirmationDialog('Are you sure you want to remove this student?', () => {
            removeStudent(studentId);
        });
    }

    function showConfirmationDialog(message, onConfirm) {
        const dialog = document.createElement('div');
        dialog.className = 'confirmation-dialog';
        dialog.innerHTML = `
            <div class="dialog-content">
                <p>${message}</p>
                <button id="confirmBtn">Confirm</button>
                <button id="cancelBtn">Cancel</button>
            </div>
        `;
        document.body.appendChild(dialog);

        document.getElementById('confirmBtn').addEventListener('click', function() {
            onConfirm();
            document.body.removeChild(dialog);
        });

        document.getElementById('cancelBtn').addEventListener('click', function() {
            document.body.removeChild(dialog);
        });
    }

    function showMessageDialog(studentId) {
        const dialog = document.createElement('div');
        dialog.className = 'message-dialog';
        dialog.innerHTML = `
            <div class="dialog-content">
                <textarea id="messageText" placeholder="Enter your message"></textarea>
                <button id="sendMessageBtn">Send</button>
                <button id="cancelMessageBtn">Cancel</button>
            </div>
        `;
        document.body.appendChild(dialog);

        document.getElementById('sendMessageBtn').addEventListener('click', function() {
            const message = document.getElementById('messageText').value;
            sendMessage(studentId, message);
            document.body.removeChild(dialog);
        });

        document.getElementById('cancelMessageBtn').addEventListener('click', function() {
            document.body.removeChild(dialog);
        });
    }

    function deleteLesson(lessonId) {
        // Implement AJAX request to delete lesson
        console.log('Deleting lesson with ID:', lessonId);
    }

    function sendMessage(studentId, message) {
        // Implement AJAX request to send message
        console.log('Sending message to student with ID:', studentId, 'Message:', message);
    }

    function removeStudent(studentId) {
        // Implement AJAX request to remove student
        console.log('Removing student with ID:', studentId);
    }
});
