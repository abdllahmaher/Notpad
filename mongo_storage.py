import os
from pymongo import MongoClient
import certifi
import urllib.parse

def get_mongo_client():
    """الحصول على عميل MongoDB مع إصلاح SSL"""
    # اقرأ connection string من environment variable
    mongo_uri = os.environ.get("MONGODB_URI")
    
    if not mongo_uri:
        print("⚠️ MONGODB_URI not found, using temporary storage")
        return None
    
    try:
        # إضافة options لإصلاح SSL
        if "ssl=true" not in mongo_uri.lower():
            if "?" in mongo_uri:
                mongo_uri += "&ssl=true&tls=true"
            else:
                mongo_uri += "?ssl=true&tls=true"
        
        # إضافة SSL certificate authority
        mongo_uri += "&tlsCAFile=" + urllib.parse.quote(certifi.where())
        
        # خيارات إضافية لـ Choreo
        options = {
            "serverSelectionTimeoutMS": 10000,
            "connectTimeoutMS": 10000,
            "socketTimeoutMS": 20000,
            "retryWrites": True,
            "w": "majority"
        }
        
        client = MongoClient(mongo_uri, **options)
        
        # اختبار الاتصال
        client.admin.command('ping')
        print("✅ MongoDB connection successful")
        return client
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None

# إنشاء العميل
client = get_mongo_client()

if client:
    db = client.get_database("telegram_bot")
    notes_collection = db.notes
    todos_collection = db.todos
else:
    # Fallback إلى SQLite
    print("🔄 Falling back to SQLite storage")
    from database import get_connection as db
    notes_collection = None
    todos_collection = None
