import asyncio
import sys

sys.path.append("/app/backend")
from open_webui.models.models import Models
from open_webui.models.users import Users

async def verify():
    models = await Models.get_all_models()
    print("Models in database:")
    for m in models:
        print(f"ID: {m.id}, Name: {m.name}, UserID: {m.user_id}, Active: {m.is_active}")

    users = await Users.get_users()
    users_list = users.get("users", [])
    print("\nUsers in database:")
    for u in users_list:
         print(f"ID: {u.id}, Email: {u.email}, Role: {u.role}")

if __name__ == "__main__":
    asyncio.run(verify())
