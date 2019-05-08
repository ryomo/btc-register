import logging

from models.model_base import ModelBase

logger = logging.getLogger(__name__)


class PaymentFiatModel(ModelBase):

    def __init__(self):
        super().__init__()
        self.payment_id = None  # type: None|int  # Unique
        self.paid = None  # type: None|int
        self.change = None  # type: None|int

    def validate(self):
        # paid
        if self.paid is None:
            return False
        elif self.paid > self.MAX_INTEGER:
            return False
        elif self.paid < 0:
            return False

        # change
        if self.change is None:
            return False
        elif self.change > self.MAX_INTEGER:
            return False
        elif self.change < 0:
            return False

        return True
