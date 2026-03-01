from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def save_message(role, content):
    """Save a message to Supabase"""
    try:
        supabase.table("conversations").insert({
            "role": role,
            "content": content
        }).execute()
    except Exception as e:
        print(f"Memory error saving: {str(e)}")

def load_history(limit=20):
    """Load last N messages from Supabase"""
    try:
        response = supabase.table("conversations")\
            .select("role, content")\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        return list(reversed(response.data))
    except Exception as e:
        print(f"Memory error loading: {str(e)}")
        return []

def clear_memory():
    """Clear all conversation history"""
    try:
        supabase.table("conversations").delete().neq("id", 0).execute()
        return "🗑️ Memory cleared!"
    except Exception as e:
        return f"❌ Error clearing memory: {str(e)}"