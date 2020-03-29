from blog.forms import CommentForm
from .models import Post, Tag, Comment
from django.db.models import Count, Prefetch
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import slugify
from django.shortcuts import redirect
from django.urls import reverse


class TagListView(ListView):
    template_name = 'blog/list-tag.html'
    model = Tag
    context_object_name = 'list_tag'

    def get_queryset(self):
        queryset = Tag.objects \
            .all() \
            .prefetch_related(Prefetch('posts', to_attr='list_post')) \
            .annotate(total_post=Count('posts')) \
            .order_by('-total_post')
        return queryset


class TagDetailView(DetailView):
    template_name = 'blog/detail-tag.html'
    model = Tag
    context_object_name = 'detail_tag'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        queryset = Tag.objects \
            .filter(slug=slug) \
            .annotate(total_post=Count('posts'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        list_post = Post.objects \
            .filter(tag=self.object) \
            .annotate(total_comment=Count('comments')) \
            .order_by('-created_at')

        page = self.kwargs.get('page')
        paginator = Paginator(list_post, 5)
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
            'list_post': list_post_per_page,
            'total_page': paginator.num_pages,
            'list_highlights_tag': list_highlights_tag,
            'list_tag': list_tag,
            'list_last_comment': list_last_comment,
        })
        return context


class PostSearchView(TemplateView):
    template_name = 'blog/search-post.html'

    def post(self, request, **kwargs):

        search = self.request.POST.get('search', '')
        search_slug = slugify(search)

        return redirect(search_slug + '/')

    def get_context_data(self, **kwargs):
        context = super(PostSearchView, self).get_context_data(**kwargs)

        search = self.kwargs.get('search')

        search_text = search.replace('-', ' ')

        list_post = Post.objects \
                        .raw('SELECT COUNT(post.id) AS count, post.*, \
                        MATCH(post.title, post.description) AGAINST(%s IN BOOLEAN MODE) AS rank_post, \
                        MATCH(tag.name) AGAINST(%s IN BOOLEAN MODE) AS rank_tag \
                        FROM blog_post post \
                        INNER JOIN blog_post_tag post_tag ON post.id = post_tag.id \
                        INNER JOIN blog_tag tag ON tag.id = post_tag.id \
                        WHERE MATCH(post.title, post.description) AGAINST(%s IN BOOLEAN MODE) \
                        OR MATCH(tag.name) AGAINST(%s IN BOOLEAN MODE) GROUP BY post.id ORDER BY rank_post DESC, rank_tag DESC', \
                        [search_text, search_text, search_text, search_text])

        page = self.kwargs.get('page')

        paginator = Paginator(list_post, 5)
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

        search = {
            'content': search_text,
            'slug': search
        }

        context.update({
            'search': search,
            'list_post': list_post_per_page,
            'total_page': paginator.num_pages,
            'list_highlights_tag': list_highlights_tag,
            'list_tag': list_tag,
            'list_last_comment': list_last_comment,
        })
        return context


class PostDetailView(FormMixin, DetailView):
    template_name = 'blog/detail-post.html'
    model = Post
    context_object_name = 'detail_post'
    form_class = CommentForm

    def post(self, request, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            if not comment.name:
                comment.user_id = self.request.user.id
            comment.post_id = self.object.id
            comment.save()
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(PostDetailView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('blog:detail_post', kwargs={'slug': self.object.slug})

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        queryset = Post.objects \
            .filter(slug=slug) \
            .annotate(total_comment=Count('comments'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post_comment = self.object.comments.order_by('-created_at')[0:5]
        relate_post = Post.objects \
                          .filter(tag__name__in=list(self.object.tag.values_list('name', flat=True))) \
                          .annotate(total_comment=Count('comments')) \
                          .exclude(id=self.object.id) \
                          .order_by('-created_at')[:3]

        list_last_comment = Comment.objects.all() \
                                .prefetch_related('post') \
                                .prefetch_related('user') \
                                .order_by('-created_at')[:6]

        list_highlights_tag = Tag.objects \
                                  .filter(highlights=1) \
                                  .annotate(total_post=Count('posts')) \
                                  .order_by('name')[:5]

        context.update({
            'relate_post': relate_post,
            'post_comment': post_comment,
            'list_last_comment': list_last_comment,
            'list_highlights_tag': list_highlights_tag,
            'comment_form': self.get_form(),
        })
        return context
