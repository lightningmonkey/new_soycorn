import os
from django.shortcuts import render, get_object_or_404
from new_soycorn.models import Article
from django.templatetags.static import static
from django.conf import settings

PAGE_LIMIT = 20
PAGE_OFFSET = 20


def index(request):
    article_list = _get_articles(1)
    context = {'latest_article_list': article_list}
    return render(request, 'new_soycorn/index.html', context)


def article_page(request, page_number):
    try:
        page_number = int(page_number)
    except:
        page_number = 1
    if page_number < 1:
        page_number = 1
    article_list = _get_articles(page_number)
    context = {'latest_article_list': article_list,
               'next_page': page_number+1,
               'prev_page': page_number-1}
    return render(request, 'new_soycorn/article_page.html', context)


def _get_articles(page_number):
    sorted_articles = Article.objects.order_by('-pub_date')
    current_offset = PAGE_OFFSET * page_number
    current_limit = PAGE_LIMIT * (page_number-1)
    article_list = sorted_articles[current_limit:current_offset]
    return article_list


def article_single(request, article_id):
    article_obj = get_object_or_404(Article, pk=article_id)
    with open(os.path.join(settings.STATIC_ROOT, "articles/{0}".format(article_obj.file))) as f:
        lines = f.read()
    print("lines: {0}".format(lines))

    context = {'article_str': article_obj.__str__(),
               'lines': lines}

    return render(request, 'new_soycorn/article_single.html', context)