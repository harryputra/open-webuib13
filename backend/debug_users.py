import asyncio
import sys

sys.path.append("/app/backend")
from open_webui.models.users import Users
from open_webui.models.prompts import Prompts
from open_webui.models.skills import Skills

async def run():
    users = await Users.get_users()
    print(f"Total users found: {len(users)}")
    
    admin_id = None
    for u in users:
        print(f"User: {u.id}, Email: {u.email}, Role: {u.role}")
        if u.role == "admin":
            admin_id = u.id
            break
            
    if not admin_id and users:
        print("No admin found. Falling back to the first user.")
        admin_id = users[0].id
        
    if not admin_id:
        print("No users in database at all!")
        return
        
    print(f"Selected user ID: {admin_id}")
    
    # Update the prompts and skills we created earlier to belong to this user
    # Or just re-insert them with the right user ID
    prompts = await Prompts.get_prompts()
    for p in prompts:
        if p.user_id == "00000000-0000-0000-0000-000000000000":
            print(f"Deleting orphaned prompt {p.command}")
            await Prompts.delete_prompt_by_command(p.command)
            
    skills = await Skills.get_skills()
    for s in skills:
        if s.user_id == "00000000-0000-0000-0000-000000000000":
            print(f"Deleting orphaned skill {s.name}")
            await Skills.delete_skill_by_id(s.id)

if __name__ == "__main__":
    asyncio.run(run())
