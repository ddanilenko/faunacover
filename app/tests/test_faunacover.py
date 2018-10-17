import json
import unittest

from app import create_app, Base
from app.config import TestConfig
from rest_api.api import create_api
from scripts.initial_script import initial_fill


class GroupResourceCase(unittest.TestCase):
    def setUp(self):
        self.application = create_app(config_class=TestConfig)
        Base.metadata.create_all(bind=self.application.engine)
        initial_fill(self.application)
        create_api(self.application)
        self.app = self.application.test_client()

    def tearDown(self):
        Base.metadata.drop_all(bind=self.application.engine)

    def test_get_by_id_positive(self):
        resp = self.app.get('/group/2')
        self.assertEqual(resp.json['name'], 'IAMX')
        self.assertIsNone(resp.json.get('songs'))
        self.assertTrue(resp._status_code, 200)

    def test_get_by_id_negative(self):
        resp = self.app.get('/group/latexfauna')
        self.assertTrue(resp._status_code, 404)
        resp1 = self.app.get('/group/16565')
        self.assertTrue(resp1._status_code, 404)


    def test_get_extended_by_id_positive(self):
        resp = self.app.get('/group/1?extended=1')
        self.assertIsNotNone(resp.json.get('songs'))
        self.assertTrue(resp._status_code, 200)

    def test_get_extended_by_id_negative(self):
        resp = self.app.get('/group/1?extended=True')
        self.assertTrue(resp._status_code, 400)
        resp1 = self.app.get('/group/latexfauna?extended=True')
        self.assertTrue(resp1._status_code, 404)

    def test_get_list_of_groups_positive(self):
        resp = self.app.get('/group')
        self.assertEqual(len(resp.json), 2)
        resp1 = self.app.get('/group?page=1&per_page=1')
        self.assertEqual(len(resp1.json), 1)
        self.assertEqual(resp1.json[0]['name'], 'latexfauna')
        resp2 = self.app.get('/group?page=2&per_page=1')
        self.assertEqual(len(resp2.json), 1)
        self.assertEqual(resp2.json[0]['name'], 'IAMX')

    def test_get_list_of_groups_negative(self):
        resp = self.app.get('/group?page=one')
        self.assertEqual(resp._status_code, 400)
        resp1 = self.app.get('/group?page=1&per_page=one')
        self.assertEqual(resp1._status_code, 400)

    def test_post_list_of_groups_positive(self):
        data = [{
            'name': "Papa Roach",
            'description': """американская рок-группа из города Вакавилль, штат Калифорния, образованная в 1993 году.
                 Обрела мировую известность благодаря своему дебютному мэйджор-альбому Infest (2000).
                 К настоящему моменту группа выпустила 8 мини-альбомов, 1 концертный альбом и 9 студийных альбомов""",
            'official_site': "http://www.paparoach.com/"}, {
            'name': "Garbage",
            'description': "британско-американская рок-группа, сформированная в городе Мэдисон в 1994 году[4]. "
                           "В состав группы входят шотландская певица Ширли Мэнсон (вокал, гитара, клавишные) и "
                           "американские музыканты Стив Маркер (гитара, клавишные), Дюк Эриксон (бас-гитара, клавишные,"
                           " гитара, перкуссия) и Бутч Виг (ударные, перкуссия).Коллектив стал известен своим необычным"
                           " звучанием, выразительным вокалом солистки, а также инновационными средствами обработки "
                           "звука.",
            'official_site': "http://www.paparoach.com/"
        }]
        resp = self.app.post('/group', data=json.dumps(data), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp._status_code, 201)
        data1 = {
            "name": "Garbage",
            "description": "британско-американская рок-группа, сформированная в городе Мэдисон в 1994 году[4]. В состав"
                           " группы входят шотландская певица Ширли Мэнсон (вокал, гитара, клавишные) и американские "
                           "музыканты Стив Маркер (гитара, клавишные), Дюк Эриксон (бас-гитара, клавишные, гитара, "
                           "перкуссия) и Бутч Виг (ударные, перкуссия). Коллектив стал известен своим необычным "
                           "звучанием, выразительным вокалом солистки, а также инновационными средствами обработки "
                           "звука.",
            "official_site": "https://www.garbage.com/"
        }
        resp1 = self.app.post('/group', data=json.dumps(data1), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp1._status_code, 201)
        resp2 = self.app.get('/group')
        self.assertEqual(len(resp2.json), 4)

    def test_post_list_of_groups_negative(self):
        data = {
            "description": "британско-американская рок-группа, сформированная в городе Мэдисон в 1994 году[4]. В состав"
                           " группы входят шотландская певица Ширли Мэнсон (вокал, гитара, клавишные) и американские "
                           "музыканты Стив Маркер (гитара, клавишные), Дюк Эриксон (бас-гитара, клавишные, гитара, "
                           "перкуссия) и Бутч Виг (ударные, перкуссия). Коллектив стал известен своим необычным "
                           "звучанием, выразительным вокалом солистки, а также инновационными средствами обработки "
                           "звука.",
            "official_site": "https://www.garbage.com/"
        }
        resp = self.app.post('/group', data=json.dumps(data), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp._status_code, 400)
        self.assertIn("Required args are missing", resp.json['message'])
        data1 = []
        resp1 = self.app.post('/group', data=json.dumps(data1), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp._status_code, 400)
        self.assertIn("your request is inappropriate!", resp1.json['message'])
        data1 = 'kjdfnbpdfd[gmd['
        resp1 = self.app.post('/group', data=json.dumps(data1), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp._status_code, 400)
        self.assertIn("your request is inappropriate!", resp1.json['message'])

    def test_put_group_by_id_positive(self):
        data = {
            "name": "Garbage",
            "description": "британско-американская рок-группа, сформированная в городе Мэдисон в 1994 году[4]. В состав"
                           " группы входят шотландская певица Ширли Мэнсон (вокал, гитара, клавишные) и американские "
                           "музыканты Стив Маркер (гитара, клавишные), Дюк Эриксон (бас-гитара, клавишные, гитара, "
                           "перкуссия) и Бутч Виг (ударные, перкуссия). Коллектив стал известен своим необычным "
                           "звучанием, выразительным вокалом солистки, а также инновационными средствами обработки "
                           "звука.",
            "official_site": "https://www.garbage.com/"
        }
        resp = self.app.put('/group/1', data=json.dumps(data), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp._status_code, 200)
        data1 = {
            "name": "latexfauna",
            "official_site": "https://www.garbage.com/"
        }
        resp1 = self.app.put('/group/1', data=json.dumps(data1), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp1._status_code, 200)

    def test_put_group_by_id_negative(self):
        data = {
            "name": "IAMX",
            "description": "",
            "official_site": "https://www.garbage.com/"
        }
        resp = self.app.put('/group/1', data=json.dumps(data), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp._status_code, 400)
        resp1 = self.app.put('/group/1999', data=json.dumps(data), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp1._status_code, 404)
        self.assertIn("There is no group with such id", resp1.json['message'])

    def test_delete_group_by_id_positive(self):
        resp = self.app.delete('/group/1')
        self.assertEqual(resp._status_code, 200)

    def test_delete_group_by_id_negative(self):
        resp = self.app.delete('/group/199999')
        self.assertEqual(resp._status_code, 404)
        self.assertIn("There is no group with such id", resp.json['message'])


