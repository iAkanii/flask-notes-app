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

# Delete Note
@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
        print(f"Deleted note {note_id}")
        return jsonify({'success': True})
    print(f"Note {note_id} not found")
    return jsonify({'success': False}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
