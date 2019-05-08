import logging

from models.model_base import ModelBase

logger = logging.getLogger(__name__)


class PaymentBtcModel(ModelBase):

    def __init__(self):
        super().__init__()
        self.payment_id = None  # type: None|int  # Unique
        self.satoshi = None  # type: None|int

    def validate(self):
        # satoshi
        if self.satoshi is None:
            return False
        elif self.satoshi > self.MAX_INTEGER:
            return False
        elif self.satoshi < 0:
            return False

        return True
