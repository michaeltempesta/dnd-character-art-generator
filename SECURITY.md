# Public Gradio Hardening (what’s already included)
- **Auth**: `auth=("user", "strong-password")` and queue limits (`concurrency_count=1, max_size=8`).
- **Input clamps**: resolution ≤ 1280×1536, steps ≤ 40, CFG ∈ [3,10], non-empty prompts.
- **Guardrails**: basic keyword denylist; negative prompt prefilled and validated.
- **Secrets**: `.env` via `python-dotenv` (HF_TOKEN), never hardcoded.
- **Logging**: no prompt logging by default.
- **Model pinning**: explicit IDs for SDXL + ControlNets.
