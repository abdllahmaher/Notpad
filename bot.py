# import os
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import (
#     ApplicationBuilder,
#     CommandHandler,
#     CallbackQueryHandler,
#     ContextTypes,
#     MessageHandler,
#     filters
# )

# from notes import add_note, list_notes, delete_note, delete_all
# from todos import add_todo, list_todos, mark_done, delete_task, delete_all_tasks

# # ============ TOKEN ============
# TOKEN = os.environ.get('TOKEN')

# if not TOKEN:
#     print("❌ ERROR: TOKEN not found!")
#     print("For Render: Add TOKEN to Environment Variables")
#     print("For local: Create .env file with TOKEN=your_token")
#     exit(1)

# print(f"✅ Token loaded: {TOKEN[:10]}...")
# # ============  TOKEN ============


# user_states = {}

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("📝 Notes", callback_data="menu_notes")],
#         [InlineKeyboardButton("✅ Todos", callback_data="menu_todos")],
#         [InlineKeyboardButton("ℹ️ Help", callback_data="menu_help")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     welcome_text = """
# ✨ *Welcome to Notepad Bot* ✨

# Manage your notes and todos efficiently with a beautiful interface!

# *Main Features:*
# 📝 **Notes** - Quick notes with formatting
# ✅ **Todos** - Task management with checkboxes
# 🗑️ **Easy Management** - Add, view, delete with one click

# Click the buttons below to get started!
# """
    
#     await update.message.reply_text(
#         welcome_text,
#         reply_markup=reply_markup,
#         parse_mode='Markdown'
#     )

# async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
    
#     user_id = str(query.from_user.id)
#     data = query.data
    
#     if data == "menu_notes":
#         await show_notes_menu(query)
#     elif data == "menu_todos":
#         await show_todos_menu(query)
#     elif data == "menu_help":
#         await show_help_menu(query)
#     elif data == "notes_view":
#         await view_notes(query)
#     elif data == "notes_add":
#         user_states[user_id] = {"action": "add_note"}
#         await query.edit_message_text(
#             "📝 *Add a New Note*\n\nPlease send me your note text:",
#             parse_mode='Markdown'
#         )
#     elif data == "notes_delete":
#         await show_delete_note_menu(query)
#     elif data == "notes_clear":
#         await clear_notes_confirm(query)
#     elif data.startswith("delete_note_"):
#         note_id = int(data.split("_")[2])
#         if delete_note(query.from_user.id, note_id):
#             await query.edit_message_text("✅ Note deleted successfully!")
#         else:
#             await query.edit_message_text("❌ Invalid note number!")
#         await show_notes_menu(query, new_message=True)
#     elif data == "confirm_clear_notes":
#         if delete_all(query.from_user.id):
#             await query.edit_message_text("🗑️ All notes cleared successfully!")
#         else:
#             await query.edit_message_text("ℹ️ No notes to clear!")
#         await show_notes_menu(query, new_message=True)
#     elif data == "cancel_clear_notes":
#         await query.edit_message_text("Clear notes operation cancelled!")
#         await show_notes_menu(query, new_message=True)
#     elif data == "todos_view":
#         await view_todos(query)
#     elif data == "todos_add":
#         user_states[user_id] = {"action": "add_todo"}
#         await query.edit_message_text(
#             "✅ *Add a New Task*\n\nPlease send me your task:",
#             parse_mode='Markdown'
#         )
#     elif data == "todos_mark":
#         await show_mark_todo_menu(query)
#     elif data == "todos_delete":
#         await show_delete_todo_menu(query)
#     elif data == "todos_clear":
#         await clear_todos_confirm(query)
#     elif data.startswith("mark_todo_"):
#         todo_id = int(data.split("_")[2])
#         if mark_done(query.from_user.id, todo_id - 1):
#             await query.edit_message_text(f"✅ Task {todo_id} marked as done!")
#         else:
#             await query.edit_message_text("❌ Invalid task number!")
#         await show_todos_menu(query, new_message=True)
#     elif data.startswith("delete_todo_"):
#         todo_id = int(data.split("_")[2])
#         if delete_task(query.from_user.id, todo_id):
#             await query.edit_message_text(f"✅ Task {todo_id} deleted!")
#         else:
#             await query.edit_message_text("❌ Invalid task number!")
#         await show_todos_menu(query, new_message=True)
#     elif data == "confirm_clear_todos":
#         if delete_all_tasks(query.from_user.id):
#             await query.edit_message_text("🗑️ All tasks cleared successfully!")
#         else:
#             await query.edit_message_text("ℹ️ No tasks to clear!")
#         await show_todos_menu(query, new_message=True)
#     elif data == "cancel_clear_todos":
#         await query.edit_message_text("Clear tasks operation cancelled!")
#         await show_todos_menu(query, new_message=True)
#     elif data == "back_main":
#         await show_main_menu(query)
#     elif data == "back_notes":
#         await show_notes_menu(query)
#     elif data == "back_todos":
#         await show_todos_menu(query)

