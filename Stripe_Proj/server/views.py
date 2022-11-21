import stripe
from django.shortcuts import redirect, get_object_or_404
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Item
from .serializers import ItemSerializer

stripe.api_key = 'sk_test_51M57GXG3FJqZ776UlTU5eqkzefU9k7yo3o9zdRUuIz7orllQEWxP78ZVvvhBjrkEZUqjCyNKy6iXwUp59etaiafA00ojLUuDZ6'


class ItemAPIView(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name', None)
        if name:
            return Item.objects.filter(name__contains=name)
        return Item.objects.all()


class ItemRend(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request, ):
        item = Item.objects.filter()
        return Response({'items': item})


class Success(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'success.html'

    def get(self, request, ):
        item = Item.objects.filter()
        return Response({'items': item})


class Cancel(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cancel.html'

    def get(self, request, ):
        item = Item.objects.filter()
        return Response({'items': item})


class ItemBuy(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'pay.html'

    def get(self, request, item_id):
        item_buy_id = get_object_or_404(Item, id=item_id)
        item = get_object_or_404(Item, id=item_id)
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': item.price,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/success',
            cancel_url='http://localhost:8000/cancel',
        )
        return Response({'items': item_buy_id, 'session_id': session.id})

    @action(methods=['POST'], detail=True)
    def create_checkout_session(self, item_id):
        item = get_object_or_404(Item, id=item_id)
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': item.price,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/success',
            cancel_url='http://localhost:8000/cancel',
        )
        return redirect(session.url, code=303)
