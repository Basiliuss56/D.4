from django.views.generic import ListView, DetailView
from .filters import PostFilter
from .models import Post


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('created_time')
    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context



class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
