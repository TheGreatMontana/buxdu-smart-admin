import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required

from .uzbek_alphabet import to_new_uzbek_latin, to_old_uzbek_latin
from .translator import translate_bundle, translate_text


@staff_member_required
def api_transliterate(request):
    """
    AJAX endpoint for instant transliteration into the new Uzbek Latin alphabet.
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body)
        text = data.get("text", "")
        direction = data.get("direction", "to_new")
        style = data.get("style", "umlaut")

        if direction == "to_old":
            result = to_old_uzbek_latin(text)
        else:
            result = to_new_uzbek_latin(text, style=style)

        return JsonResponse({"success": True, "result": result})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@staff_member_required
def api_translate(request):
    """
    AJAX endpoint for multi-language translation.
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body)
        text = data.get("text", "")
        source_lang = data.get("source_lang", "uz")
        target_langs = data.get("target_langs", ["ru", "en", "zh-cn"])

        translations = translate_bundle(
            text=text,
            source_lang=source_lang,
            target_langs=target_langs
        )

        return JsonResponse({"success": True, "translations": translations})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)
