import asyncio
import sys

sys.path.append("/app/backend")
from open_webui.models.models import Models, ModelForm, ModelMeta, ModelParams

async def fix_models():
    # ID Knowledge Base yang telah kita buat sebelumnya
    kb_id = "fd3adbfa-f954-43f9-be8a-e63101b32992"
    kb_name = "SIM-KKN Core Documentation"
    
    # Base model yang valid (Ollama)
    base_model_id = "deepseek-v3.1:671b-cloud"
    
    ids = ["antigravity-architect", "simkkn-backend-wizard", "uiux-aesthetic-specialist"]
    
    for mid in ids:
        model = await Models.get_model_by_id(mid)
        if model:
            print(f"Fixing metadata for {mid}...")
            
            # Format Knowledge yang benar adalah list of dicts
            knowledge_data = [
                {
                    "id": kb_id,
                    "name": kb_name,
                    "type": "collection"
                }
            ] if mid != "uiux-aesthetic-specialist" else []
            
            # Format Skills: Open WebUI menggunakan 'skillIds' di meta
            skill_ids = []
            if mid == "antigravity-architect":
                skill_ids = ["sim-kkn-architecture", "antigravity-strict-mode"]
            elif mid == "uiux-aesthetic-specialist":
                skill_ids = ["antigravity-strict-mode"]

            # Update meta dengan extra fields yang benar
            meta_dict = model.meta.model_dump()
            meta_dict["knowledge"] = knowledge_data
            meta_dict["skillIds"] = skill_ids
            
            # Bersihkan kunci lama jika ada
            meta_dict.pop("skills", None) 
            
            form = ModelForm(
                id=model.id,
                base_model_id=base_model_id,
                name=model.name,
                params=model.params,
                meta=ModelMeta(**meta_dict),
                is_active=model.is_active
            )
            await Models.update_model_by_id(mid, form)
            print(f"Model {mid} updated successfully.")

if __name__ == "__main__":
    asyncio.run(fix_models())
