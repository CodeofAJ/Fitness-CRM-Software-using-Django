from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from members.models import Member
from memberships.models import Membership

from .models import Payment
from .services.razorpay_service import create_razorpay_order



@login_required
def payment_list(request):

    search = request.GET.get(
        "search",
        ""
    ).strip()

    status = request.GET.get(
        "status",
        ""
    ).strip()

    payment_method = request.GET.get(
        "payment_method",
        ""
    ).strip()

    payments = (
        Payment.objects
        .select_related(
            "member",
            "membership",
            "membership__plan",
        )
        .all()
    )

    if search:
        payments = payments.filter(
            Q(member__member_id__icontains=search)
            | Q(member__full_name__icontains=search)
            | Q(member__phone__icontains=search)
            | Q(razorpay_order_id__icontains=search)
            | Q(razorpay_payment_id__icontains=search)
        )

    if status:
        payments = payments.filter(
            status=status
        )

    if payment_method:
        payments = payments.filter(
            payment_method=payment_method
        )

    context = {
        "payments": payments,
        "search": search,
        "status": status,
        "payment_method": payment_method,
    }

    return render(
        request,
        "payments/payment_list.html",
        context
    )


@login_required
def payment_detail(request, pk):

    payment = get_object_or_404(
        Payment.objects.select_related(
            "member",
            "membership",
            "membership__plan",
        ),
        pk=pk
    )

    return render(
        request,
        "payments/payment_detail.html",
        {
            "payment": payment,
        }
    )


@login_required
def member_payment_history(request, member_id):

    member = get_object_or_404(
        Member,
        member_id=member_id
    )

    payments = (
        Payment.objects
        .select_related(
            "membership",
            "membership__plan",
        )
        .filter(member=member)
        .order_by("-created_at")
    )

    return render(
        request,
        "payments/member_payment_history.html",
        {
            "member": member,
            "payments": payments,
        }
    )



@login_required
def razorpay_payment(request, pk):

    membership = get_object_or_404(
        Membership.objects.select_related(
            "member",
            "plan",
        ),
        pk=pk
    )

    # Prevent payment for an inactive member
    if membership.member.status != "ACTIVE":
        return redirect("memberships:membership_detail", pk=membership.pk)

    # Create our local Payment record first
    payment = Payment.objects.create(
        member=membership.member,
        membership=membership,
        amount=membership.plan.price,
        payment_method="RAZORPAY",
        status="PENDING",
    )

    # Create Razorpay order
    razorpay_order = create_razorpay_order(
        amount=payment.amount,
        receipt=f"gms_payment_{payment.id}",
    )

    # Save Razorpay order ID
    payment.razorpay_order_id = razorpay_order["id"]
    payment.save(
        update_fields=["razorpay_order_id"]
    )

    context = {
        "payment": payment,
        "membership": membership,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "razorpay_order_id": razorpay_order["id"],
    }

    return render(
        request,
        "payments/razorpay_checkout.html",
        context
    )