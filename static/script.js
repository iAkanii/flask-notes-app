document.addEventListener('DOMContentLoaded', () => {
    const notesList = document.getElementById('notes-list');

    notesList.addEventListener('click', (e) => {
        const noteDiv = e.target.closest('.note');
        const noteId = noteDiv?.getAttribute('data-id');

        // Удаление
        if (e.target.classList.contains('delete-btn')) {
            fetch(`/delete/${noteId}`, { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        noteDiv.remove();
                    } else {
                        alert('Failed to delete note.');
                    }
                })
                .catch(() => alert('Network error.'));
        }

        // Редактирование
        if (e.target.classList.contains('edit-btn')) {
            const titleEl = noteDiv.querySelector('h3');
            const contentEl = noteDiv.querySelector('p');

            const title = titleEl.textContent;
            const content = contentEl.textContent;

            noteDiv.innerHTML = `
                <input type="text" class="edit-title" value="${title}" /><br>
                <textarea class="edit-content">${content}</textarea><br>
                <button class="save-btn">Save</button>
                <button class="cancel-btn">Cancel</button>
            `;
        }

        // Сохранить редактирование
        if (e.target.classList.contains('save-btn')) {
            const newTitle = noteDiv.querySelector('.edit-title').value.trim();
            const newContent = noteDiv.querySelector('.edit-content').value.trim();

            fetch(`/edit/${noteId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title: newTitle, content: newContent })
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        noteDiv.innerHTML = `
                            <h3>${newTitle}</h3>
                            <p>${newContent}</p>
                            <button class="edit-btn">Edit</button>
                            <button class="delete-btn">Delete</button>
                        `;
                    } else {
                        alert('Update failed: ' + data.message);
                    }
                });
        }

        // Отмена редактирования
        if (e.target.classList.contains('cancel-btn')) {
            location.reload(); // просто перезагружаем, чтобы вернуть старое состояние
        }
    });
});
