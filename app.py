from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)

# Main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title or len(title) > 100 or len(content) < 5:
            return redirect('/')

        new_note = Note(title=title, content=content)
        db.session.add(new_note)
        db.session.commit()
        return redirect('/')

    notes = Note.query.all()
    return render_template('index.html', notes=notes)

# Delete note
@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

# Edit note
@app.route('/edit/<int:note_id>', methods=['POST'])
def edit_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'success': False, 'message': 'Note not found'}), 404

    data = request.get_json()
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title or len(title) > 100 or len(content) < 5:
        return jsonify({'success': False, 'message': 'Invalid input'}), 400

    note.title = title
    note.content = content
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
