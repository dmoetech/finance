from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View
from django.contrib.auth import logout as logout_user
from django.contrib.auth import login as login_user
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from apps.core.views import CustomInvalidFormMixin
from apps.alternative.models import Depot as AlternativeDepot
from apps.banking.models import Depot as BankingDepot
from apps.crypto.models import init_crypto as crypto_init_crypto
from apps.crypto.models import Depot as CryptoDepot
from apps.users.forms import SignInUserForm
from apps.users.forms import UpdateCryptoStandardUserForm
from apps.users.forms import UpdateGeneralStandardUserForm
from apps.users.forms import UpdateStandardUserForm
from apps.users.forms import CreateStandardUserForm
from apps.users.models import StandardUser


class SignUpView(CustomInvalidFormMixin, generic.CreateView):
    form_class = CreateStandardUserForm
    model = StandardUser
    template_name = "users_signup.njk"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:redirect', permanent=False)
        else:
            return super(SignUpView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data()
        context["sign_up_form"] = self.get_form()
        return context

    def form_valid(self, form):
        user = form.save()
        login_user(self.request, user)
        return redirect('core:redirect', permanent=False)


class SignInView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:redirect', permanent=False)
        else:
            context = {"sign_in_form": SignInUserForm()}
            return render(request, "users_signin.njk", context=context)

    def post(self, request):
        form = SignInUserForm(request.POST)
        if not request.user.is_authenticated and form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login_user(request, user)
            else:
                messages.error(request, "This combination of username and password doesn't exist.")
        return redirect('core:redirect', permanent=False)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout_user(request)
        return redirect('core:redirect')


class SettingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = "users_settings.njk"

    def get_context_data(self, **kwargs):
        context = dict()
        context["user"] = self.request.user
        context["edit_user_form"] = UpdateStandardUserForm(instance=self.request.user)
        context["edit_user_password_form"] = PasswordChangeForm(user=self.request.user)
        context["edit_user_general_form"] = UpdateGeneralStandardUserForm(
            instance=self.request.user)

        # banking
        context["banking_depots"] = context["user"].banking_depots.all()
        # crypto
        context["crypto_depots"] = context["user"].crypto_depots.all()
        context["edit_user_crypto_form"] = UpdateCryptoStandardUserForm(instance=self.request.user)
        # alternative
        context["alternative_depots"] = context["user"].alternative_depots.all()
        return context


def init_banking(request):
    user = request.user
    request.user.create_random_banking_data()
    user.banking_is_active = True
    user.save()
    return HttpResponseRedirect(reverse_lazy("users:settings"))


def init_crypto(request):
    user = request.user
    crypto_init_crypto(user)
    user.crypto_is_active = True
    user.save()
    return HttpResponseRedirect(reverse_lazy("users:settings"))


def init_alternative(request):
    user = request.user
    # alternative_init_alternative(user)
    user.alternative_is_active = True
    user.save()
    return HttpResponseRedirect(reverse_lazy("users:settings"))


def set_banking_depot_active(request, slug, pk):
    depot_pk = int(pk)
    depot = BankingDepot.objects.get(pk=depot_pk)
    request.user.set_banking_depot_active(depot)
    return HttpResponseRedirect(reverse_lazy("users:settings", args=[request.user.slug]))


def set_crypto_depot_active(request, slug, pk):
    depot_pk = int(pk)
    depot = CryptoDepot.objects.get(pk=depot_pk)
    request.user.set_crypto_depot_active(depot)
    return HttpResponseRedirect(reverse_lazy("users:settings", args=[request.user.slug]))


def set_alternative_depot_active(request, slug, pk):
    depot_pk = int(pk)
    depot = AlternativeDepot.objects.get(pk=depot_pk)
    request.user.set_alternative_depot_active(depot)
    return HttpResponseRedirect(reverse_lazy("users:settings", args=[request.user.slug]))