import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('function showHaulCompletedInvoiceModal(')
pos2 = text.find('function openDriverHaulHistoryModal(')

print("showHaulCompletedInvoiceModal at:", pos1)
print("openDriverHaulHistoryModal at:", pos2)

if pos1 != -1:
    print("\n--- showHaulCompletedInvoiceModal ---")
    print(text[pos1:pos1+1000])

if pos2 != -1:
    print("\n--- openDriverHaulHistoryModal ---")
    print(text[pos2:pos2+1000])
