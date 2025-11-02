import graphene
from graphene_django.types import DjangoObjectType
from crm.models import Product 

#productType for returning product data
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

#update low stock products
class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass

    success = graphene.String()
    updated_products = graphene.List(ProductType)

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []

        for product in low_stock_products:
            product.stock += 10  # restock by 10
            product.save()
            updated_products.append(product)

        message = f"{len(updated_products)} products updated successfully."
        return UpdateLowStockProducts(success=message, updated_products=updated_products)


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")


class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
