from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic import CreateView
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from payments.forms import WalletForm, AddFundsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from reservations.models import Appointment, Service
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .models import Wallet, Transaction
from decimal import Decimal


class PaymentView(View):
    def get(self, request, *args, **kwargs):
        appointment_id = kwargs.get('appointment_id')
        appointment = get_object_or_404(Appointment, id=appointment_id)
        service = appointment.service

        context = {
            'appointment': appointment,
            'service': service,
            'price': service.price,
        }

        return render(request, 'payments/payment.html', context)

    def post(self, request, *args, **kwargs):
        appointment_id = request.POST.get('appointment_id')
        appointment = get_object_or_404(Appointment, id=appointment_id)
        service = appointment.service

        # ایجاد کیف پول یا دریافت کیف پول موجود
        wallet, created = Wallet.objects.get_or_create(user=appointment.user)

        # استفاده از Decimal برای جمع کردن موجودی
        amount = Decimal(service.price)
        Transaction.objects.create(wallet=wallet, amount=amount)
        wallet.balance = wallet.balance + amount
        wallet.save()

        # به روز رسانی وضعیت نهایی رزرو
        appointment.status = 'confirmed'
        appointment.save()

        # هدایت به صفحه تأیید پرداخت یا صفحه اصلی
        messages.success(
            request, 'رزرو شما در انتظار تایید هست. بعد از تایید ارایشگر به شما پیامک میشود')
        return redirect('home')


class ProcessPaymentView(View):
    def post(self, request, *args, **kwargs):
        appointment_id = request.POST.get('appointment_id')
        appointment = get_object_or_404(Appointment, id=appointment_id)
        service = appointment.service

        # افزودن مبلغ به کیف پول کاربر
        wallet, created = Wallet.objects.get_or_create(user=appointment.user)
        Transaction.objects.create(wallet=wallet, amount=service.price)
        wallet.balance += service.price
        wallet.save()

        # به روز رسانی وضعیت نهایی رزرو
        appointment.status = 'confirmed'
        appointment.save()

        # هدایت به صفحه تأیید پرداخت یا صفحه اصلی
        return redirect('home')


class CreateWalletView(LoginRequiredMixin, CreateView):
    model = Wallet
    form_class = WalletForm
    template_name = 'payments/create_wallet.html'
    success_url = reverse_lazy('create_wallet')

    def form_valid(self, form):
        if Wallet.objects.filter(user=self.request.user).exists():
            messages.error(self.request, "شما قبلاً کیف پول دارید.")
            return redirect('create_wallet')
        form.instance.user = self.request.user
        wallet = form.save()
        wallet.save()
        messages.success(self.request, "کیف پول شما با موفقیت شارژ شد.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wallet'] = Wallet.objects.get(user=self.request.user)
        return context


class AddFundsView(LoginRequiredMixin, FormView):
    form_class = AddFundsForm
    template_name = 'payments/add_funds.html'
    success_url = reverse_lazy('wallet_success')

    def form_valid(self, form):
        # دریافت کیف پول کاربر یا ایجاد یکی جدید
        wallet, created = Wallet.objects.get_or_create(user=self.request.user)

        # افزودن موجودی جدید
        amount = form.cleaned_data['amount']
        if amount > 0:
            wallet.add_funds(amount)
            # messages.success(self.request, f"موجودی کیف پول با موفقیت به {
            #                  amount} افزایش یافت.")
            print("...")
        else:
            messages.error(self.request, "مقدار باید بزرگتر از صفر باشد.")
            return self.form_invalid(form)

        return super().form_valid(form)


class SomeErrorPageView(TemplateView):
    template_name = 'payments/some_error_page.html'


class WalletSuccess(TemplateView):
    template_name = 'payments/success.html'
