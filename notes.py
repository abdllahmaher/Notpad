# from storage import load_data, save_data

# def add_note(user_id, text):
#     data = load_data()
#     user = data.setdefault(str(user_id), {"notes": [], "todos": []})
#     user["notes"].append(text)
#     save_data(data)

# def list_notes(user_id):
#     data = load_data()
#     return data.get(str(user_id), {}).get("notes", [])

# def delete_note(user_id, index):
#     data = load_data()
#     user = data.get(str(user_id))
    
#     if not user:
#         return False
    
#     notes = user.get("notes", [])
#     if index is None or not (0 < index <= len(notes)):
#         return False
#     if user["notes"][index-1]==[]:
#         return False
#     user["notes"].pop(index-1)
    
#     save_data(data)
#     return True


# def delete_all(user_id):
#     data = load_data()
#     user = data.get(str(user_id))
    
#     if not user:
#         return False
#     if user["notes"] == []:
#         return False
#     user["notes"] = []
#     save_data(data)
#     return True

from mongo_storage import db

def add_note(user_id, text):
    db.add_note(user_id, text)

def list_notes(user_id):
    return db.get_notes(user_id)

def delete_note(user_id, index):
    return db.delete_note(user_id, index)

def delete_all(user_id):
    # Note: For MongoDB, we'll delete all notes for user
    # This is a simple implementation
    notes = list_notes(user_id)
    if not notes:
        return False
    
    # Delete one by one (for now)
    user_id = str(user_id)
    try:
        from mongo_storage import db
        if db.use_mongo:
            db.db.notes.delete_many({"user_id": user_id})
            return True
        else:
            # Local fallback
            if user_id in db.local_data:
                db.local_data[user_id]['notes'] = []
                return True
    except:
        pass
    return False