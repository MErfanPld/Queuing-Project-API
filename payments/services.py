from payments.models import Wallet, Transaction, Payment
from django.db import transaction as db_transaction
from django.core.exceptions import ValidationError

def pay_with_wallet(user, appointment):
    amount = appointment.service.price

    wallet = Wallet.objects.get(user=user)
    if wallet.balance < amount:
        raise ValidationError("موجودی کیف پول کافی نیست.")

    with db_transaction.atomic():
        # کم کردن موجودی
        wallet.decrease(amount)

        # ثبت تراکنش
        Transaction.objects.create(
            wallet=wallet,
            amount=amount,
            type='WITHDRAW',
            status='SUCCESS',
            reservation=appointment
        )

        # ثبت پرداخت
        Payment.objects.create(
            user=user,
            amount=amount,
            method='WALLET',
            status='SUCCESS',
            reservation=appointment,
            description=f"پرداخت برای نوبت {appointment.id} از طریق کیف پول"
        )

        # تغییر وضعیت نوبت
        appointment.status = 'confirmed'
        appointment.save()
