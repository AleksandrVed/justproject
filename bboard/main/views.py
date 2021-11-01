from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from . import models, forms
from .utilites import signer
from django.core.signing import BadSignature
from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    bbs = models.Bb.objects.filter(is_active=True)[:10]
    context = {'bbs': bbs}
    return render(request, 'main/index.html', context)

def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

class BBLoginView(LoginView):
    template_name = 'main/login.html'

class BBLogoutView(LogoutView):
    template_name = 'main/logout.html'

class ChangeUserInfoView(UpdateView):
    model = models.AdvUser
    template_name = 'main/change_user_info.html'
    form_class = forms.ChangeUserInfoForm
    success_url = reverse_lazy('profile')
    success_message = 'Данные успешно изменены'
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('profile')
    success_message = 'Данные успешно изменены'

@login_required
def profile(request):
    bbs = models.Bb.objects.filter(author=request.user.pk)
    context = {'bbs':bbs}
    return render(request, 'main/profile.html', context)

class RegisterUserView(CreateView):
    model = models.AdvUser
    template_name = 'main/register_user.html'
    form_class = forms.RegisterUserForm
    success_url = reverse_lazy('register_done')

class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'

def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(models.AdvUser, username=username)
    if user.is_active:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        #user.is_activated = True
        user.save()
    return render(request, template)

class DeleteUserView(DeleteView):
    model = models.AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('login')
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удалён')
        return super().post(request, *args, **kwargs)
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

def by_rubric(request, pk):
    rubric = get_object_or_404(models.SubRubric, pk = pk)
    bbs = models.Bb.objects.filter(is_active = True, rubric =pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(title__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''
    form = forms.SearchForm(initial={'keyword': keyword})
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubric': rubric, 'page': page, 'bbs': page.object_list, 'form': form}
    return render(request, 'main/by_rubric.html', context)

def detail(request, rubric_pk, pk):
    bb = get_object_or_404(models.Bb, pk=pk)
    ais = bb.additionalimage_set.all()
    context = {'bb': bb, 'ais': ais}
    return render(request, 'main/detail.html', context)

def profile_bb_detail(request, pk):
    bb = get_object_or_404(models.Bb, pk = pk)
    ais = bb.additionalimage_set.all()
    return render(request, 'main/profile_bb_detail.html', context={'bb': bb, 'ais': ais})