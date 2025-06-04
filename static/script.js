document.addEventListener('DOMContentLoaded', () => {
    const notesList = document.getElementById('notes-list');

    notesList.addEventListener('click', (e) => {
        if (e.target.classList.contains('delete-btn')) {
            const noteDiv = e.target.closest('.note');
            const noteId = noteDiv.getAttribute('data-id');

            fetch(`/delete/${noteId}`, {
                method: 'POST',
            })
            .then(response => {
                if (response.ok) {
                    noteDiv.remove();
                } else {
                    alert('Failed to delete note.');
                }
            })
            .catch(() => alert('Network error.'));
        }
    });
});
