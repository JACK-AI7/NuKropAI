import os

files = ['app/src/main/assets/index.html', 'nukrop_emulator.html']
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find the try block in handleFormAuthSubmit
    try_block_old = """    if (isSignUp) {
      result = await supabaseSignUp(email, password, name);
    } else {
      result = await supabaseSignIn(email, password);
    }

    let userId = 'usr_' + Date.now();
    let token = 'sb_token_' + Date.now();

    if (result.ok && result.data) {
      if (result.data.user) userId = result.data.user.id;
      if (result.data.access_token) token = result.data.access_token;
      currentSupabaseSession = result.data;
    } else if (result.data && result.data.msg) {
      console.log('Supabase Auth Notice:', result.data.msg);
    }"""
    
    try_block_new = """    // Delegating to official Supabase JS SDK (js/supabase_integration.js)
    if (typeof nk_loginUser === 'undefined') {
        alert("System error: architecture script missing.");
        return;
    }
    let result = await nk_loginUser(email, password);
    
    let userId = 'usr_' + Date.now();
    let token = 'sb_token_' + Date.now();
    
    if (result.data && result.data.user) {
        userId = result.data.user.id;
        token = result.data.session?.access_token || token;
    } else if (result.error) {
        console.warn("Supabase auth error:", result.error.message);
        // Fallback to local offline mode if login fails (for prototyping)
    }"""

    text = text.replace(try_block_old, try_block_new)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

import shutil
shutil.copy('app/src/main/assets/js/supabase_integration.js', 'js/supabase_integration.js')
print("Login updated to use real architecture.")
