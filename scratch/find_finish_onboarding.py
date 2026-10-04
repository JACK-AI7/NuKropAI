import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('finishPlantixOnboarding')
if pos == -1:
    pos = text.find('completeOnboarding')
if pos == -1:
    pos = text.find('closePlantixFlow')
if pos == -1:
    pos = text.find('onboarding_completed')

print("Pos:", pos)
if pos != -1:
    print(text[pos-100:pos+500])
