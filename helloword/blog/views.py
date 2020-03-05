from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from .admin import Article


def article_content(request):
    article = Article.objects.all()[0]
    title = article.title
    brief_content = article.brief_content
    content = article.content
    ti = article.publish_date
    a_atr = f'标题: {title}, 摘要: {brief_content}' \
            f'内容: {content}, 发布日期: {ti}'
    return HttpResponse(a_atr)


def article1(request):
    page = request.GET.get('page')
    if not page:
        page = 1
    page = int(page)
    article = Article.objects.all()
    p = Paginator(article, 2)
    p_num = p.num_pages
    p_list = p.page(page)
    if p_list.has_next():
        n_page = page + 1
    else:
        n_page = page
    if p_list.has_previous():
        u_page = page - 1
    else:
        u_page = page
    return render(request, 'article.html', {
        'articles': p_list,
        'p_num': range(1, p_num + 1),
        'n_page': n_page,
        'u_page': u_page
    })


def detail(request, article_id):
    articles = Article.objects.all()
    for article_index, article in enumerate(articles):
        if article_id == article.aticle_id:
            if article_index == 0:
                up_article = 0
                next_article = article_index + 1
            elif article_index == len(articles) - 1:
                up_article = article_index - 1
                next_article = len(articles) - 1
            else:
                up_article = article_index - 1
                next_article = article_index + 1
            return render(request, 'detail.html', {
                'article': article,
                'up_article': articles[up_article],
                'next_article': articles[next_article]
            })

    def not_found(request, e):
        return HttpResponse('not')
