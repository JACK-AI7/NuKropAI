import os

for filepath in [r"app\src\main\assets\index.html", r"nukrop_emulator.html"]:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # PowerShell replacement messed up, let's fix it manually.
        # It might be `    `,\\n\\n  /* -- DRIVER: LOGIN -- */` now.
        content = content.replace("    `,\\n\\n  /* -- DRIVER: LOGIN -- */\n  driver_login:", "    `,\n\n  /* -- DRIVER: LOGIN -- */\n  driver_login:")
        
        # Also fix the original semicolon if it's still there
        content = content.replace("    `;\n\n  /* -- DRIVER: LOGIN -- */\n  driver_login:", "    `,\n\n  /* -- DRIVER: LOGIN -- */\n  driver_login:")
        content = content.replace("    `;\r\n\r\n  /* -- DRIVER: LOGIN -- */\r\n  driver_login:", "    `,\n\n  /* -- DRIVER: LOGIN -- */\n  driver_login:")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
