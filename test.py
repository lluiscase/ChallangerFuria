import random
import json



def predefine(n):
    with open('intents.json','r',encoding='utf-8') as messagePredefine:
        parsed = json.load(messagePredefine)
        answer = parsed['intents'][n]['response']
    return random.choice(answer)

result = predefine(0)
print(result)