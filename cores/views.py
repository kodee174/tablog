from blog.models import Post, Tag, Comment
from django.db.models import Count
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


class HomePageView(TemplateView):
    template_name = 'homepages/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        list_highlights_post = Post.objects \
                                   .filter(highlights=1) \
                                   .prefetch_related('tag') \
                                   .annotate(total_comment=Count('comments')) \
                                   .order_by('-updated_at')[:5]

        list_new_post = Post.objects \
            .all() \
            .annotate(total_comment=Count('comments')) \
            .order_by('-created_at')

        page = self.kwargs.get('page')

        paginator = Paginator(list_new_post, 5)
        try:
            list_post_per_page = paginator.page(page)
        except PageNotAnInteger:
            list_post_per_page = paginator.page(1)
        except EmptyPage:
            list_post_per_page = paginator.page(paginator.num_pages)

        list_highlights_tag = Tag.objects \
                                  .filter(highlights=1) \
                                  .annotate(total_post=Count('posts')) \
                                  .order_by('name')[:5]

        list_tag = Tag.objects \
                       .all() \
                       .annotate(total_post=Count('posts')) \
                       .order_by('-id')[:10]

        list_last_comment = Comment.objects.all() \
                                .prefetch_related('post') \
                                .prefetch_related('user') \
                                .order_by('-created_at')[:6]

        context.update({
            'list_new_post': list_post_per_page,
            'total_page': paginator.num_pages,
            'list_highlights_post': list_highlights_post,
            'list_highlights_tag': list_highlights_tag,
            'list_tag': list_tag,
            'list_last_comment': list_last_comment,
        })
        return context


class AboutView(TemplateView):
    template_name = 'homepages/about.html'


class ContactView(TemplateView):
    template_name = 'homepages/contact.html'

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)

        list_highlights_tag = Tag.objects \
                                  .filter(highlights=1) \
                                  .annotate(total_post=Count('posts')) \
                                  .order_by('name')[:5]

        list_last_comment = Comment.objects.all() \
                                .prefetch_related('post') \
                                .prefetch_related('user') \
                                .order_by('-created_at')[:6]

        context.update({
            'list_highlights_tag': list_highlights_tag,
            'list_last_comment': list_last_comment,
        })
        return context


def bad_request(request, exception=None):
    return render(request, 'cores/error.html', status=400)


def permission_denied(request, exception=None):
    return render(request, 'cores/error.html', status=403)


def page_not_found(request, exception=None):
    return render(request, 'cores/error.html', status=404)


def server_error(request, exception=None):
    return render(request, 'cores/error.html', status=500)
