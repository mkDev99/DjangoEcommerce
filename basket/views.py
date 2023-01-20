from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import Product
from django.http import JsonResponse
from .basket import Basket

def basket_summary(request):
    basket = Basket(request)
    return render(request, 'basket/summary.html')

def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response

def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)
        baskettotal = basket.get_total_price()
        basketqty = basket.__len__()

        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response
    
def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)
        

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        itemtotal = basket.get_total_item_price()

        print(baskettotal)
        print(itemtotal)
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal, 'totalitemprice': itemtotal})
        return response