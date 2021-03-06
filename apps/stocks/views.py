from django.contrib.auth.mixins import LoginRequiredMixin
from apps.core.mixins import CustomGetFormUserMixin, AjaxResponseMixin, TabContextMixin, \
    GetFormWithDepotAndInitialDataMixin, CustomAjaxDeleteMixin, GetFormWithDepotMixin
from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from .models import Depot, Stock, Bank, Flow, Trade, Price, Dividend, PriceFetcher
from .mixins import GetDepotMixin
from .forms import DepotForm, DepotActiveForm, DepotSelectForm, BankForm, BankSelectForm, StockSelectForm, StockForm, \
    FlowForm, TradeForm, EditStockForm, DividendForm, PriceFetcherForm, PriceEditForm
import json


###
# Depot: Detail, Create, Edit, Delete, SetActive
###
class IndexView(LoginRequiredMixin, TabContextMixin, generic.DetailView):
    template_name = 'stocks/index.j2'
    model = Depot

    def get_queryset(self):
        return self.request.user.stock_depots.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = self.object.get_stats()
        context['banks'] = self.object.banks.order_by('-value')
        context['stocks'] = self.object.stocks.order_by('-value')
        context['values'] = self.object.get_values()
        context['flows'] = self.object.get_flows()
        return context


class CreateDepotView(LoginRequiredMixin, CustomGetFormUserMixin, AjaxResponseMixin, generic.CreateView):
    template_name = 'symbols/form_snippet.njk'
    model = Depot
    form_class = DepotForm


class EditDepotView(LoginRequiredMixin, CustomGetFormUserMixin, AjaxResponseMixin, generic.UpdateView):
    model = Depot
    form_class = DepotForm
    template_name = "symbols/form_snippet.njk"


class DeleteDepotView(LoginRequiredMixin, CustomGetFormUserMixin, AjaxResponseMixin, generic.FormView):
    model = Depot
    template_name = "symbols/form_snippet.njk"
    form_class = DepotSelectForm

    def form_valid(self, form):
        depot = form.cleaned_data["depot"]
        user = depot.user
        depot.delete()
        if user.stock_depots.count() <= 0:
            user.save()
        return HttpResponse(json.dumps({"valid": True}), content_type="application/json")


class SetActiveDepotView(LoginRequiredMixin, generic.View):
    http_method_names = ['get', 'head', 'options']

    def get(self, request, pk, *args, **kwargs):
        self.request.user.stock_depots.update(is_active=False)
        depot = get_object_or_404(self.request.user.stock_depots.all(), pk=pk)
        form = DepotActiveForm(data={'is_active': True}, instance=depot)
        if form.is_valid():
            depot = form.save()
        url = '{}?tab=stocks'.format(reverse_lazy('users:settings', args=[self.request.user.pk]))
        return HttpResponseRedirect(url)


###
# Stock: Detail, Add, Edit, Delete
###
class StockView(LoginRequiredMixin, TabContextMixin, generic.DetailView):
    template_name = 'stocks/stock.j2'
    model = Stock

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trades'] = self.object.trades.all().select_related('bank', 'stock')
        context['stats'] = self.object.get_stats()
        context['prices'] = Price.objects.filter(ticker=self.object.ticker, exchange=self.object.exchange)
        context['dividends'] = self.object.dividends.all()
        context['values'] = self.object.get_values()
        context['flows'] = self.object.get_flows()
        context['price_fetcher'] = self.object.price_fetcher if hasattr(self.object, 'price_fetcher') else None
        return context


class AddStockView(LoginRequiredMixin, GetDepotMixin, GetFormWithDepotMixin, AjaxResponseMixin, generic.CreateView):
    form_class = StockForm
    model = Stock
    template_name = "symbols/form_snippet.njk"


class EditStockView(GetDepotMixin, GetFormWithDepotMixin, AjaxResponseMixin, generic.UpdateView):
    model = Stock
    form_class = EditStockForm
    template_name = "symbols/form_snippet.njk"

    def get_queryset(self):
        return Stock.objects.filter(depot__in=self.request.user.stock_depots.all())


class DeleteStockView(LoginRequiredMixin, GetDepotMixin, GetFormWithDepotMixin, AjaxResponseMixin, generic.FormView):
    model = Stock
    template_name = "symbols/form_snippet.njk"
    form_class = StockSelectForm

    def form_valid(self, form):
        stock = form.cleaned_data["stock"]
        stock.delete()
        return HttpResponse(json.dumps({"valid": True}), content_type="application/json")


###
# Price: Edit
###
class EditPriceView(LoginRequiredMixin, AjaxResponseMixin, generic.UpdateView):
    model = Price
    form_class = PriceEditForm
    template_name = 'symbols/form_snippet.njk'


###
# StockPriceFetcher: Add, Edit, Delete
###
class AddPriceFetcherView(LoginRequiredMixin, GetDepotMixin, GetFormWithDepotAndInitialDataMixin,
                          AjaxResponseMixin, generic.CreateView):
    form_class = PriceFetcherForm
    model = PriceFetcher
    template_name = "symbols/form_snippet.njk"


