import os
import shutil

files = ['app/src/main/assets/index.html', 'nukrop_emulator.html']
supabase_scripts = """
  <!-- Supabase Architecture -->
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  <script src="js/supabase_integration.js"></script>
"""

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    if 'supabase-js' not in text:
        text = text.replace('</head>', supabase_scripts + '</head>')
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

if not os.path.exists('js'):
    os.makedirs('js')
shutil.copy('app/src/main/assets/js/supabase_integration.js', 'js/supabase_integration.js')

print('Supabase integrated into HTML')