# async def show_main_menu(query):
#     keyboard = [
#         [InlineKeyboardButton("📝 Notes", callback_data="menu_notes")],
#         [InlineKeyboardButton("✅ Todos", callback_data="menu_todos")],
#         [InlineKeyboardButton("ℹ️ Help", callback_data="menu_help")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     await query.edit_message_text(
#         "✨ *Main Menu* ✨\n\nSelect an option:",
#         reply_markup=reply_markup,
#         parse_mode='Markdown'
#     )

# async def show_notes_menu(query, new_message=False):
#     keyboard = [
#         [InlineKeyboardButton("📋 View Notes", callback_data="notes_view")],
#         [InlineKeyboardButton("➕ Add Note", callback_data="notes_add")],
#         [InlineKeyboardButton("🗑️ Delete Note", callback_data="notes_delete")],
#         [InlineKeyboardButton("🧹 Clear All Notes", callback_data="notes_clear")],
#         [InlineKeyboardButton("🔙 Back to Main", callback_data="back_main")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     text = "📝 *Notes Menu*\n\nSelect an action:"
    
#     if new_message:
#         await query.message.reply_text(
#             text,
#             reply_markup=reply_markup,
#             parse_mode='Markdown'
#         )
#     else:
#         await query.edit_message_text(
#             text,
#             reply_markup=reply_markup,
#             parse_mode='Markdown'
#         )

# async def show_todos_menu(query, new_message=False):
#     keyboard = [
#         [InlineKeyboardButton("📋 View Tasks", callback_data="todos_view")],
#         [InlineKeyboardButton("➕ Add Task", callback_data="todos_add")],
#         [InlineKeyboardButton("✅ Mark Done", callback_data="todos_mark")],
#         [InlineKeyboardButton("🗑️ Delete Task", callback_data="todos_delete")],
#         [InlineKeyboardButton("🧹 Clear All Tasks", callback_data="todos_clear")],
#         [InlineKeyboardButton("🔙 Back to Main", callback_data="back_main")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     text = "✅ *Todos Menu*\n\nSelect an action:"
    
#     if new_message:
#         await query.message.reply_text(
#             text,
#             reply_markup=reply_markup,
#             parse_mode='Markdown'
#         )
#     else:
#         await query.edit_message_text(
#             text,
#             reply_markup=reply_markup,
#             parse_mode='Markdown'
#         )

# async def show_help_menu(query):
#     help_text = """
# *📚 Help Guide*

# *Commands:*
# /start - Show main menu
# /help - Show this help message

# *Notes Features:*
# • Add unlimited notes
# • View all notes in formatted list
# • Delete specific notes
# • Clear all notes at once

# *Todos Features:*
# • Add tasks with status tracking
# • Mark tasks as done
# • Delete specific tasks
# • Clear all tasks

# *How to Use:*
# 1. Use the inline buttons to navigate
# 2. When adding notes/tasks, just type your text
# 3. Select from lists using number buttons
# 4. Confirm deletions when prompted

# *Tips:*
# • Use emojis to make your notes more visual ✨
# • Keep tasks concise for better management
# • Regularly clear completed tasks
# """
    
#     keyboard = [[InlineKeyboardButton("🔙 Back to Main", callback_data="back_main")]]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     await query.edit_message_text(
#         help_text,
#         reply_markup=reply_markup,
#         parse_mode='Markdown'
#     )

# async def view_notes(query):
#     notes = list_notes(query.from_user.id)
    
