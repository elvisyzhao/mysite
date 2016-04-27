import logging
from django.contrib.auth.backends import ModelBackend

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)
logger.setLevel(logging.INFO)

class MyBackend(ModelBackend):
    def has_perm(self, user_obj, perm, obj=None):
        if obj == None:
            logger.error('obj is None')
            return super(MyBackend, self).has_perm(user_obj, perm)
        else:
            result = super(MyBackend, self).has_perm(user_obj, perm)
            logger.error('obj is not None')
            if result:
                return True
            else:
                return False