class GroupWithSongResourceCase(unittest.TestCase):
    def setUp(self):
        self.application = create_app(config_class=TestConfig)
        Base.metadata.create_all(bind=self.application.engine)
        initial_fill(self.application)
        create_api(self.application)
        self.app = self.application.test_client()

    def tearDown(self):
        Base.metadata.drop_all(bind=self.application.engine)

    def test_post_group_with_songs_positive(self):
        data = [{
            "name": "Papa Roach",
            "description": "американская рок-группа из города Вакавилль, штат Калифорния, образованная в 1993 году. "
                           "Обрела мировую известность благодаря своему дебютному мэйджор-альбому Infest (2000)."
                           "К настоящему моменту группа выпустила 8 мини-альбомов, 1 концертный альбом и 9 студийных "
                           "альбомов",
            "official_site": "http://www.paparoach.com/",
            "songs": [{
                "title":"I Almost Told You That I Loved You",
                "text": """You know I love it when you're down on your knees\nAnd I'm a junkie for the way that you please\nYou shut me up when you swallow me down\nMy back to the wall you're going to town\nI almost told you that I loved you\nThank God I didn't 'cause it would have been a lie\nI say the damnedest things when you're on top of me\nI almost told you that I loved you\nI hate to say it but it has to be said\nYou look so fragile as I fuck with your head\nI know it shouldn't but it's getting me on\nIf sex is the drug then what is the cost?\nI almost told you that I loved you\nThank God I didn't 'cause it would have been a lie\nI say the damnedest things when you're on top of me\nI almost told you that I loved you\nI'm not the one that you want\nNot the one that you need\nMy love…""",
                "year": "2009",
                "youtube_link": "https://www.youtube.com/watch?v=OHs5cg5RIu8"
                },
                {
                "title":"Scars",
                "text": "I tear my heart open\nI sew myself shut\nMy weakness is\nThat I care too much\nMy scars remind us\nThat the past is real\nI tear my heart open\nJust to feel\nDrunk and I'm feeling down\nAnd I just want to be alone\nI'm pissed cause you came around\nWhy don't you just go home\n'Cause you channel all your pain\nAnd I can't help you go fix yourself\nYour making me insane\nAll I can say is\nI tear my heart open\nI sew myself shut\nMy weakness is\nThat I care too much\nOur scars remind us\nThat the past is real\nI tear my heart\nOpen just to feel\nI tried to help you once\nAgainst my own advice\nI saw you going down\nBut you never realized\nThat your drowning in the water\nSo I offered you my hand\nCompassion's in my nature\nTonight is our last stand\nI tear my heart open\nI sew myself shut\nMy weakness is\nThat I…",
                "year": "2009",
                "youtube_link": "https://www.youtube.com/watch?v=eHbNU9WuVgw"
                }]
            },
            {
            "name": "Garbage",
            "description": "британско-американская рок-группа, сформированная в городе Мэдисон в 1994 году[4]. В состав"
                           "группы входят шотландская певица Ширли Мэнсон (вокал, гитара, клавишные) и американские"
                           "музыканты Стив Маркер (гитара, клавишные), Дюк Эриксон (бас-гитара, клавишные, гитара, "
                           "перкуссия) и Бутч Виг (ударные, перкуссия). Коллектив стал известен своим необычным "
                           "звучанием, выразительным вокалом солистки, а также инновационными средствами обработки "
                           "звука.",
            "official_site": "https://www.garbage.com/",
            "songs": [{
                "title": "Blood for puppies",
                "text": "Salute the sun, I've been sitting here all night long\nHauling rock over Buddha with the Longhorn\nGot a hole, rip a pocket off my uniform\nWith the Blackwatch Boys get your heads down\nDuty calls but it is way too late I'm too far gone\nWaiting for Godot, hell with my pants down\nCracked the stash sent me crying in the midday sun\nI miss my dog and I miss my freedom\nI don't know why they are calling on the radio\nThey know I'm here just out of sight\nI don't know why they're calling on the radio\nHe's by my side and I know I'm right\nI don't know why they are calling on the radio\nThey know I'm here just out of sight\nI don't know why they're calling on the radio\nHe's by my side and I know I'm right\nI hate the things I think about you when I'm all alone\nI know you're tough but I've been gone for so long\nI play the memories of you inside my head\nSo all those pictures of us burn and radiate\nWatch the clouds and I'm falling, falling through the cracks\nHead beats and the heart is pounding fast\nOff the ground into the starry dark\nInto your arms I'm falling\nI'm falling, I'm falling\nI don't know why they are calling on the radio\nThey know I'm here just out of sight\nI don't know why they're calling on the radio\nHe's by my side and I know I'm right\nI don't know why they are calling on the radio\nThey know I'm here just out of sight\nI don't know why they're calling on the radio\nHe's by my side and I know I'm right\nMy brain, my body's fried\nI've got to stay alive\nI've got to take a chance and keep on moving\nKeep on moving\nI don't know why they are calling on the radio\nThey know I'm here just out of sight\nDon't know why they're calling on the radio\nHe's by my side and I know I'm right\nDon't know why they are calling on the radio\nIt's on my side and I know I'm right\nI don't know why they are calling on the radio\nIt's on my side and I know I'm alright\nI see your light from miles away\nI see your light from miles away",
                "year": "2012",
                "youtube_link": "https://www.youtube.com/watch?v=4OdTBCgqRt4"
                },
                {
                "title": "Only Happy When It Rains",
                "text": "I'm only happy when it rains\nI'm only happy when it's complicated\nAnd though I know you can't appreciate it\nI'm only happy when it rains\nYou know I love it when the news is bad\nWhy it feels so good to feel so sad?\nI'm only happy when it rains\nPour your misery down\nPour your misery down on me\nPour your misery down\nPour your misery down on me\nI'm only happy when it rains\nI feel good when things are goin' wrong\nI only listen to the sad, sad songs\nI'm only happy when it rains\nI only smile in the dark\nMy only comfort is the night gone black\nI didn't accidentally tell you that\nI'm only happy when it rains\nYou'll get the message by the time I'm through\nWhen I complain about me and you\nI'm only happy when it rains\nPour your misery down (Pour your misery down)\nPour your misery down on me\nPour your misery down (Pour your misery down)\nPour your misery down on me\nPour your misery down (Pour your misery down)\nPour your misery down on me\nPour your misery down\nYou can keep me company\nAs long as you don't care\nI'm only happy when it rains\nYou wanna hear about my new obsession?\nI'm riding high upon a deep depression\nI'm only happy when it rains\nPour some misery down on me\nI'm only happy when it rains\nPour some misery down on me\nI'm only happy when it rains\nPour some misery down on me\nI'm only happy when it rains\nPour some misery down on me\nI'm only happy when it rains\nPour some misery down on me\nPour some misery down on me\nPour some misery down on me\nPour some misery down on me\nPour some misery down on me\nPour some misery down on me",
                "year": "2013",
                "youtube_link": "https://www.youtube.com/watch?v=GpBFOJ3R0M4"
                }]
            }]
        resp = self.app.post('/group/song', data=json.dumps(data), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp._status_code, 201)
        data1 = {
            "name": "Within Temptation",
            "description": "американская рок-группа из города Вакавилль, штат Калифорния, образованная в 1993 году. "
                           "Обрела мировую известность благодаря своему дебютному мэйджор-альбому Infest (2000)."
                           "К настоящему моменту группа выпустила 8 мини-альбомов, 1 концертный альбом и 9 студийных "
                           "альбомов",
            "official_site": "https://www.resist-temptation.com/"
        }
        resp1 = self.app.post('/group/song', data=json.dumps(data1), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp1._status_code, 201)

    def test_post_group_with_songs_negative(self):
        data = {
            "description": "американская рок-группа из города Вакавилль, штат Калифорния, образованная в 1993 году. "
                           "Обрела мировую известность благодаря своему дебютному мэйджор-альбому Infest (2000)."
                           "К настоящему моменту группа выпустила 8 мини-альбомов, 1 концертный альбом и 9 студийных "
                           "альбомов",
            "official_site": "https://www.resist-temptation.com/"
        }
        resp = self.app.post('/group/song', data=json.dumps(data), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp._status_code, 400)
        self.assertIn("Required args are missing", resp.json['message'])
        data1 = {
            "name": "latexfauna",
            "description": "американская рок-группа из города Вакавилль, штат Калифорния, образованная в 1993 году. "
                           "Обрела мировую известность благодаря своему дебютному мэйджор-альбому Infest (2000)."
                           "К настоящему моменту группа выпустила 8 мини-альбомов, 1 концертный альбом и 9 студийных "
                           "альбомов",
            "official_site": "https://www.resist-temptation.com/",
            "songs": [{
                "title": "LIME",
                "text": """Мене в тобі всьо устраює\nОсобливо липень\nОсобливо липень\nБасейн клоне на сон\nЯ багато випив\nЯ багато випив\nІ лайм\nІ лаймові небеса\nІ лайм\nІ лаймові небеса\nМене всьо устраює\nШо ти людина\nНайнебезпечніший в світі звір\nНаші теплі новини\nНалежать лише мені\nЛа-ла-ла\nЛа-ла-ла\nІ ми крісіві\nУ світлі лаймових небес\nІ нас розум\nЯдерний процес\nМене в тобі всьо устраює\nОсобливо липень\nОсобливо липень\nБасейн клоне на сон\nЯ багато випив\nЯ багато випив\nІ лайм\nІ лаймові небеса\nІ лайм\nІ лаймові небеса\nМене всьо устраює\nШо я людина\nНайбезпорадніший в світі звір\nЯ безсмертна дитина\nІ я багато чого хотів\nІ мав, мав, мав\nЛав, лав, лав\nОдна й та сама штука\nПозаду твоїх і моїх очей\nДивиться на вічність\nТрогатєльних речей\nМене в тобі всьо устраює\nОсобливо липень\nОсобливо липень\nБасейн клоне на сон\nЯ багато випив\nЯ багато випив\nІ лайм\nІ лаймові небеса\nІ лайм\nІ лаймові небеса\nМене всьо устраює\nОсобливо липень\nОсобливо липень""",
                "year": "2017",
                "youtube_link": "https://www.youtube.com/watch?v=-UqKwEEkX2s",
                "group_id": 1
            }]
        }
        resp1 = self.app.post('/group/song', data=json.dumps(data1), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp1._status_code, 400)
        self.assertIn("Such song from this group already exists", resp1.json['message'])
        data2 = {
            "name": "latexfauna",
            "description": "американская рок-группа из города Вакавилль, штат Калифорния, образованная в 1993 году. "
                           "Обрела мировую известность благодаря своему дебютному мэйджор-альбому Infest (2000)."
                           "К настоящему моменту группа выпустила 8 мини-альбомов, 1 концертный альбом и 9 студийных "
                           "альбомов",
            "official_site": "https://www.resist-temptation.com/",
            "songs": [{
                "text": """Мене в тобі всьо устраює\nОсобливо липень\nОсобливо липень\nБасейн клоне на сон\nЯ багато випив\nЯ багато випив\nІ лайм\nІ лаймові небеса\nІ лайм\nІ лаймові небеса\nМене всьо устраює\nШо ти людина\nНайнебезпечніший в світі звір\nНаші теплі новини\nНалежать лише мені\nЛа-ла-ла\nЛа-ла-ла\nІ ми крісіві\nУ світлі лаймових небес\nІ нас розум\nЯдерний процес\nМене в тобі всьо устраює\nОсобливо липень\nОсобливо липень\nБасейн клоне на сон\nЯ багато випив\nЯ багато випив\nІ лайм\nІ лаймові небеса\nІ лайм\nІ лаймові небеса\nМене всьо устраює\nШо я людина\nНайбезпорадніший в світі звір\nЯ безсмертна дитина\nІ я багато чого хотів\nІ мав, мав, мав\nЛав, лав, лав\nОдна й та сама штука\nПозаду твоїх і моїх очей\nДивиться на вічність\nТрогатєльних речей\nМене в тобі всьо устраює\nОсобливо липень\nОсобливо липень\nБасейн клоне на сон\nЯ багато випив\nЯ багато випив\nІ лайм\nІ лаймові небеса\nІ лайм\nІ лаймові небеса\nМене всьо устраює\nОсобливо липень\nОсобливо липень""",
                "youtube_link": "https://www.youtube.com/watch?v=-UqKwEEkX2s",
                "group_id": 1
            }]
        }
        resp2 = self.app.post('/group/song', data=json.dumps(data2), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp2._status_code, 400)
        self.assertIn("Required args are missing", resp2.json['message'])
        data3 = "sdgdafg"
        resp3 = self.app.post('/group/song', data=json.dumps(data3), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp3._status_code, 400)
        self.assertIn("your request is inappropriate!", resp3.json['message'])


