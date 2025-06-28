from .models import Bread
from .utils import generate_slug

class BreadService:
    """
    Service class for interacting with Post objects
    """

    @staticmethod
    def get_all_bread():
        """
        Retrieve all bread from database
        """
        return Bread.objects.all()