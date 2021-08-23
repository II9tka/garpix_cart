from logging import getLogger

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _

from .abstracts import AbstractCartHandler, AbstractCartSession
from .exceptions import CartError
from .utils import make_session_format

CART_SESSION_KEY = settings.CART_SESSION_KEY

logger = getLogger(__name__)


class BaseCartHandler(AbstractCartHandler):
    def __init__(self, core):
        self._core = core

    def validate(self, products):
        if isinstance(products, list):
            return products
        raise CartError(
            _('"products" must be list.')
        )

    def is_valid(self, products) -> bool:
        try:
            self.validate(products)
        except CartError:
            return False
        return True

    def error_log(self, products):
        try:
            self.validate(products)
        except CartError as error:
            logger.debug(
                str(error)
            )
            return str(error)
        return None


class BaseCartAdd(BaseCartHandler):
    def make(self, products):
        cart = self._core.get()
        formatted_products = make_session_format(products)
        updates = [num for num, items in enumerate(formatted_products.items()) if items[0] in cart]

        for num, product in enumerate(products):
            if num not in updates:
                product['created_at'] = timezone.now().strftime("%m.%d.%Y, %H:%M:%S")
            else:
                del products[num]
                product = cart.get(product['product'])

            product['updated_at'] = timezone.now().strftime("%m.%d.%Y, %H:%M:%S")

        cart.update(make_session_format(products))
        self._core.modify_session(cart)

        return True


class BaseCartRemove(BaseCartHandler):
    def validate(self, products):
        cart = self._core.get()
        formatted_products = make_session_format(products)

        for key, _ in formatted_products.items():
            if key not in cart:
                raise CartError(f'Key {key} does not exist')
        return super().validate(products)

    def make(self, products):
        cart = self._core.get()

        products = make_session_format(products)

        for key, _ in products.items():
            del cart[key]

        self._core.modify_session(cart)

        return True


class BaseCartSession(AbstractCartSession):
    def __init__(self, session):
        self.__session = session
        self.add = BaseCartAdd(self)
        self.remove = BaseCartRemove(self)

    def get(self):
        return self.__session.get(CART_SESSION_KEY, {})

    def list(self):
        return [self.get()]

    def modify_session(self, values):
        self.__session[CART_SESSION_KEY] = values

        return True
