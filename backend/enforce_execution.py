import asyncio
import sys

sys.path.append("/app/backend")
from open_webui.models.models import Models, ModelForm, ModelMeta

async def enforce_execution():
    ids = ["antigravity-architect"]
    
    for mid in ids:
        model = await Models.get_model_by_id(mid)
        if model:
            print(f"Enforcing execution for {mid}...")
            
            meta_dict = model.meta.model_dump()
            
            # Aktifkan fitur Code Interpreter secara paksa
            if "capabilities" not in meta_dict:
                meta_dict["capabilities"] = {}
            
            # Pastikan capabilities ini aktif
            meta_dict["capabilities"]["code_interpreter"] = True
            meta_dict["capabilities"]["builtin_tools"] = True
            
            # Tambahkan fitur ini ke dalam meta.features jika ada
            if "features" not in meta_dict:
                meta_dict["features"] = {}
            meta_dict["features"]["code_interpreter"] = True
            
            # Gunakan mode 'native' untuk function calling
            if "params" not in meta_dict:
                meta_dict["params"] = {}
            meta_dict["params"]["function_calling"] = "native"

            form = ModelForm(
                id=model.id,
                base_model_id=model.base_model_id,
                name=model.name,
                params=model.params.model_dump(),
                meta=ModelMeta(**meta_dict),
                is_active=model.is_active
            )
            await Models.update_model_by_id(mid, form)
            print(f"Persona {mid} now has ENFORCED execution capabilities.")

if __name__ == "__main__":
    asyncio.run(enforce_execution())
