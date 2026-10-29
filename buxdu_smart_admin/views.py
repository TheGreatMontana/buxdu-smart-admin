import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.apps import apps

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


@staff_member_required
@csrf_exempt
def api_bulk_action(request):
    """
    AJAX endpoint for bulk transliteration and translation on the Changelist (list view).
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body)
        app_label = data.get("app_label", "news")
        model_name = data.get("model_name", "article")
        ids = data.get("ids", [])
        action_type = data.get("action_type", "transliterate")  # 'transliterate', 'translate', 'both'

        model = apps.get_model(app_label, model_name)
        if not model:
            return JsonResponse({"success": False, "error": f"Model {app_label}.{model_name} topilmadi."}, status=404)

        if ids and len(ids) > 0:
            queryset = model.objects.filter(pk__in=ids)
        else:
            # If no specific IDs passed, apply to all objects in the model
            queryset = model.objects.all()

        updated_count = 0
        target_fields = [
            'sarlavha_uz', 'text_uz', 'title_uz', 'content_uz', 'nomi_uz',
            'fio_uz', 'ilmiy_unvoni_uz', 'address_uz', 'qabul_vaqti_uz',
            'mehnat_faoliyati_uz', 'malaka_oshirish_uz', 'oqitadigan_fanlari_uz',
            'ilmiy_faoliyati_uz', 'annotatsiya_uz', 'sarlavha', 'title', 'nomi', 'text'
        ]

        for obj in queryset:
            changed = False

            # 1. TRANSLITERATE
            if action_type in ("transliterate", "both"):
                for field_name in target_fields:
                    if hasattr(obj, field_name):
                        val = getattr(obj, field_name, None)
                        if val and isinstance(val, str):
                            new_val = to_new_uzbek_latin(val)
                            if new_val != val:
                                setattr(obj, field_name, new_val)
                                changed = True

            # 2. TRANSLATE
            if action_type in ("translate", "both"):
                # Find all _uz fields and translate them into _ru, _en, _zh
                for field_name in target_fields:
                    if hasattr(obj, field_name) and field_name.endswith('_uz'):
                        val = getattr(obj, field_name, None)
                        if val and isinstance(val, str) and val.strip():
                            base_name = field_name[:-3]
                            ru_field = f"{base_name}_ru"
                            en_field = f"{base_name}_en"
                            zh_field = f"{base_name}_zh"

                            needs_ru = hasattr(obj, ru_field)
                            needs_en = hasattr(obj, en_field)
                            needs_zh = hasattr(obj, zh_field)

                            if needs_ru or needs_en or needs_zh:
                                trans = translate_bundle(val, source_lang='uz', target_langs=['ru', 'en', 'zh-cn'])
                                if needs_ru and trans.get('ru'):
                                    setattr(obj, ru_field, trans['ru'])
                                    changed = True
                                if needs_en and trans.get('en'):
                                    setattr(obj, en_field, trans['en'])
                                    changed = True
                                if needs_zh and trans.get('zh-cn'):
                                    setattr(obj, zh_field, trans['zh-cn'])
                                    changed = True

            if changed:
                obj.save()
                updated_count += 1

        if action_type == "transliterate":
            msg = f"✅ Muvaffaqiyatli: {updated_count} ta maqola yangi 2026-yilgi lotin alifbosiga (Ö, Ğ, Ş, Ç) o'tkazildi va saqlandi!"
        elif action_type == "translate":
            msg = f"🎉 Ajoyib: {updated_count} ta maqola rus, ingliz va xitoy tillariga tarjima qilindi va saqlandi!"
        else:
            msg = f"🚀 Bajarildi: {updated_count} ta maqola yangi alifboga o'tkazildi va barcha tillarga (RU, EN, ZH) tarjima qilindi!"

        return JsonResponse({
            "success": True,
            "updated_count": updated_count,
            "message": msg
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)
