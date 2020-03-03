from django.views.generic.edit import FormMixin
from django.template.loader import render_to_string
from finance.core.forms import DeleteForm
from django.utils.html import strip_tags
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse_lazy

import json
import re

from finance.core.models import Page


# mixins
class CustomAjaxDeleteMixin(object):
    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        object.delete()
        return HttpResponse(json.dumps({"valid": True}), content_type="application/json")


class CustomAjaxFormMixin(object):
    def form_invalid(self, form):
        html = render_to_string(self.template_name, self.get_context_data(form=form),
                                request=self.request)
        return HttpResponse(json.dumps({"valid": False, "html": html}),
                            content_type="application/json")

    def form_valid(self, form):
        form.save()
        return HttpResponse(json.dumps({"valid": True}), content_type="application/json")


class CustomInvalidFormMixin(object):
    def form_invalid(self, form):
        message = ["Form Error(s):"]
        for field in form:
            if field.errors:
                text = "{}: {}".format(field.label, strip_tags(field.errors))
                message.append(text)
        message = "<br>".join(message)
        messages.warning(self.request, message)
        return self.render_to_response(self.get_context_data(form=form))


# views
class CustomDeleteView(generic.View):
    def post(self, request, *args, **kwargs):
        form = DeleteForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form):
        raise NotImplementedError()

    def form_invalid(self, form, **kwargs):
        raise NotImplementedError()


class IndexView(generic.TemplateView):
    template_name = "core_index.njk"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["pages"] = Page.objects.order_by("-ordering")
        return context


class OldIndexView(generic.TemplateView):
    template_name = "core_index_old.njk"

    def get_context_data(self, **kwargs):
        context = super(OldIndexView, self).get_context_data(**kwargs)
        context["pages"] = Page.objects.order_by("-ordering")
        return context


class RedirectView(generic.RedirectView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            front_page = request.user.front_page
            if front_page == "BANKING":
                return redirect("banking:index", permanent=False)
            elif front_page == "CRYPTO":
                return redirect("crypto:index", permanent=False)
            elif front_page == "ALTERNATIVE":
                return redirect("alternative:index", permanent=False)
            else:
                return redirect("users:settings", permanent=False)
        else:
            return redirect('users:signin', permanent=False)


class PageView(generic.TemplateView):
    template_name = "core_page.njk"

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)
        context["pages"] = Page.objects.order_by("-ordering")
        context["page"] = get_object_or_404(Page, slug=self.kwargs['slug'])
        return context


class DataProtectionView(generic.TemplateView):
    template_name = "core_dataprotection.njk"


class ImprintView(generic.TemplateView):
    template_name = "core_imprint.njk"


class TermsOfUseView(generic.TemplateView):
    template_name = "core_termsofuse.njk"


class StaticRedirectView(RedirectView):
    def get(self, request, *args, **kwargs):
        current_url = request.get_full_path()
        splitted_url = re.split(r'(js|images|css|icons)', current_url)
        url = ''.join(splitted_url[1:])
        static_url = '/static/' + url
        return HttpResponseRedirect(static_url)


# error views
def error_400_view(request, exception=None):
    return render(request, "error_templates/400.html")


def error_403_view(request, exception=None):
    return render(request, "error_templates/403.html")


def error_404_view(request, exception=None):
    return render(request, "error_templates/404.html")


def error_500_view(request, exception=None):
    return render(request, "error_templates/500.html")
