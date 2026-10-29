import urllib.request
import json

def post_json(url, data):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

# 1. Test transliterate
res_translit = post_json('http://127.0.0.1:8000/api/tools/transliterate/', {
    'text': "Buxoro davlat universiteti o'qituvchilari g'olib bo'lishdi, shahar, Is'hoq."
})
print("Transliterate API result:", res_translit['result'])

# 2. Test translate
res_trans = post_json('http://127.0.0.1:8000/api/tools/translate/', {
    'text': "Universitetda yangi ilmiy laboratoriya ochildi.",
    'source_lang': 'uz',
    'target_langs': ['ru', 'en', 'zh-cn']
})
print("Translate API RU:", res_trans['translations']['ru'])
print("Translate API EN:", res_trans['translations']['en'])

# 3. Test create article
res_create = post_json('http://127.0.0.1:8000/api/articles/', {
    'title_uz': "Yangi laboratoriya",
    'content_uz': "Matn",
    'title_ru': res_trans['translations']['ru'],
    'content_ru': "Текст",
    'category': "Ilmiy yangiliklar"
})
print("Create Article ID:", res_create['id'])
