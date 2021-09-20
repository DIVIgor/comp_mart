from store.models import Product
from decimal import Decimal


class Basket():
    """A base basket class"""
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        # Check if the user has a session
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, qty):
        """Adding and updating the users basket session data"""
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'price': str(product.price), 'qty': int(qty)}

            self.save_session()

    def delete(self, product):
        """Deleting the item from the basket session data"""
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save_session()

    def save_session(self):
        self.session.modified = True

    def __len__(self):
        """Get the basket data"""
        return sum(item['qty'] for item in self.basket.values())

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) * Decimal(item['qty']) for item in self.basket.values())