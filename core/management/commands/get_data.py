import kaggle
from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
import os
from core.models import *
import csv
from datetime import datetime


dataset = "pinuto/us-oil-and-gas-production-and-disposition-20152025" 


states_cache = {}
counties_cache = {}
land_classes_cache = {}
commodities_cache = {}
offshore_regions_cache = {}
land_categories_cache = {}


class Command(BaseCommand):
    help = 'Gets data from dataset'
    def handle(self, *args, **options):

        kaggle.api.authenticate() 

        outputDir = "./core/media/kaggle"

        os.makedirs(outputDir, exist_ok = True)

        kaggle.api.dataset_download_files(dataset, path=outputDir,unzip=True)

        self.stdout.write("Dataset downloaded successfully\n")

        with open("./core/media/kaggle/OGORBcsv.csv") as file:

            reader = csv.DictReader(file)
            for row in reader:
                
                # Get Date
                productionDate = datetime.strptime(row["Production Date"], "%m/%d/%Y").date()

                # Get Land Class 
                landClass, _ = LandClass.objects.get_or_create(name=row["Land Class"].strip())

                landCategory, _ = LandCategory.objects.get_or_create(name=row["Land Category"].strip())
                # State
                state = None
                stateName = row["State"].strip()

                if (stateName and stateName not in states_cache):
                        if (stateName is not None):
                            state, _ = State.objects.get_or_create(name=row["State"].strip())
                            states_cache = state

                        else:
                            state, _ = "Offshore"
                else:
                    state = states_cache[stateName]

                # County 

                county = None
                countyName = row["County"].strip()

                if (countyName and countyName not in counties_cache):
                    county, _ = County.objects.get_or_create(name=row["County"].strip(), state=state, FIPScode = row["FIPS Code"].strip())
                    counties_cache = county




                # Offshore REgion

                if (row["Offshore Region"].strip()):
                    offshoreRegion, _ = OffshoreRegion.objects.get_or_create(name=row["Offshore Region"].strip())
                # Commodity

                commodityRaw = row["Commodity"].strip()

                commodityName, commodityUnit = commodityRaw.split("(",1)
                commodityUnit = commodityUnit.replace(")","").strip()

                commodity, _ = Commodity.objects.get_or_create(name=commodityName.strip(), unit=commodityUnit.strip())



                # Disposition 


                disposition = Disposition.objects.create(code=int(row["Disposition Code"]),description = row["Disposition Description"].strip(),)



                # Volume 

                volumeString = row["Volume"].replace(",", "").strip()
                volume = float(volumeString) if volumeString else 0


                ProductionRecord.objects.create(
                    productionDate=productionDate,
                    volume=volume,
                    landClass=landClass,
                    landCategory=landCategory,
                    state=state,
                    county=county,
                    offshoreRegion=offshoreRegion,
                    commodity=commodity,
                    disposition=disposition,
                )

            
                




