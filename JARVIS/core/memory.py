import json
from config import MEMORY_FILE, DATA_DIR
MAX_MESSAGES = 50
def _load():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not MEMORY_FILE.exists(): return []
    try: return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except Exception: return []
def _save(items):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    MEMORY_FILE.write_text(json.dumps(items[-MAX_MESSAGES:], ensure_ascii=False, indent=2), encoding="utf-8")
def add(role, content):
    items=_load(); items.append({"role":role,"content":str(content)}); _save(items)
def recent(limit=12): return _load()[-limit:]
def context(limit=12):
    return "\n".join(f"{m['role'].upper()}: {m['content']}" for m in recent(limit))
def clear(): _save([])
