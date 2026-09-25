import razorpay

from django.conf import settings


def get_razorpay_client():

    return razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET,
        )
    )


def create_razorpay_order(
    amount,
    receipt
):

    client = get_razorpay_client()

    amount_in_paise = int(
        amount * 100
    )

    order_data = {
        "amount": amount_in_paise,
        "currency": "INR",
        "receipt": receipt,
    }

    return client.order.create(
        data=order_data
    )