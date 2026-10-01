import re
import os

for path in ['app/src/main/assets/index.html', 'nukrop_emulator.html']:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = re.sub(
        r"models:\s*\[\s*'qwen/qwen3\.6-27b',\s*'groq/compound-mini',\s*'openai/gpt-oss-20b'\s*\]",
        "models: ['openai/gpt-oss-20b']",
        content
    )
    
    # Let's also check if there's any other GROQ_API_KEYS logic that needs updating
    # (In sendAiChatMessage, it might use callGroqAI which had compound-mini)
    content = re.sub(
        r"model:\s*'groq/compound-mini'",
        "model: 'openai/gpt-oss-20b'",
        content
    )
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("AI models updated successfully")
