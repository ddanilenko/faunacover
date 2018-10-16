from app.models.userprofile import UserProfile
from app.models.song import Song
from app.models.group import Group


def initial_fill(application):

    user1 = UserProfile(name="Darya", email="ddanilenko@ukr.net", password_hash="qwerty")
    user1.hash_password("qwerty")

    user2 = UserProfile(name="user2", email="user2@example.com", password_hash="cat")
    user2.hash_password("cat")

    application.session.add_all([user1, user2])


    group1 = Group(name="latexfauna",
                   description="""Once upon a time, Kievskie Hipstery zatsenili our
                    music and Latexfauna became a popular band, despite of its 
                    zaunylaya and odnotipnaya musica. Ha-ha-ha we thought.
                    Nihuya sebe we thought.""",
                   official_site="https://www.facebook.com/latexfauna")

    group2 = Group(name="IAMX",
                   description="""IAMX is the solo musical project of Chris Corner,
                    formerly of the band Sneaker Pimps. Founded in 2004 in London,
                     it is an independent music project which also focuses on and 
                     experiments with visual art.[1] Musically, IAMX spans multiple
                      genres from electronic rock and dance music to 
                      burlesque-influenced songs and emotional ballads. Corner's 
                      striking and wide-ranging voice, and his way of programming 
                      sounds and beats, make up the obvious characteristic of the 
                      IAMX sound.""",
                   official_site="http://iamxmusic.com/")

    application.session.add_all([group1, group2])

    song1 = Song(title="LIME",
                 text="""Мене в тобі всьо устраює\nОсобливо липень\nОсобливо липень\nБасейн клоне на сон\nЯ багато випив\nЯ багато випив\nІ лайм\nІ лаймові небеса\nІ лайм\nІ лаймові небеса\nМене всьо устраює\nШо ти людина\nНайнебезпечніший в світі звір\nНаші теплі новини\nНалежать лише мені\nЛа-ла-ла\nЛа-ла-ла\nІ ми крісіві\nУ світлі лаймових небес\nІ нас розум\nЯдерний процес\nМене в тобі всьо устраює\nОсобливо липень\nОсобливо липень\nБасейн клоне на сон\nЯ багато випив\nЯ багато випив\nІ лайм\nІ лаймові небеса\nІ лайм\nІ лаймові небеса\nМене всьо устраює\nШо я людина\nНайбезпорадніший в світі звір\nЯ безсмертна дитина\nІ я багато чого хотів\nІ мав, мав, мав\nЛав, лав, лав\nОдна й та сама штука\nПозаду твоїх і моїх очей\nДивиться на вічність\nТрогатєльних речей\nМене в тобі всьо устраює\nОсобливо липень\nОсобливо липень\nБасейн клоне на сон\nЯ багато випив\nЯ багато випив\nІ лайм\nІ лаймові небеса\nІ лайм\nІ лаймові небеса\nМене всьо устраює\nОсобливо липень\nОсобливо липень""",
                 year="2017",
                 youtube_link="https://www.youtube.com/watch?v=-UqKwEEkX2s",
                 group_id=1)

    song2 = Song(title="Exit",
                 text="""Hold me like you mean it\nTonight I need to feel your skin on my skin\nOften I forget you’re this being\nI get lost alone online, stalking humanity\nThe world is collapsing\nThe world is indifferent\nCan you feel it\nThe communication\nInside this room?\nWe are infinite\nSo let the hurricane come blow me down\nDown to the mountain where I will scream to be found\nThe sky has opened up and now I’m overcome\nWith all the information, the universe, the atom""",
                 year="2018",
                 youtube_link="https://www.youtube.com/watch?v=m35fDh_3Ay4",
                 group_id=1)

    application.session.add_all([song1, song2])
    application.session.commit()


