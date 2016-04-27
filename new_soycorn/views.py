import os

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from new_soycorn.models import Article
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static



PAGE_LIMIT = 20
PAGE_OFFSET = PAGE_LIMIT


def index(request):
    article_list = _get_articles(1)
    context = {'latest_article_list': article_list}
    return render(request, 'new_soycorn/index.html', context)


def faq(request):
    return render(request, 'new_soycorn/faq.html', {})


def contact_us(request):
    return render(request, 'new_soycorn/contact_us.html', {})


def about_us(request):
    return render(request, 'new_soycorn/about_us.html', {})


def pdf_view(request):
    name = request.GET.get('name', None)
    if not name:
        raise Http404("PDF does not exist")
    try:
        with open('new_soycorn/static/new_soycorn/pdf/{0}.pdf'.format(name), 'r') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=some_file.pdf'
            return response
    except Exception:
        raise  Http404("PDF did not work")

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
        all_lines = f.readlines()
    # print("lines: {0}".format(lines))
    date = all_lines[0]
    title = all_lines[1]
    lines = " ".join(all_lines[2:])
    context = {'article_str': article_obj.__str__(),
               'date': date,
               'title': title,
               'lines': lines}

    return render(request, 'new_soycorn/article_single.html', context)