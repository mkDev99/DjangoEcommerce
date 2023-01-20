from store.models import Product
from decimal import Decimal
import json

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)

class Basket():
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, qty):
        product_id = str(product.id)
        
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}

        self.save()

    def __iter__(self):
        """
            Collect the product_id in the session data to query the database 
            and return products
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.basket.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
    
    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def update(self, product, qty):
        """
        Update values in session data
        """
        product_id = str(product)
        qty = qty


        if product_id in self.basket:
            item = self.basket[product_id]
            item['qty'] = qty
        
        self.save()

    def get_total_item_price(self):
        total_jtem = 0
        for item in self.basket.values():
            for jtem in self.basket.values():
                if item != jtem:
                    total_jtem = sum(Decimal(jtem['price']) * jtem['qty'])
                    
                    
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values()) - total_jtem

        
    def save(self):
        self.session.modified = True