class SongResourceCase(unittest.TestCase):
    def setUp(self):
        self.application = create_app(config_class=TestConfig)
        Base.metadata.create_all(bind=self.application.engine)
        initial_fill(self.application)
        create_api(self.application)
        self.app = self.application.test_client()

    def tearDown(self):
        Base.metadata.drop_all(bind=self.application.engine)

    def test_get_song_by_id_positive(self):
        pass

    def test_get_song_by_id_negative(self):
        pass

    def test_get_list_of_songs_positive(self):
        pass

    def test_get_list_of_songs_negative(self):
        pass

    def test_post_list_of_songs_positive(self):
        pass

    def test_post_list_of_songs_negative(self):
        pass

    def test_put_song_by_id_positive(self):
        pass

    def test_put_song_by_id_negative(self):
        pass

    def test_delete_song_by_id_positive(self):
        pass

    def test_delete_song_by_id_negative(self):
        pass


class CreateSongByGroupIdResourceCase(unittest.TestCase):
    def setUp(self):
        self.application = create_app(config_class=TestConfig)
        Base.metadata.create_all(bind=self.application.engine)
        initial_fill(self.application)
        create_api(self.application)
        self.app = self.application.test_client()

    def tearDown(self):
        Base.metadata.drop_all(bind=self.application.engine)

    def test_post_create_song_by_group_id_positive(self):
        pass

    def test_post_create_song_by_group_id_negative(self):
        pass


class UserProfileResourceCase(unittest.TestCase):
    def setUp(self):
        self.application = create_app(config_class=TestConfig)
        Base.metadata.create_all(bind=self.application.engine)
        initial_fill(self.application)
        create_api(self.application)
        self.app = self.application.test_client()

    def tearDown(self):
        Base.metadata.drop_all(bind=self.application.engine)

    def test_get_user_by_id_positive(self):
        pass

    def test_get_user_by_id_negative(self):
        pass

    def test_post_user_positive(self):
        pass

    def test_post_user_negative(self):
        pass

    def test_put_user_by_id_positive(self):
        pass

    def test_put_user_by_id_negative(self):
        pass


if __name__ == '__main__':
    unittest.main()