#     if not notes:
#         keyboard = [[InlineKeyboardButton("➕ Add Note", callback_data="notes_add")],
#                    [InlineKeyboardButton("🔙 Back", callback_data="back_notes")]]
#         reply_markup = InlineKeyboardMarkup(keyboard)
        
#         await query.edit_message_text(
#             "📭 *No Notes Found*\n\nYou don't have any notes yet. Add your first note!",
#             reply_markup=reply_markup,
#             parse_mode='Markdown'
#         )
#         return
    
#     notes_text = "📓 *Your Notes*\n\n"
    
#     for i, note in enumerate(notes, 1):
#         note = note.replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
        
#         display_note = note if len(note) < 100 else note[:97] + "..."
        
#         notes_text += f"*{i}.* `{display_note}`\n"
        
#         if len(note) >= 100:
#             notes_text += "   └─ *...continued*\n"
        
#         notes_text += f"   └─ 📝 {len(note)} characters\n\n"
    
#     keyboard = [
#         [InlineKeyboardButton("➕ Add More", callback_data="notes_add")],
#         [InlineKeyboardButton("🗑️ Delete Note", callback_data="notes_delete")],
#         [InlineKeyboardButton("🔙 Back", callback_data="back_notes")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     if len(notes_text) > 4000:
#         notes_text = notes_text[:4000] + "\n\n*⚠️ Note:* Some notes were truncated due to message length limit."
    
#     await query.edit_message_text(
#         notes_text,
#         reply_markup=reply_markup,
#         parse_mode='Markdown'
#     )

# async def view_todos(query):
#     todos = list_todos(query.from_user.id)
    
#     if not todos:
#         keyboard = [[InlineKeyboardButton("➕ Add Task", callback_data="todos_add")],
#                    [InlineKeyboardButton("🔙 Back", callback_data="back_todos")]]
#         reply_markup = InlineKeyboardMarkup(keyboard)
        
#         await query.edit_message_text(
#             "📭 *No Tasks Found*\n\nYou don't have any tasks yet. Add your first task!",
#             reply_markup=reply_markup,
#             parse_mode='Markdown'
#         )
#         return
    
#     todos_text = "✅ *Your Tasks*\n\n"
    
#     completed = sum(1 for t in todos if t['done'])
#     total = len(todos)
    
#     todos_text += f"📊 *Progress:* {completed}/{total} completed\n\n"
    
#     for i, todo in enumerate(todos, 1):
#         status = "✅" if todo['done'] else "⏳"
#         task_text = f"~~{todo['task']}~~" if todo['done'] else todo['task']
#         todos_text += f"*{i}.* {status} {task_text}\n"
    
#     keyboard = [
#         [InlineKeyboardButton("➕ Add More", callback_data="todos_add")],
#         [InlineKeyboardButton("✅ Mark Done", callback_data="todos_mark")],
#         [InlineKeyboardButton("🗑️ Delete Task", callback_data="todos_delete")],
#         [InlineKeyboardButton("🔙 Back", callback_data="back_todos")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     await query.edit_message_text(
#         todos_text,
#         reply_markup=reply_markup,
#         parse_mode='Markdown'
#     )

# async def show_delete_note_menu(query):
#     notes = list_notes(query.from_user.id)
    
#     if not notes:
#         await query.edit_message_text("No notes to delete!")
#         await show_notes_menu(query, new_message=True)
#         return
    
