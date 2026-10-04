import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('function triggerDriverCall(')
pos2 = text.find('function openDriverLiveChatModal(')
pos3 = text.find('function sendLiveHaulChatMessage(')
pos4 = text.find('function shareLiveHaulTrip(')

print("triggerDriverCall at:", pos1)
print("openDriverLiveChatModal at:", pos2)
print("sendLiveHaulChatMessage at:", pos3)
print("shareLiveHaulTrip at:", pos4)

print("\n--- triggerDriverCall code ---")
print(text[pos1:pos2])

print("\n--- openDriverLiveChatModal code ---")
print(text[pos2:pos3+400])
