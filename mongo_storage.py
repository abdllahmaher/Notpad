import os
from pymongo import MongoClient
from datetime import datetime

class MongoDBStorage:
    def __init__(self):
     
        mongo_url = os.environ.get('MONGODB_URL')
        
        if not mongo_url:
          
            print("⚠️ MONGODB_URL not found. Using temporary storage.")
            self.use_mongo = False
            self.local_data = {}
            return
        
        try:
            self.client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
            
            self.client.admin.command('ping')
            self.db = self.client['telegram_bot_db']
            self.use_mongo = True
            print("✅ Connected to MongoDB Atlas successfully!")
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            print("⚠️ Falling back to temporary storage")
            self.use_mongo = False
            self.local_data = {}
    
    def add_note(self, user_id, text):
        user_id = str(user_id)
        
        if self.use_mongo:
            try:
                self.db.notes.insert_one({
                    "user_id": user_id,
                    "text": text,
                    "created_at": datetime.now()
                })
                print(f"📝 Note saved to MongoDB for user {user_id}")
            except Exception as e:
                print(f"❌ Failed to save note: {e}")
                self._save_local(user_id, 'notes', text)
        else:
            self._save_local(user_id, 'notes', text)
    
    def get_notes(self, user_id):
        user_id = str(user_id)
        
        if self.use_mongo:
            try:
                notes = list(self.db.notes.find(
                    {"user_id": user_id}
                ).sort("created_at", -1))
                return [note["text"] for note in notes]
            except Exception as e:
                print(f"❌ Failed to get notes: {e}")
                return self.local_data.get(user_id, {}).get('notes', [])
        else:
            return self.local_data.get(user_id, {}).get('notes', [])
    
    def delete_note(self, user_id, index):
        user_id = str(user_id)
        
        if self.use_mongo:
            try:
                notes = list(self.db.notes.find(
                    {"user_id": user_id}
                ).sort("created_at", -1))
                
                if 0 < index <= len(notes):
                    note_id = notes[index-1]["_id"]
                    self.db.notes.delete_one({"_id": note_id})
                    return True
            except Exception as e:
                print(f"❌ Failed to delete note: {e}")
        
        # Fallback to local
        if user_id in self.local_data:
            notes = self.local_data[user_id].get('notes', [])
            if 0 < index <= len(notes):
                self.local_data[user_id]['notes'].pop(index-1)
                return True
        return False
    
    def add_todo(self, user_id, task):
        user_id = str(user_id)
        
        if self.use_mongo:
            try:
                self.db.todos.insert_one({
                    "user_id": user_id,
                    "task": task,
                    "done": False,
                    "created_at": datetime.now()
                })
                print(f"✅ Todo saved to MongoDB for user {user_id}")
            except Exception as e:
                print(f"❌ Failed to save todo: {e}")
                self._save_local_todo(user_id, task)
        else:
            self._save_local_todo(user_id, task)
    
    def get_todos(self, user_id):
        user_id = str(user_id)
        
        if self.use_mongo:
            try:
                todos = list(self.db.todos.find(
                    {"user_id": user_id}
                ).sort("created_at", -1))
                return [{"task": todo["task"], "done": todo["done"]} for todo in todos]
            except Exception as e:
                print(f"❌ Failed to get todos: {e}")
                return self.local_data.get(user_id, {}).get('todos', [])
        else:
            return self.local_data.get(user_id, {}).get('todos', [])
    
    def mark_done(self, user_id, index):
        user_id = str(user_id)
        
        if self.use_mongo:
            try:
                todos = list(self.db.todos.find(
                    {"user_id": user_id}
                ).sort("created_at", -1))
                
                if 0 <= index < len(todos):
                    todo_id = todos[index]["_id"]
                    self.db.todos.update_one(
                        {"_id": todo_id},
                        {"$set": {"done": True}}
                    )
                    return True
            except Exception as e:
                print(f"❌ Failed to mark todo done: {e}")
        
        # Fallback to local
        if user_id in self.local_data:
            todos = self.local_data[user_id].get('todos', [])
            if 0 <= index < len(todos):
                todos[index]["done"] = True
                return True
        return False
    
    def delete_todo(self, user_id, index):
        # Similar to delete_note but for todos
        user_id = str(user_id)
        
        if self.use_mongo:
            try:
                todos = list(self.db.todos.find(
                    {"user_id": user_id}
                ).sort("created_at", -1))
                
                if 0 < index <= len(todos):
                    todo_id = todos[index-1]["_id"]
                    self.db.todos.delete_one({"_id": todo_id})
                    return True
            except Exception as e:
                print(f"❌ Failed to delete todo: {e}")
        
        # Fallback to local
        if user_id in self.local_data:
            todos = self.local_data[user_id].get('todos', [])
            if 0 < index <= len(todos):
                self.local_data[user_id]['todos'].pop(index-1)
                return True
        return False
    
    def _save_local(self, user_id, type_, content):
        """local as fallback"""
        if user_id not in self.local_data:
            self.local_data[user_id] = {'notes': [], 'todos': []}
        
        if type_ == 'notes':
            self.local_data[user_id]['notes'].append(content)
        elif type_ == 'todos':
            self.local_data[user_id]['todos'].append({"task": content, "done": False})
    
    def _save_local_todo(self, user_id, task):
        if user_id not in self.local_data:
            self.local_data[user_id] = {'notes': [], 'todos': []}
        self.local_data[user_id]['todos'].append({"task": task, "done": False})


db = MongoDBStorage()