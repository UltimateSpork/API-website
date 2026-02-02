from rest_framework import serializers
from core.models import State, County
from core.models import ProductionRecord

class StateSerializer(serializers.ModelSerializer):

    class Meta:

        model = State
        fields = ["id", "name"]

class CountySerializer(serializers.ModelSerializer):

    state = StateSerializer()
    class Meta:
        model = County
        fields = ["name","FIPScode","state"]

class ProductionRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductionRecord
        fields = ["id","productionDate","volume","landClass","landCategory","state","county","offshoreRegion","commodity","disposition"]


class TotalProductionSerializer(serializers.Serializer):

    totalProduction = serializers.FloatField()

class ProductionByStateSerializer(serializers.Serializer):

    stateName = serializers.CharField(source="state__name")
    total_volume = serializers.FloatField()

class ProductionByCountySerializer(serializers.Serializer):
    countyName = serializers.CharField(source = "county__name")
    stateName = serializers.CharField(source = "state__name")
    total_volume = serializers.FloatField()

class ProductionByCommoditySerializer(serializers.Serializer):

    commodityName = serializers.CharField(source = "commodity__name")
    total_volume = serializers.FloatField()

class ProductionByDispositionSerializer(serializers.Serializer):

    dispositionCode = serializers.CharField(source = "disposition__code")
    dispositionDesc = serializers.CharField(source = "disposition__description")
    total_volume = serializers.FloatField()

class YearlyProductionSerializer(serializers.Serializer):

    year = serializers.CharField()
    avgVol = serializers.FloatField()

class OffOnShoreSerializer(serializers.Serializer):

    offshore = serializers.FloatField()
    onshore = serializers.FloatField()

    def validate_offshore(self, value):

        if value < 0:

            raise serializers.ValidationError("Production cannot be negative")
        return value
    def validate_onshore(self, value):

        if value > 0:

            raise serializers.ValidationError("Production cannot be negative")
        return value


class TopCountiesSerializer(serializers.Serializer):
    countyName = serializers.CharField(source = "county__name")
    stateName = serializers.CharField(source = "state__name")
    total_volume = serializers.FloatField()


class ProductionByLandClasSerializer(serializers.Serializer):
    landClassName = serializers.CharField(source = "landClass__name")
    total_volume = serializers.FloatField()


class ProductionOverTimeStateSerializer(serializers.Serializer):

    stateName = serializers.CharField(source = "state__name")
    year = serializers.CharField()
    total_volume = serializers.FloatField()


class OffshoreOnshoreProductionSerializer(serializers.Serializer):
    offshore = serializers.FloatField()
    onshore = serializers.FloatField()

