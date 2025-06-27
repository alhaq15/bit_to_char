n = 0
all = 0
with open("kbbi-bersih.txt", 'r', encoding='utf-8') as file:
    for word in file:
        all += 1
        if len(word)>10:
            n += 1

print(f"{n}-of-{all}-{n/all}")