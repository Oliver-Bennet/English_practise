# dao.py (mới)
import json
from models import db, Group, Item, Flashcard

def seed_json(json_path, model_class, transform=None):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        if transform:
            item = transform(item)
        obj = model_class(**item)
        db.session.add(obj)
    db.session.commit()

def seed_ipa_data():
    with open("data/ipa_data.json", encoding="utf-8") as f:
        data = json.load(f)

    for group_id, group_data in data.items():
        # Kiểm tra xem group đã tồn tại chưa
        existing_group = Group.query.get(group_id)
        if existing_group:
            continue  # Bỏ qua nếu đã có

        group = Group(id=group_id, title=group_data['title'])
        db.session.add(group)

        for item_data in group_data['items']:
            # Thêm group_id vào item_data
            item_data['group_id'] = group_id
            item = Item(**item_data)
            db.session.add(item)

    db.session.commit()
    print("IPA data seeded successfully (or already exists)!")

def seed_flashcards():
    seed_json("data/flashcards.json", Flashcard)

def load_flashcards():
    return Flashcard.query.all()