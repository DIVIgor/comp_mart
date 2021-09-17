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
        product_id = product.id
        if product_id not in self.basket:
            self.basket[product_id] = {'price': float(product.price), 'qty': int(qty)}

        self.session.modified = True

    def __len__(self):
        """Get the basket data"""
        return sum(item['qty'] for item in self.basket.values())