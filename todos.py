# from storage import load_data, save_data

# def add_todo(user_id, task):
#     data = load_data()
#     user = data.setdefault(str(user_id), {"notes": [], "todos": []})
#     user["todos"].append({"task": task, "done": False})
#     save_data(data)

# def list_todos(user_id):
#     data = load_data()
#     return data.get(str(user_id), {}).get("todos", [])

# def mark_done(user_id, index):
#     data = load_data()
#     user = data.get(str(user_id))
#     if user and 0 <= index < len(user["todos"]):
#         user["todos"][index]["done"] = True
#         save_data(data)
#         return True
#     return False


# def delete_task(user_id, index):
#     data = load_data()
#     user = data.get(str(user_id))
    
#     if not user:
#         return False
    
#     todos = user.get("todos", [])
#     if index is None or not (0 < index <= len(todos)):
#         return False
#     user["todos"].pop(index-1)
    
#     save_data(data)
#     return True


# def delete_all_tasks(user_id):
#     data = load_data()
#     user = data.get(str(user_id))
    
#     if not user:
#         return False
#     if user["todos"] == []:
#         return False
#     user["todos"] = []
#     save_data(data)
#     return True

from mongo_storage import db

def add_todo(user_id, task):
    db.add_todo(user_id, task)

def list_todos(user_id):
    return db.get_todos(user_id)

def mark_done(user_id, index):
    return db.mark_done(user_id, index)

def delete_task(user_id, index):
    return db.delete_todo(user_id, index)

def delete_all_tasks(user_id):
    # Similar to delete_all in notes
    todos = list_todos(user_id)
    if not todos:
        return False
    
    user_id = str(user_id)
    try:
        from mongo_storage import db
        if db.use_mongo:
            db.db.todos.delete_many({"user_id": user_id})
            return True
        else:
            if user_id in db.local_data:
                db.local_data[user_id]['todos'] = []
                return True
    except:
        pass
    return False