# app.py (cập nhật)
import json

from flask import Flask, render_template, request, send_file, jsonify
from gtts import gTTS
import io

import dao
from models import db, Group
from dao import seed_ipa_data, seed_flashcards

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    seed_ipa_data()  # Seed IPA nếu chưa có
    seed_flashcards()  # Seed flashcard nếu chưa có


@app.route('/')
def index():
    groups = Group.query.all()

    # Chuyển model thành dict để Jinja có thể tojson an toàn
    groups_data = []
    for group in groups:
        group_dict = {
            "id": group.id,
            "title": group.title,
            "items": []
        }
        for item in group.items:
            group_dict["items"].append({
                "id": item.id,
                "sound": item.sound,
                "words": item.words,
                "ipa": item.ipa,
                "guide": item.guide,
                "approx": item.approx
            })
        groups_data.append(group_dict)

    return render_template('ipa.html', groups=groups_data)

@app.route('/flashcard')
def flashcard():
    with open('data/flashcards.json', 'r', encoding='utf-8') as f:
        flashcards = json.load(f)
    return render_template('flashcard.html', flashcards=flashcards)

@app.route('/minimal-pairs')
def minimal_pairs():
    pairs = dao.load_minimal_pairs()
    return render_template('minimal_pairs.html', minimal_pairs=pairs)

@app.route('/tts')
def tts():
    text = request.args.get('text', '').strip()
    if not text:
        return "", 400
    tts = gTTS(text=text, lang='en', tld='co.uk', slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return send_file(fp, mimetype='audio/mp3')

@app.route('/flashcards', methods=['GET'])
def get_flashcards():
    flashcards = [ {'word': f.word, 'ipa': f.ipa, 'meaning': f.meaning} for f in load_flashcards() ]
    return jsonify(flashcards)

if __name__ == '__main__':
    app.run(debug=True)