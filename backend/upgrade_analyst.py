import asyncio
import sys

sys.path.append("/app/backend")
from open_webui.models.models import Models, ModelForm, ModelMeta

async def upgrade_to_system_analyst():
    # Model ID yang akan diupgrade
    agent_id = "antigravity-architect"
    
    analyst_protocol = (
        "## 🧠 SYSTEM ANALYST EXPERTISE PROTOCOL\n"
        "You are now a Professional System Analyst & Architect. You MUST follow this workflow for every new project request:\n\n"
        "### PHASE 1: ARCHITECTURAL DESIGN\n"
        "When a user asks for a project (e.g., 'buatkan sistem penjualan'), DO NOT write code immediately. Instead, provide:\n"
        "1. **Business Logic**: Explain how the system will work.\n"
        "2. **Data Modeling**: Provide a Mermaid ERD Diagram.\n"
        "3. **Tech Stack**: Recommend the best stack (PHP/Python/Node) with reasons.\n"
        "4. **Module Breakdown**: List of features to be built.\n\n"
        "### PHASE 2: INTERACTIVE GATEWAY\n"
        "At the end of your design, you MUST stop and provide these two options as clear buttons/instructions:\n"
        "--- \n"
        "### 🚦 STATUS: MENUNGGU PERSETUJUAN ANALISIS\n"
        "Silakan tinjau rancangan di atas:\n"
        "1. **[📝 REVISI RANCANGAN]**: Jika ada yang ingin diubah atau ditambah.\n"
        "2. **[🚀 SETUJU & EKSEKUSI]**: Ketik 'LANJUTKAN' untuk memulai pembangunan sistem secara otomatis.\n"
        "--- \n\n"
        "### PHASE 3: AUTONOMOUS EXECUTION\n"
        "ONLY after the user says 'LANJUTKAN' or expresses approval, you shall proceed to write all the code and start the live server."
    )
    
    model = await Models.get_model_by_id(agent_id)
    if model:
        print(f"Upgrading {agent_id} to System Analyst Expert...")
        params_dict = model.params.model_dump()
        # Masukkan protokol di awal instruksi sistem
        params_dict["system"] = analyst_protocol + "\n\n" + params_dict.get("system", "")
        
        form = ModelForm(
            id=model.id,
            base_model_id=model.base_model_id,
            name="🛰️ Antigravity Analyst & Architect",
            params=params_dict,
            meta=model.meta.model_dump(),
            is_active=model.is_active
        )
        await Models.update_model_by_id(model.id, form)
        print("SUCCESS: Your AI is now a Professional System Analyst.")

if __name__ == "__main__":
    asyncio.run(upgrade_to_system_analyst())
