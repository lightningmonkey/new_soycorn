import os
from django.shortcuts import render, get_object_or_404
from new_soycorn.models import Article
from django.templatetags.static import static
from django.conf import settings


def index(request):
    latest_article_list = Article.objects.order_by('-pub_date')[:5]
    context = {'latest_article_list': latest_article_list}
    return render(request, 'new_soycorn/base.html', context)


def article(request, article_id):
    article_obj = get_object_or_404(Article, pk=article_id)
    with open(os.path.join(settings.STATIC_ROOT, article_obj.file)) as f:
        lines = f.read()
    print("lines: {0}".format(lines))

    context = {'article_str': article_obj.__str__(),
               'lines': lines}

    return render(request, 'new_soycorn/article.html', context)