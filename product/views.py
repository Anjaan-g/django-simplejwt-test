from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer
from rest_framework.viewsets import ModelViewSet
# Create your views here.

class ProductViewSet(ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print("**************************************************************************")
        print(self.request.user)
        print("**************************************************************************")
        return self.queryset.filter(user=self.request.user)