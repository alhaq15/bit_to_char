import random
import string

kata_uji = ['you', 'fired']
pref = ["I like the melody of this song", "The lyrics of this song touched my feelings"
        "This song has good vocal quality","I'm very interested in listening to this song again",
        "This song is just my kind of music"]
indeks = list(string.ascii_lowercase)
indeks.append(' ')
f = open("song-list.txt", 'r', encoding='utf-8')
songs = f.readlines()
for kata in kata_uji:
    if len(kata)>len(songs):
        print("the message can not be embedded")
    else:
        f = open("respondent-list.txt", 'r', encoding='utf-8')
        respondents = f.readlines()
        responden = random.choice(respondents)
        i = 0
        for song in songs:
            if i < len(kata):
                kar = kata[i]
                idx = indeks.index(kar) + 1
                fbiner = format(idx, '05b')
                arr = song.split('-')
                templ = "The followings is the preference of song titled: " + arr[0] + " by " + arr[1]
                prefs = []
                if fbiner[0] == "1":
                    prefs.append(pref[0])
                elif fbiner[1] == "1":
                    prefs.append(pref[1])
                elif fbiner[2] == "1":
                    prefs.append(pref[2])
                elif fbiner[3] == "1":
                    prefs.append(pref[3])
                elif fbiner[4] == "1":
                    prefs.append(pref[4])
            
                templ += '. '.join(prefs)

                print(templ)
            i +=1