from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Avg, Count
from core.models import ProductionRecord, State, County
from .serializers import StateSerializer, ProductionRecordSerializer, CountySerializer,TotalProductionSerializer,ProductionByStateSerializer, ProductionByCountySerializer, ProductionByCommoditySerializer, ProductionByDispositionSerializer,YearlyProductionSerializer, TopCountiesSerializer, ProductionByLandClasSerializer, ProductionOverTimeStateSerializer, OffshoreOnshoreProductionSerializer

class TotalProduction(APIView):
    """
    Returns the total volume produced

    """
    def get(self, request):
        total = ProductionRecord.objects.aggregate(total_volume=Sum("volume"))["total_volume"]
        serializer = TotalProductionSerializer({"totalProduction": total})

        return Response(serializer.data)


class ProductionByState(APIView):
    """
    Returns total production by State

    """
    def get(self, request):
        data = (
            ProductionRecord.objects
            .values("state__name")
            .annotate(total_volume=Sum("volume"))
            .order_by("-total_volume")
        )
        serializer = ProductionByStateSerializer(data, many = True)
        return Response(serializer.data)

class ProductionByCounty(APIView):
    """
    Returns total prouction by County

    """
    def get(self, request):
        data = (
            ProductionRecord.objects
            .values("county__name", "state__name")
            .annotate(total_volume=Sum("volume"))
            .order_by("-total_volume")
        )
        serializer = ProductionByCountySerializer(data, many = True)
        return Response(serializer.data)

class ProductionByCommodity(APIView):
    """
    Returns total production by Commodity

    """
    def get(self, request):
        data = (
            ProductionRecord.objects
            .values("commodity__name")
            .annotate(total_volume=Sum("volume"))
            .order_by("-total_volume")
        )
        serializer = ProductionByCommoditySerializer(data, many = True)
        return Response(serializer.data)

class AverageProductionPerYear(APIView):
    """
    Returns average production by year

    """
    def get(self, request):
        data = (
            ProductionRecord.objects
            .extra({'year': "strftime('%%Y', productionDate)"})
            .values("year")
            .annotate(avgVol=Avg("volume"))
            .order_by("year")
        )
        serializer = YearlyProductionSerializer(data, many = True)
        return Response(serializer.data)

class ProductionByOffshore(APIView):
    """
    Returns total offshore production
    """
    def get(self, request):
        offshore_total = (ProductionRecord.objects
            .filter(offshoreRegion__isnull=False)
            .aggregate(total=Sum("volume"))["total"]
        )

        onshore_total = (ProductionRecord
            .objects.filter(county__isnull=False)
            .aggregate(total=Sum("volume"))["total"]
        )

        data = {"offshore": offshore_total, "onshore": onshore_total}
        serializer=  OffshoreOnshoreProductionSerializer(data = data)
        serializer.is_valid(raise_exception = True)

        return Response(serializer.validated_data)
class ProductionByDisposition(APIView):
    """
    Returns total production by disposition
    """
    def get(self, request):
        data = (
            ProductionRecord.objects
            .values("disposition__code", "disposition__description")
            .annotate(total_volume=Sum("volume"))
            .order_by("-total_volume")
        )
        serializer = ProductionByDispositionSerializer(data, many = True)
        return Response(serializer.data)

class TopCounties(APIView):
    """
    Returns the top counties in terms of production
    """
    def get(self, request):
        data = (
            ProductionRecord.objects
            .values("county__name", "state__name")
            .annotate(total_volume=Sum("volume"))
            .order_by("-total_volume")[:5]
        )
        serializer = TopCountiesSerializer(data, many = True)
        return Response(serializer.data)

class ProductionOverTimeState(APIView):
    """
    Returns total production over time per State
    """
    def get(self, request):


                data = (
                    ProductionRecord.objects
                    .exclude(state__name = None)
                    .extra({'year': "strftime('%%Y', productionDate)"})
                    .values("state__name","year")
                    .annotate(total_volume=Sum("volume"))
                    .order_by("state__name","year")
                    )
                serializer = ProductionOverTimeStateSerializer(data, many = True)
                return Response(serializer.data)

class ProductionByLandClass(APIView):
    """
    Returns total production by land class
    """
    def get(self, request):
        data = (
            ProductionRecord.objects
            .values("landClass__name")
            .annotate(total_volume=Sum("volume"))
            .order_by("-total_volume")
        )
        serializer = ProductionByLandClasSerializer(data, many = True)
        return Response(serializer.data)


class StateList(APIView):
    def get(self, request):
        states = State.objects.all()
        serializer = StateSerializer(states, many = True)
        return Response(serializer.data)

class ProductionRecordList(APIView):
    def get(self,request):
        record = ProductionRecord.objects.all()
        serializer = ProductionRecordSerializer(record, many = True)
        return Response(serializer.data)
class countyList(APIView):
    def get(self, request):
        county = County.objects.all()
        serializer = CountySerializer(county, many = True)
        return Response(serializer.data)