#     keyboard = []
#     row = []
#     for i in range(1, len(notes) + 1):
#         row.append(InlineKeyboardButton(f"{i}", callback_data=f"delete_note_{i}"))
#         if len(row) == 3:
#             keyboard.append(row)
#             row = []
#     if row:
#         keyboard.append(row)
#     keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_notes")])
    
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     await query.edit_message_text(
#         "🗑️ *Delete Note*\n\nSelect the note number to delete:",
#         reply_markup=reply_markup,
#         parse_mode='Markdown'
#     )

# async def show_delete_todo_menu(query):
#     todos = list_todos(query.from_user.id)
    
#     if not todos:
#         await query.edit_message_text("No tasks to delete!")
#         await show_todos_menu(query, new_message=True)
#         return
    
#     keyboard = []
#     row = []
#     for i in range(1, len(todos) + 1):
#         row.append(InlineKeyboardButton(f"{i}", callback_data=f"delete_todo_{i}"))
#         if len(row) == 3:
#             keyboard.append(row)
#             row = []
#     if row:
#         keyboard.append(row)
#     keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_todos")])
    
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     await query.edit_message_text(
#         "🗑️ *Delete Task*\n\nSelect the task number to delete:",
#         reply_markup=reply_markup,
#         parse_mode='Markdown'
#     )

# async def show_mark_todo_menu(query):
#     todos = list_todos(query.from_user.id)
    
#     if not todos:
#         await query.edit_message_text("No tasks to mark!")
#         await show_todos_menu(query, new_message=True)
#         return
    
#     pending = [i for i, t in enumerate(todos, 1) if not t['done']]
    
#     if not pending:
#         await query.edit_message_text("All tasks are already completed! 🎉")
#         await show_todos_menu(query, new_message=True)
#         return
    
#     keyboard = []
#     row = []
#     for i in pending:
#         row.append(InlineKeyboardButton(f"{i}", callback_data=f"mark_todo_{i}"))
#         if len(row) == 3:
#             keyboard.append(row)
#             row = []
#     if row:
#         keyboard.append(row)
#     keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_todos")])
    
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     await query.edit_message_text(
#         "✅ *Mark Task as Done*\n\nSelect the task number to mark as done:",
#         reply_markup=reply_markup,
#         parse_mode='Markdown'
#     )

# async def clear_notes_confirm(query):
#     keyboard = [
#         [
#             InlineKeyboardButton("✅ Yes, Clear All", callback_data="confirm_clear_notes"),
#             InlineKeyboardButton("❌ No, Cancel", callback_data="cancel_clear_notes")
#         ],
#         [InlineKeyboardButton("🔙 Back", callback_data="back_notes")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     await query.edit_message_text(
#         "⚠️ *Clear All Notes*\n\nAre you sure you want to delete ALL notes?\nThis action cannot be undone!",
#         reply_markup=reply_markup,
#         parse_mode='Markdown'
#     )

# async def clear_todos_confirm(query):
#     keyboard = [
#         [
#             InlineKeyboardButton("✅ Yes, Clear All", callback_data="confirm_clear_todos"),
#             InlineKeyboardButton("❌ No, Cancel", callback_data="cancel_clear_todos")
#         ],
#         [InlineKeyboardButton("🔙 Back", callback_data="back_todos")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     await query.edit_message_text(
#         "⚠️ *Clear All Tasks*\n\nAre you sure you want to delete ALL tasks?\nThis action cannot be undone!",
#         reply_markup=reply_markup,
#         parse_mode='Markdown'
#     )

# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = str(update.effective_user.id)
#     text = update.message.text
    
#     if user_id in user_states:
#         action = user_states[user_id].get("action")
        
#         if action == "add_note":
#             add_note(update.effective_user.id, text)
            
#             keyboard = [[InlineKeyboardButton("📋 View Notes", callback_data="notes_view")],
#                        [InlineKeyboardButton("🔙 Back to Notes", callback_data="back_notes")]]
#             reply_markup = InlineKeyboardMarkup(keyboard)
            
#             await update.message.reply_text(
#                 "✅ *Note Added Successfully!*\n\nYour note has been saved.",
#                 reply_markup=reply_markup,
#                 parse_mode='Markdown'
#             )
#             del user_states[user_id]
            
#         elif action == "add_todo":
#             add_todo(update.effective_user.id, text)
            
#             keyboard = [[InlineKeyboardButton("📋 View Tasks", callback_data="todos_view")],
#                        [InlineKeyboardButton("🔙 Back to Todos", callback_data="back_todos")]]
#             reply_markup = InlineKeyboardMarkup(keyboard)
            
#             await update.message.reply_text(
#                 "✅ *Task Added Successfully!*\n\nYour task has been saved.",
#                 reply_markup=reply_markup,
#                 parse_mode='Markdown'
#             )
#             del user_states[user_id]
#     else:
#         await show_main_menu_direct(update)

# async def show_main_menu_direct(update: Update):
#     keyboard = [
#         [InlineKeyboardButton("📝 Notes", callback_data="menu_notes")],
#         [InlineKeyboardButton("✅ Todos", callback_data="menu_todos")],
#         [InlineKeyboardButton("ℹ️ Help", callback_data="menu_help")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     await update.message.reply_text(
#         "✨ *Main Menu* ✨\n\nSelect an option:",
#         reply_markup=reply_markup,
#         parse_mode='Markdown'
#     )

# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [[InlineKeyboardButton("🔙 Back to Main", callback_data="back_main")]]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     help_text = """
# *📚 Help Guide*

# *Commands:*
# /start - Show main menu
# /help - Show this help message

# *Navigation:*
# Use the inline buttons to navigate through the menu. No need to type commands!

# *Quick Actions:*
# 1. Tap buttons to perform actions
# 2. Type text when prompted
# 3. Select from numbered lists
# 4. Confirm important actions

# Need more help? Just explore the menus!
# """
    
#     await update.message.reply_text(
#         help_text,
#         reply_markup=reply_markup,
#         parse_mode='Markdown'
#     )

# def main():
    
#     app = ApplicationBuilder().token(TOKEN).build()
    
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CommandHandler("help", help_command))
    
#     app.add_handler(CallbackQueryHandler(button_callback))
    
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
#     app.add_handler(CommandHandler("note", note_cmd))
#     app.add_handler(CommandHandler("notes", notes_cmd))
#     app.add_handler(CommandHandler("todo", todo_cmd))
#     app.add_handler(CommandHandler("todos", todos_cmd))
#     app.add_handler(CommandHandler("done", done_cmd))
#     app.add_handler(CommandHandler("deleteNote", dlnt_cmd))
#     app.add_handler(CommandHandler("deleteTask", dltsk_cmd))
#     app.add_handler(CommandHandler("clearNotes", clrnt_cmd))
#     app.add_handler(CommandHandler("clearTodo", clrtsk_cmd))
    
#     print("Bot is starting...")
#     app.run_polling()

# async def note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await show_main_menu_direct(update)

# async def notes_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await show_main_menu_direct(update)

# async def todo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await show_main_menu_direct(update)

# async def todos_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await show_main_menu_direct(update)

# async def done_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await show_main_menu_direct(update)

# async def dlnt_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await show_main_menu_direct(update)

# async def dltsk_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await show_main_menu_direct(update)

# async def clrnt_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await show_main_menu_direct(update)

# async def clrtsk_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await show_main_menu_direct(update)

# if __name__ == "__main__":
#     main()
import os
import threading
import time
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from notes import add_note, list_notes, delete_note, delete_all
from todos import add_todo, list_todos, mark_done, delete_task, delete_all_tasks

# ============ TOKEN ============
TOKEN = os.environ.get('TOKEN')

if not TOKEN:
    print("❌ ERROR: TOKEN not found!")
    print("For Render: Add TOKEN to Environment Variables")
    print("For local: Create .env file with TOKEN=your_token")
    exit(1)

print(f"✅ Token loaded: {TOKEN[:10]}...")
# ============  TOKEN ============

# ============ KEEP ALIVE FUNCTION ============
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def keep_alive_background():
    while True:
        try:
            app_url = os.environ.get('APP_URL', 'https://your-bot-name.cherno.dev')
            
            try:
                response = requests.get(app_url, timeout=10)
                print(f"[{get_current_time()}] Keep-alive ping sent. Status: {response.status_code}")
            except:
                print(f"[{get_current_time()}] Keep-alive ping failed")
                
        except Exception as e:
            print(f"[{get_current_time()}] Keep-alive error: {e}")
        
        time.sleep(7200)
# ============ END KEEP ALIVE ============

user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📝 Notes", callback_data="menu_notes")],
        [InlineKeyboardButton("✅ Todos", callback_data="menu_todos")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="menu_help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = """
✨ *Welcome to Notepad Bot* ✨

Manage your notes and todos efficiently with a beautiful interface!

*Main Features:*
📝 **Notes** - Quick notes with formatting
✅ **Todos** - Task management with checkboxes
🗑️ **Easy Management** - Add, view, delete with one click

Click the buttons below to get started!
"""
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    data = query.data
    
    if data == "menu_notes":
        await show_notes_menu(query)
    elif data == "menu_todos":
        await show_todos_menu(query)
    elif data == "menu_help":
        await show_help_menu(query)
    elif data == "notes_view":
        await view_notes(query)
    elif data == "notes_add":
        user_states[user_id] = {"action": "add_note"}
        await query.edit_message_text(
            "📝 *Add a New Note*\n\nPlease send me your note text:",
            parse_mode='Markdown'
        )
    elif data == "notes_delete":
        await show_delete_note_menu(query)
    elif data == "notes_clear":
        await clear_notes_confirm(query)
    elif data.startswith("delete_note_"):
        note_id = int(data.split("_")[2])
        if delete_note(query.from_user.id, note_id):
            await query.edit_message_text("✅ Note deleted successfully!")
        else:
            await query.edit_message_text("❌ Invalid note number!")
        await show_notes_menu(query, new_message=True)
    elif data == "confirm_clear_notes":
        if delete_all(query.from_user.id):
            await query.edit_message_text("🗑️ All notes cleared successfully!")
        else:
            await query.edit_message_text("ℹ️ No notes to clear!")
        await show_notes_menu(query, new_message=True)
    elif data == "cancel_clear_notes":
        await query.edit_message_text("Clear notes operation cancelled!")
        await show_notes_menu(query, new_message=True)
    elif data == "todos_view":
        await view_todos(query)
    elif data == "todos_add":
        user_states[user_id] = {"action": "add_todo"}
        await query.edit_message_text(
            "✅ *Add a New Task*\n\nPlease send me your task:",
            parse_mode='Markdown'
        )
    elif data == "todos_mark":
        await show_mark_todo_menu(query)
    elif data == "todos_delete":
        await show_delete_todo_menu(query)
    elif data == "todos_clear":
        await clear_todos_confirm(query)
    elif data.startswith("mark_todo_"):
        todo_id = int(data.split("_")[2])
        if mark_done(query.from_user.id, todo_id - 1):
            await query.edit_message_text(f"✅ Task {todo_id} marked as done!")
        else:
            await query.edit_message_text("❌ Invalid task number!")
        await show_todos_menu(query, new_message=True)
    elif data.startswith("delete_todo_"):
        todo_id = int(data.split("_")[2])
        if delete_task(query.from_user.id, todo_id):
            await query.edit_message_text(f"✅ Task {todo_id} deleted!")
        else:
            await query.edit_message_text("❌ Invalid task number!")
        await show_todos_menu(query, new_message=True)
    elif data == "confirm_clear_todos":
        if delete_all_tasks(query.from_user.id):
            await query.edit_message_text("🗑️ All tasks cleared successfully!")
        else:
            await query.edit_message_text("ℹ️ No tasks to clear!")
        await show_todos_menu(query, new_message=True)
    elif data == "cancel_clear_todos":
        await query.edit_message_text("Clear tasks operation cancelled!")
        await show_todos_menu(query, new_message=True)
    elif data == "back_main":
        await show_main_menu(query)
    elif data == "back_notes":
        await show_notes_menu(query)
    elif data == "back_todos":
        await show_todos_menu(query)

async def show_main_menu(query):
    keyboard = [
        [InlineKeyboardButton("📝 Notes", callback_data="menu_notes")],
        [InlineKeyboardButton("✅ Todos", callback_data="menu_todos")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="menu_help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "✨ *Main Menu* ✨\n\nSelect an option:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_notes_menu(query, new_message=False):
    keyboard = [
        [InlineKeyboardButton("📋 View Notes", callback_data="notes_view")],
        [InlineKeyboardButton("➕ Add Note", callback_data="notes_add")],
        [InlineKeyboardButton("🗑️ Delete Note", callback_data="notes_delete")],
        [InlineKeyboardButton("🧹 Clear All Notes", callback_data="notes_clear")],
        [InlineKeyboardButton("🔙 Back to Main", callback_data="back_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "📝 *Notes Menu*\n\nSelect an action:"
    
    if new_message:
        await query.message.reply_text(
            text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def show_todos_menu(query, new_message=False):
    keyboard = [
        [InlineKeyboardButton("📋 View Tasks", callback_data="todos_view")],
        [InlineKeyboardButton("➕ Add Task", callback_data="todos_add")],
        [InlineKeyboardButton("✅ Mark Done", callback_data="todos_mark")],
        [InlineKeyboardButton("🗑️ Delete Task", callback_data="todos_delete")],
        [InlineKeyboardButton("🧹 Clear All Tasks", callback_data="todos_clear")],
        [InlineKeyboardButton("🔙 Back to Main", callback_data="back_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "✅ *Todos Menu*\n\nSelect an action:"
    
    if new_message:
        await query.message.reply_text(
            text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def show_help_menu(query):
    help_text = """
*📚 Help Guide*

*Commands:*
/start - Show main menu
/help - Show this help message

*Notes Features:*
• Add unlimited notes
• View all notes in formatted list
• Delete specific notes
• Clear all notes at once

*Todos Features:*
• Add tasks with status tracking
• Mark tasks as done
• Delete specific tasks
• Clear all tasks

*How to Use:*
1. Use the inline buttons to navigate
2. When adding notes/tasks, just type your text
3. Select from lists using number buttons
4. Confirm deletions when prompted

*Tips:*
• Use emojis to make your notes more visual ✨
• Keep tasks concise for better management
• Regularly clear completed tasks
"""
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Main", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        help_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def view_notes(query):
    notes = list_notes(query.from_user.id)
    
    if not notes:
        keyboard = [[InlineKeyboardButton("➕ Add Note", callback_data="notes_add")],
                   [InlineKeyboardButton("🔙 Back", callback_data="back_notes")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📭 *No Notes Found*\n\nYou don't have any notes yet. Add your first note!",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    notes_text = "📓 *Your Notes*\n\n"
    
    for i, note in enumerate(notes, 1):
        note = note.replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
        
        display_note = note if len(note) < 100 else note[:97] + "..."
        
        notes_text += f"*{i}.* `{display_note}`\n"
        
        if len(note) >= 100:
            notes_text += "   └─ *...continued*\n"
        
        notes_text += f"   └─ 📝 {len(note)} characters\n\n"
    
    keyboard = [
        [InlineKeyboardButton("➕ Add More", callback_data="notes_add")],
        [InlineKeyboardButton("🗑️ Delete Note", callback_data="notes_delete")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_notes")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if len(notes_text) > 4000:
        notes_text = notes_text[:4000] + "\n\n*⚠️ Note:* Some notes were truncated due to message length limit."
    
    await query.edit_message_text(
        notes_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def view_todos(query):
    todos = list_todos(query.from_user.id)
    
    if not todos:
        keyboard = [[InlineKeyboardButton("➕ Add Task", callback_data="todos_add")],
                   [InlineKeyboardButton("🔙 Back", callback_data="back_todos")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📭 *No Tasks Found*\n\nYou don't have any tasks yet. Add your first task!",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    todos_text = "✅ *Your Tasks*\n\n"
    
    completed = sum(1 for t in todos if t['done'])
    total = len(todos)
    
    todos_text += f"📊 *Progress:* {completed}/{total} completed\n\n"
    
    for i, todo in enumerate(todos, 1):
        status = "✅" if todo['done'] else "⏳"
        task_text = f"~~{todo['task']}~~" if todo['done'] else todo['task']
        todos_text += f"*{i}.* {status} {task_text}\n"
    
    keyboard = [
        [InlineKeyboardButton("➕ Add More", callback_data="todos_add")],
        [InlineKeyboardButton("✅ Mark Done", callback_data="todos_mark")],
        [InlineKeyboardButton("🗑️ Delete Task", callback_data="todos_delete")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_todos")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        todos_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_delete_note_menu(query):
    notes = list_notes(query.from_user.id)
    
    if not notes:
        await query.edit_message_text("No notes to delete!")
        await show_notes_menu(query, new_message=True)
        return
    
    keyboard = []
    row = []
    for i in range(1, len(notes) + 1):
        row.append(InlineKeyboardButton(f"{i}", callback_data=f"delete_note_{i}"))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_notes")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🗑️ *Delete Note*\n\nSelect the note number to delete:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_delete_todo_menu(query):
    todos = list_todos(query.from_user.id)
    
    if not todos:
        await query.edit_message_text("No tasks to delete!")
        await show_todos_menu(query, new_message=True)
        return
    
    keyboard = []
    row = []
    for i in range(1, len(todos) + 1):
        row.append(InlineKeyboardButton(f"{i}", callback_data=f"delete_todo_{i}"))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_todos")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🗑️ *Delete Task*\n\nSelect the task number to delete:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_mark_todo_menu(query):
    todos = list_todos(query.from_user.id)
    
    if not todos:
        await query.edit_message_text("No tasks to mark!")
        await show_todos_menu(query, new_message=True)
        return
    
    pending = [i for i, t in enumerate(todos, 1) if not t['done']]
    
    if not pending:
        await query.edit_message_text("All tasks are already completed! 🎉")
        await show_todos_menu(query, new_message=True)
        return
    
    keyboard = []
    row = []
    for i in pending:
        row.append(InlineKeyboardButton(f"{i}", callback_data=f"mark_todo_{i}"))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_todos")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "✅ *Mark Task as Done*\n\nSelect the task number to mark as done:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def clear_notes_confirm(query):
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes, Clear All", callback_data="confirm_clear_notes"),
            InlineKeyboardButton("❌ No, Cancel", callback_data="cancel_clear_notes")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="back_notes")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "⚠️ *Clear All Notes*\n\nAre you sure you want to delete ALL notes?\nThis action cannot be undone!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def clear_todos_confirm(query):
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes, Clear All", callback_data="confirm_clear_todos"),
            InlineKeyboardButton("❌ No, Cancel", callback_data="cancel_clear_todos")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="back_todos")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "⚠️ *Clear All Tasks*\n\nAre you sure you want to delete ALL tasks?\nThis action cannot be undone!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text
    
    if user_id in user_states:
        action = user_states[user_id].get("action")
        
        if action == "add_note":
            add_note(update.effective_user.id, text)
            
            keyboard = [[InlineKeyboardButton("📋 View Notes", callback_data="notes_view")],
                       [InlineKeyboardButton("🔙 Back to Notes", callback_data="back_notes")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "✅ *Note Added Successfully!*\n\nYour note has been saved.",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            del user_states[user_id]
            
        elif action == "add_todo":
            add_todo(update.effective_user.id, text)
            
            keyboard = [[InlineKeyboardButton("📋 View Tasks", callback_data="todos_view")],
                       [InlineKeyboardButton("🔙 Back to Todos", callback_data="back_todos")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "✅ *Task Added Successfully!*\n\nYour task has been saved.",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            del user_states[user_id]
    else:
        await show_main_menu_direct(update)

async def show_main_menu_direct(update: Update):
    keyboard = [
        [InlineKeyboardButton("📝 Notes", callback_data="menu_notes")],
        [InlineKeyboardButton("✅ Todos", callback_data="menu_todos")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="menu_help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "✨ *Main Menu* ✨\n\nSelect an option:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔙 Back to Main", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    help_text = """
*📚 Help Guide*

*Commands:*
/start - Show main menu
/help - Show this help message

*Navigation:*
Use the inline buttons to navigate through the menu. No need to type commands!

*Quick Actions:*
1. Tap buttons to perform actions
2. Type text when prompted
3. Select from numbered lists
4. Confirm important actions

Need more help? Just explore the menus!
"""
    
    await update.message.reply_text(
        help_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    
    app.add_handler(CallbackQueryHandler(button_callback))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.add_handler(CommandHandler("note", note_cmd))
    app.add_handler(CommandHandler("notes", notes_cmd))
    app.add_handler(CommandHandler("todo", todo_cmd))
    app.add_handler(CommandHandler("todos", todos_cmd))
    app.add_handler(CommandHandler("done", done_cmd))
    app.add_handler(CommandHandler("deleteNote", dlnt_cmd))
    app.add_handler(CommandHandler("deleteTask", dltsk_cmd))
    app.add_handler(CommandHandler("clearNotes", clrnt_cmd))
    app.add_handler(CommandHandler("clearTodo", clrtsk_cmd))
    
    print("Bot is starting...")
    print(f"[{get_current_time()}] Keep-alive system activated")
    app.run_polling()

async def note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu_direct(update)

async def notes_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu_direct(update)

async def todo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu_direct(update)

async def todos_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu_direct(update)

async def done_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu_direct(update)

async def dlnt_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu_direct(update)

async def dltsk_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu_direct(update)

async def clrnt_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu_direct(update)

async def clrtsk_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu_direct(update)

if __name__ == "__main__":
    keep_alive_thread = threading.Thread(target=keep_alive_background, daemon=True)
    keep_alive_thread.start()
    main()
