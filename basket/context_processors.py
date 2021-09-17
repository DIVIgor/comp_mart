from .basket import Basket


def basket(request):
    # Data that is returning here - the default Basket data
    return {'basket': Basket(request)}