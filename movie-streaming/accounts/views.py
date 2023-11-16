from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.urls import reverse_lazy
from accounts.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from accounts.forms import UserCreateForm


from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

class Auth(View):
    def get(self, request):
        return render(request, 'accounts/login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('movies')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')

class Logout(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logout successful.')
        return redirect('login')
        
class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('movies')  # Redirect to login page after successful registration

    def get(self, request):
        #to avoid the rendering the default form
        return render(request, self.template_name)

    def post(self, request, *args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            return redirect('movies')
        else:
            return render(request, self.template_name, {'form': form.errors})
