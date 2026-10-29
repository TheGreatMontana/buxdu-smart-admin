import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from news.models import (
    Article, Employee, Book, Category, Position, 
    TypeArticle, Menu, PhotoContent,
    Material, Xodim, Kategoriya, Lavozim, MaterialTuri
)
from buxdu_smart_admin.uzbek_alphabet import to_new_uzbek_latin
from buxdu_smart_admin.translator import translate_bundle


MODEL_MAP = {
    # Real buxdu.uz names
    'article': Article,
    'articles': Article,
    'materiallar': Article,
    'materials': Article,

    'employee': Employee,
    'employees': Employee,
    'xodimlar': Employee,

    'book': Book,
    'books': Book,

    'category': Category,
    'categories': Category,
    'kategoriyalar': Category,

    'position': Position,
    'positions': Position,
    'lavozimlar': Position,

    'typearticle': TypeArticle,
    'typearticles': TypeArticle,
    'materialturlari': TypeArticle,

    'menu': Menu,
    'menus': Menu,

    'photocontent': PhotoContent,
    'photocontents': PhotoContent,
    'photos': PhotoContent,
}


@csrf_exempt
def api_generic_list_create(request, model_name):
    model = MODEL_MAP.get(model_name.lower())
    if not model:
        return JsonResponse({'success': False, 'error': f'Model {model_name} topilmadi'}, status=404)

    if request.method == "GET":
        qs = model.objects.all()
        q = request.GET.get('search', '').strip()

        # Search filter
        if q:
            if hasattr(model, 'sarlavha_uz'):
                qs = qs.filter(sarlavha_uz__icontains=q)
            elif hasattr(model, 'fio_uz'):
                qs = qs.filter(fio_uz__icontains=q)
            elif hasattr(model, 'title_uz'):
                qs = qs.filter(title_uz__icontains=q)

        data = []
        for obj in qs:
            item = {'id': obj.id}
            for f in obj._meta.get_fields():
                if f.is_relation and f.many_to_one:
                    rel_obj = getattr(obj, f.name, None)
                    item[f.name] = str(rel_obj) if rel_obj else None
                    item[f"{f.name}_id"] = getattr(obj, f"{f.name}_id", None)
                elif not f.is_relation:
                    val = getattr(obj, f.name, None)
                    if hasattr(val, 'strftime'):
                        item[f.name] = val.strftime('%Y-%m-%d %H:%M')
                    else:
                        item[f.name] = str(val) if val is not None else ''
            data.append(item)

        return JsonResponse({'success': True, 'items': data, model_name: data})

    elif request.method == "POST":
        try:
            body = json.loads(request.body)
            valid_fields = {f.name for f in model._meta.get_fields() if not f.is_relation or f.many_to_one}
            create_kwargs = {}
            for k, v in body.items():
                if k in valid_fields:
                    create_kwargs[k] = v
                elif k.endswith('_id') and k[:-3] in valid_fields:
                    create_kwargs[k] = v

            obj = model.objects.create(**create_kwargs)
            return JsonResponse({'success': True, 'id': obj.id, 'message': "Muvaffaqiyatli saqlandi!"})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def api_generic_detail_update_delete(request, model_name, pk):
    model = MODEL_MAP.get(model_name.lower())
    if not model:
        return JsonResponse({'success': False, 'error': f'Model {model_name} topilmadi'}, status=404)

    try:
        obj = model.objects.get(pk=pk)
    except model.DoesNotExist:
        return JsonResponse({'success': False, 'error': "Yozuv topilmadi"}, status=404)

    if request.method == "GET":
        item = {'id': obj.id}
        for f in obj._meta.get_fields():
            if f.is_relation and f.many_to_one:
                rel = getattr(obj, f.name, None)
                item[f.name] = str(rel) if rel else None
                item[f"{f.name}_id"] = getattr(obj, f"{f.name}_id", None)
            elif not f.is_relation:
                v = getattr(obj, f.name, None)
                item[f.name] = v.strftime('%Y-%m-%d %H:%M') if hasattr(v, 'strftime') else (str(v) if v is not None else '')
        return JsonResponse({'success': True, 'item': item})

    elif request.method in ["PUT", "POST"]:
        try:
            body = json.loads(request.body)
            valid_fields = {f.name for f in model._meta.get_fields() if not f.is_relation or f.many_to_one}
            for k, v in body.items():
                if k in valid_fields:
                    setattr(obj, k, v)
                elif k.endswith('_id'):
                    setattr(obj, k, v)
            obj.save()
            return JsonResponse({'success': True, 'message': "Muvaffaqiyatli yangilandi!"})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    elif request.method == "DELETE":
        obj.delete()
        return JsonResponse({'success': True, 'message': "Muvaffaqiyatli o'chirildi!"})

    return JsonResponse({'error': 'Method not allowed'}, status=405)


