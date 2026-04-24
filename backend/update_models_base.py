import asyncio
import sys

sys.path.append("/app/backend")
from open_webui.models.models import Models, ModelForm, ModelMeta, ModelParams

async def update_models():
    # We will point the custom models to 'deepseek-v3.1:671b-cloud' which exists in Ollama
    base_model_id = "deepseek-v3.1:671b-cloud"
    
    ids = ["antigravity-architect", "simkkn-backend-wizard", "uiux-aesthetic-specialist"]
    
    for mid in ids:
        model = await Models.get_model_by_id(mid)
        if model:
            print(f"Updating base_model_id for {mid} to {base_model_id}...")
            form = ModelForm(
                id=model.id,
                base_model_id=base_model_id,
                name=model.name,
                params=model.params,
                meta=model.meta,
                is_active=model.is_active
            )
            await Models.update_model_by_id(mid, form)

if __name__ == "__main__":
    asyncio.run(update_models())