class EditPriceFetcherView(LoginRequiredMixin, GetDepotMixin, GetFormWithDepotMixin, AjaxResponseMixin, generic.UpdateView):
    model = PriceFetcher
    form_class = PriceFetcherForm
    template_name = "symbols/form_snippet.njk"


class DeletePriceFetcherView(LoginRequiredMixin, CustomAjaxDeleteMixin, generic.DeleteView):
    model = PriceFetcher
    template_name = "symbols/delete_snippet.njk"

    def get_queryset(self):
        return PriceFetcher.objects.filter(
            stock__in=Stock.objects.filter(
                depot__pk=self.request.user.get_active_stocks_depot_pk()))


###
# Bank: Detail, Add, Edit, Delete
###
class BankView(LoginRequiredMixin, TabContextMixin, generic.DetailView):
    template_name = 'stocks/bank.j2'
    model = Bank

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flows'] = Flow.objects.filter(bank=self.object)
        context['stats'] = self.object.get_stats()
        context['trades'] = Trade.objects.filter(bank=self.object)
        context['dividends'] = self.object.dividends.all()
        return context


class AddBankView(LoginRequiredMixin, GetDepotMixin, GetFormWithDepotMixin, AjaxResponseMixin, generic.CreateView):
    form_class = BankForm
    model = Bank
    template_name = "symbols/form_snippet.njk"


class EditBankView(GetDepotMixin, GetFormWithDepotMixin, AjaxResponseMixin, generic.UpdateView):
    model = Bank
    form_class = BankForm
    template_name = "symbols/form_snippet.njk"

    def get_queryset(self):
        return Bank.objects.filter(depot__in=self.request.user.stock_depots.all())


class DeleteBankView(LoginRequiredMixin, GetDepotMixin, GetFormWithDepotMixin, AjaxResponseMixin, generic.FormView):
    model = Bank
    template_name = "symbols/form_snippet.njk"
    form_class = BankSelectForm

    def form_valid(self, form):
        bank = form.cleaned_data["bank"]
        bank.delete()
        return HttpResponse(json.dumps({"valid": True}), content_type="application/json")


###
# Flow: Add, Edit, Delete
###
class AddFlowView(LoginRequiredMixin, GetDepotMixin, GetFormWithDepotAndInitialDataMixin, AjaxResponseMixin,
                  generic.CreateView):
    model = Flow
    form_class = FlowForm
    template_name = "symbols/form_snippet.njk"


class EditFlowView(LoginRequiredMixin, GetDepotMixin, GetFormWithDepotMixin, AjaxResponseMixin, generic.UpdateView):
    model = Flow
    form_class = FlowForm
    template_name = "symbols/form_snippet.njk"


class DeleteFlowView(LoginRequiredMixin, CustomAjaxDeleteMixin, generic.DeleteView):
    model = Flow
    template_name = "symbols/delete_snippet.njk"

    def get_queryset(self):
        return Flow.objects.filter(
            bank__in=Bank.objects.filter(
                depot__pk=self.request.user.get_active_stocks_depot_pk()))


###
# Dividend: Add, Edit, Delete
###
class AddDividendView(LoginRequiredMixin, GetDepotMixin, GetFormWithDepotAndInitialDataMixin, AjaxResponseMixin,
                      generic.CreateView):
    model = Dividend
    form_class = DividendForm
    template_name = "symbols/form_snippet.njk"


class EditDividendView(LoginRequiredMixin, GetDepotMixin, GetFormWithDepotMixin, AjaxResponseMixin, generic.UpdateView):
    model = Dividend
    form_class = DividendForm
    template_name = "symbols/form_snippet.njk"


class DeleteDividendView(LoginRequiredMixin, CustomAjaxDeleteMixin, generic.DeleteView):
    model = Dividend
    template_name = "symbols/delete_snippet.njk"

    def get_queryset(self):
        return Dividend.objects.filter(
            bank__in=Bank.objects.filter(
                depot__pk=self.request.user.get_active_stocks_depot_pk()))


###
# Trade: Add, Edit, Delete
###
class AddTradeView(LoginRequiredMixin, GetDepotMixin, GetFormWithDepotAndInitialDataMixin, AjaxResponseMixin,
                   generic.CreateView):
    model = Trade
    form_class = TradeForm
    template_name = "symbols/form_snippet.njk"


class EditTradeView(LoginRequiredMixin, GetDepotMixin, GetFormWithDepotMixin, AjaxResponseMixin, generic.UpdateView):
    model = Trade
    form_class = TradeForm
    template_name = "symbols/form_snippet.njk"


class DeleteTradeView(LoginRequiredMixin, CustomAjaxDeleteMixin, generic.DeleteView):
    model = Trade
    template_name = "symbols/delete_snippet.njk"

    def get_queryset(self):
        return Trade.objects.filter(
            bank__in=Bank.objects.filter(
                depot__pk=self.request.user.get_active_stocks_depot_pk()))