# Transliteration tool
@csrf_exempt
def tool_transliterate(request):
    if request.method != "POST":
        return JsonResponse({'error': 'POST method required'}, status=405)
    try:
        body = json.loads(request.body)
        text = body.get('text', '')
        style = body.get('style', 'umlaut')
        converted = to_new_uzbek_latin(text, style=style)
        return JsonResponse({'success': True, 'result': converted})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# Translation tool
@csrf_exempt
def tool_translate(request):
    if request.method != "POST":
        return JsonResponse({'error': 'POST method required'}, status=405)
    try:
        body = json.loads(request.body)
        text = body.get('text', '')
        source_lang = body.get('source_lang', 'uz')
        target_langs = body.get('target_langs', ['ru', 'en', 'zh-cn'])
        translations = translate_bundle(text=text, source_lang=source_lang, target_langs=target_langs)
        return JsonResponse({'success': True, 'translations': translations})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# Bulk transliterate database tool (Senior feature!)
@csrf_exempt
def tool_bulk_transliterate(request):
    if request.method != "POST":
        return JsonResponse({'error': 'POST method required'}, status=405)
    try:
        body = json.loads(request.body)
        target_model_name = body.get('model', 'all')
        style = body.get('style', 'umlaut')

        models_to_process = []
        if target_model_name == 'all':
            models_to_process = [Article, Employee, Book, Category, Position, TypeArticle, Menu]
        elif target_model_name in MODEL_MAP:
            models_to_process = [MODEL_MAP[target_model_name]]

        stats = {'total_records': 0, 'updated_records': 0, 'fields_modified': 0}

        for model in models_to_process:
            uz_fields = [f.name for f in model._meta.get_fields() if f.name.endswith('_uz') and not f.is_relation]
            for obj in model.objects.all():
                stats['total_records'] += 1
                modified = False
                for field_name in uz_fields:
                    val = getattr(obj, field_name, '')
                    if val and isinstance(val, str):
                        new_val = to_new_uzbek_latin(val, style=style)
                        if new_val != val:
                            setattr(obj, field_name, new_val)
                            stats['fields_modified'] += 1
                            modified = True
                if modified:
                    obj.save()
                    stats['updated_records'] += 1

        return JsonResponse({'success': True, 'stats': stats, 'message': f"Ommaviy transliteratsiya yakunlandi: {stats['updated_records']} ta yozuv yangilandi!"})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# Dashboard stats
@csrf_exempt
def dashboard_stats(request):
    return JsonResponse({
        'success': True,
        'stats': {
            'materials': Article.objects.count(),
            'articles': Article.objects.count(),
            'xodimlar': Employee.objects.count(),
            'employees': Employee.objects.count(),
            'books': Book.objects.count(),
            'kategoriyalar': Category.objects.count(),
            'categories': Category.objects.count(),
            'lavozimlar': Position.objects.count(),
            'positions': Position.objects.count(),
            'materialturlari': TypeArticle.objects.count(),
            'typearticles': TypeArticle.objects.count(),
            'menus': Menu.objects.count(),
            'photos': PhotoContent.objects.count(),
            'photocontents': PhotoContent.objects.count(),
        }
    })