# "You know I love it when you're down on your knees\nAnd I'm a junkie for the way that you please\nYou shut me up when you swallow me down\nMy back to the wall you're going to town\nI almost told you that I loved you\nThank God I didn't 'cause it would have been a lie\nI say the damnedest things when you're on top of me\nI almost told you that I loved you\nI hate to say it but it has to be said\nYou look so fragile as I fuck with your head\nI know it shouldn't but it's getting me on\nIf sex is the drug then what is the cost?\nI almost told you that I loved you\nThank God I didn't 'cause it would have been a lie\nI say the damnedest things when you're on top of me\nI almost told you that I loved you\nI'm not the one that you want\nNot the one that you need\nMy love…"
#
# "I tear my heart open\nI sew myself shut\nMy weakness is\nThat I care too much\nMy scars remind us\nThat the past is real\nI tear my heart open\nJust to feel\nDrunk and I'm feeling down\nAnd I just want to be alone\nI'm pissed cause you came around\nWhy don't you just go home\n'Cause you channel all your pain\nAnd I can't help you go fix yourself\nYour making me insane\nAll I can say is\nI tear my heart open\nI sew myself shut\nMy weakness is\nThat I care too much\nOur scars remind us\nThat the past is real\nI tear my heart\nOpen just to feel\nI tried to help you once\nAgainst my own advice\nI saw you going down\nBut you never realized\nThat your drowning in the water\nSo I offered you my hand\nCompassion's in my nature\nTonight is our last stand\nI tear my heart open\nI sew myself shut\nMy weakness is\nThat I…"
#
# "Salute the sun, I've been sitting here all night long\nHauling rock over Buddha with the Longhorn\nGot a hole, rip a pocket off my uniform\nWith the Blackwatch Boys get your heads down\nDuty calls but it is way too late I'm too far gone\nWaiting for Godot, hell with my pants down\nCracked the stash sent me crying in the midday sun\nI miss my dog and I miss my freedom\nI don't know why they are calling on the radio\nThey know I'm here just out of sight\nI don't know why they're calling on the radio\nHe's by my side and I know I'm right\nI don't know why they are calling on the radio\nThey know I'm here just out of sight\nI don't know why they're calling on the radio\nHe's by my side and I know I'm right\nI hate the things I think about you when I'm all alone\nI know you're tough but I've been gone for so long\nI play the memories of you inside my head\nSo all those pictures of us burn and radiate\nWatch the clouds and I'm falling, falling through the cracks\nHead beats and the heart is pounding fast\nOff the ground into the starry dark\nInto your arms I'm falling\nI'm falling, I'm falling\nI don't know why they are calling on the radio\nThey know I'm here just out of sight\nI don't know why they're calling on the radio\nHe's by my side and I know I'm right\nI don't know why they are calling on the radio\nThey know I'm here just out of sight\nI don't know why they're calling on the radio\nHe's by my side and I know I'm right\nMy brain, my body's fried\nI've got to stay alive\nI've got to take a chance and keep on moving\nKeep on moving\nI don't know why they are calling on the radio\nThey know I'm here just out of sight\nDon't know why they're calling on the radio\nHe's by my side and I know I'm right\nDon't know why they are calling on the radio\nIt's on my side and I know I'm right\nI don't know why they are calling on the radio\nIt's on my side and I know I'm alright\nI see your light from miles away\nI see your light from miles away"
#
# "I'm only happy when it rains\nI'm only happy when it's complicated\nAnd though I know you can't appreciate it\nI'm only happy when it rains\nYou know I love it when the news is bad\nWhy it feels so good to feel so sad?\nI'm only happy when it rains\nPour your misery down\nPour your misery down on me\nPour your misery down\nPour your misery down on me\nI'm only happy when it rains\nI feel good when things are goin' wrong\nI only listen to the sad, sad songs\nI'm only happy when it rains\nI only smile in the dark\nMy only comfort is the night gone black\nI didn't accidentally tell you that\nI'm only happy when it rains\nYou'll get the message by the time I'm through\nWhen I complain about me and you\nI'm only happy when it rains\nPour your misery down (Pour your misery down)\nPour your misery down on me\nPour your misery down (Pour your misery down)\nPour your misery down on me\nPour your misery down (Pour your misery down)\nPour your misery down on me\nPour your misery down\nYou can keep me company\nAs long as you don't care\nI'm only happy when it rains\nYou wanna hear about my new obsession?\nI'm riding high upon a deep depression\nI'm only happy when it rains\nPour some misery down on me\nI'm only happy when it rains\nPour some misery down on me\nI'm only happy when it rains\nPour some misery down on me\nI'm only happy when it rains\nPour some misery down on me\nI'm only happy when it rains\nPour some misery down on me\nPour some misery down on me\nPour some misery down on me\nPour some misery down on me\nPour some misery down on me\nPour some misery down on me"
#
# "Ми наробили кіборгів\nУ красівому бункері\nІ пишемо про них книжки\nБо ми дослідники\nА ти дослідниця\nПротирай очки\nА я зломав олівця\nТак собі факт\nНо ти мені нравишся\nТи мені нравишся\nТи мені нравишся\nТи мені нравишся\nТи закидаєш волоси\nТи откриваєшся\nА я усе січу\nСвою напарніцу\nТи така умніца\nУ тебе всьо схвачено\nА я нахуячений\nТак собі факт\nНо ти мені нравишся\nТи мені нравишся\nТи мені нравишся\nТи мені нравишся\nМи наробили кіборгів\nУ красівому бункері\nІ пишемо про них книжки\nБо ми дослідники\nМи наробили кіборгів\nУ красівому бункері\nІ пишемо про них книжки\nБо ми дослідники\nА ти дослідниця"