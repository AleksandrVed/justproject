from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from . import models
from . import forms

def index(request):
    return render(request, 'main/index.html')

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
    return render(request, 'main/profile.html')

class RegisterUserView(CreateView):
    model = models.AdvUser
    template_name = 'main/register_user.html'
    form_class = forms.RegisterUserForm
    success_url = reverse_lazy('register_done')

class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'