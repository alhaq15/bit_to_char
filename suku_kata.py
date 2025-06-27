import re

def pecah_suku_kata(kata):
    # Vokal bahasa Indonesia
    vokal = 'aiueoAIUEO'
    hasil = []
    temp = ''
    i = 0
    while i < len(kata):
        temp += kata[i]
        if kata[i] in vokal:
            # Cek apakah huruf berikutnya konsonan+vokal (CV)
            if i+2 < len(kata) and kata[i+1] not in vokal and kata[i+2] in vokal:
                hasil.append(temp)
                temp = ''
            # Cek apakah akhir kata
            elif i+1 == len(kata):
                hasil.append(temp)
                temp = ''
            # Cek apakah vokal diikuti konsonan terakhir
            elif i+1 < len(kata) and kata[i+1] not in vokal and i+2 == len(kata):
                temp += kata[i+1]
                hasil.append(temp)
                break
            else:
                hasil.append(temp)
                temp = ''
        i += 1
    if temp:
        hasil.append(temp)
    return hasil

# Contoh penggunaan
contoh_kata = [
    "bahasa", "indonesia", "rumah", "makanan", "mengerti", "komputer", "anak", "bermain"
]

for kata in contoh_kata:
    print(f"{kata} ➜ {pecah_suku_kata(kata)}")
