from django.shortcuts import render
from django.views import generic
from django.conf import settings
from django.http.response import JsonResponse, Http404
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt

from .models import Item

import stripe


class ItemListView(generic.ListView):
    model = Item


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelledView(TemplateView):
    template_name = 'cancelled.html'


def index(request):
    num_items = Item.objects.all().count()

    return render(
        request,
        'index.html',
        context={'num_items': num_items},
    )


def item_detail_view(request, pk):
    try:
        current_item = Item.objects.get(pk=pk)
        price = str(current_item.price)
        item_price = f"{price[0:-2]}.{price[-2:]}"

    except Item.DoesNotExist:
        raise Http404("Book does not exist")

    return render(
        request,
        'catalog/item_detail.html',
        context={'item': current_item, 'item_price': item_price}
    )


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request, pk):
    current_item = Item.objects.get(pk=pk)
    if request.method == 'GET':
        domain_url = settings.DEV_SITE_URL
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': current_item.price,
                            'product_data': {
                                'name': current_item.name,
                                'description': current_item.description,
                            },
                        },
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})



