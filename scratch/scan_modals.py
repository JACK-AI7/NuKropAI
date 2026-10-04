import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('function showHaulCompletedInvoiceModal(')
pos1_end = text.find('\nfunction ', pos1 + 50)

pos2 = text.find('function openDriverHaulHistoryModal(')
pos2_end = text.find('\nfunction ', pos2 + 50)

def print_emojis(name, s):
    emojis = re.findall(r'[\U00010000-\U0010ffff\u2600-\u27bf\u2300-\u23ff\u2b50]', s)
    print(f"\n{name} emojis: {set(emojis)}")
    for em in set(emojis):
        for m in re.finditer(re.escape(em), s):
            snip = s[max(0, m.start()-30):min(len(s), m.end()+30)].replace('\n', ' ')
            print(f"  {em}: {snip.strip()}")

print_emojis("showHaulCompletedInvoiceModal", text[pos1:pos1_end])
print_emojis("openDriverHaulHistoryModal", text[pos2:pos2_end])
