from django.urls import path
from .views import (
    TotalProduction, ProductionByState, ProductionByCounty, ProductionByCommodity,
    AverageProductionPerYear, ProductionByOffshore, ProductionByDisposition,
    TopCounties, ProductionOverTimeState, ProductionByLandClass, StateList, ProductionRecordList, countyList
    
)

urlpatterns = [
    path("production/total/", TotalProduction.as_view()),
    path("production/by-state/", ProductionByState.as_view()),
    path("production/by-county/", ProductionByCounty.as_view()),
    path("production/by-commodity/", ProductionByCommodity.as_view()),
    path("production/average-year/", AverageProductionPerYear.as_view()),
    path("production/offshore-onshore/", ProductionByOffshore.as_view()),
    path("production/by-disposition/", ProductionByDisposition.as_view()),
    path("production/top-counties/", TopCounties.as_view()),
    path("production/over-time/", ProductionOverTimeState.as_view()),
    path("production/by-landclass/", ProductionByLandClass.as_view()),
    path("states/",StateList.as_view(), name = 'state-list'),
    path("productionrecord/",ProductionRecordList.as_view(),name = 'Record List'),
    path("county/",countyList.as_view(),name = 'County List'),
]

