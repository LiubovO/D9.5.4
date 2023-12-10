from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import Post, Author, Appointment, Category, CategorySubscribe, PostCategory
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives, mail_admins
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

class PostsList(ListView):

    model = Post
    ordering = '-id'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        context['isauthor'] = self._isauthor()

        return context

    def _isauthor(self):
        try:
            Author.objects.get(user=self.request.user)
            return True
        except Author.DoesNotExist:
            return False

class PostsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_category(self, **kwargs):
        self.object.post = PostCategory.objects.get(post_id=self.id)
        return PostCategory.objects.get(pk=id)


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.author = Author.objects.get(user=self.request.user)
    #     if 'post' in self.request.path:
    #         type_ = 'PST'
    #     elif 'news' in self.request.path:
    #         type_ = 'NWS'
    #     self.object.type = type_
    #     return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'post_edit.html'
    form_class = PostForm
    model = Post

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('postlist')


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'appointments/make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # получаем наш html
        html_content = render_to_string(
            'appointments/appointment_created.html',
            {
                'appointment': appointment,
            }
        )

        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%m-%d")}',
            body=appointment.message,  # это то же, что и message
            from_email='for.skillfactory@yandex.ru',
            to=['lyubaol@mail.ru'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "appointment/appointment_created.html")  # добавляем html

        mail_admins(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )

        msg.send()

        return redirect('appointment_created')

class CategoryPost(DetailView):
    model = Category
    template_name = 'categories/post_category.html'
    context_object_name = 'postcategory'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(category=kwargs['object'])
        return context


# Добавление категории:
class AddCategoryView(CreateView):
    model = Category
    template_name = 'categories/add_category.html'
    fields = '__all__'


# Список категорий:
class CategoryList(ListView):
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'category'


# Функция позволяющая подписаться на категорию
def subscribe_to_category(request, pk):

    current_user = request.user
    CategorySubscribe.objects.create(category=Category.objects.get(pk=pk), subscriber=User.objects.get(pk=current_user.id))

    return render(request, 'subscribe.html')