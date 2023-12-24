from schema.pharmacy import pharmacyEntity, pharmaciesEntity
from geopy import distance
from fastapi import APIRouter, HTTPException
from config.database import collection_name
from fastapi import APIRouter, HTTPException
from models.mpharmacy import Pharmacy
from models.mpharmacist import Pharmacist
from models.mdrugs import Drug
from config.database import collection_name
from schema.pharmacy import pharmacyEntity, pharmaciesEntity
from bson import ObjectId
from models.mlocation import Location
from typing import List, Optional , Union
import re


def get_all_service(pharmacies):

    """
    Return all pharmacies in the database
    """
    print(pharmaciesEntity(pharmacies))
    return pharmaciesEntity(pharmacies)




# async def search_for_drug_service(drug_name, user_lat, user_lon):
#     """
#     Takes three arguments : drug name , user lat and long , then it returns the top 5 pharmacies
#     based on the distance method of the geopy
#     """
#     pharmacies = await collection_name.find({"drugs.name": drug_name}).to_list(1000)
#     if not pharmacies:
#         raise HTTPException(status_code=404, detail="No pharmacies found with the specified drug")

#     # Calculate distance from user location to each pharmacy and sort
#     for pharmacy in pharmacies:
#         pharmacy_location = (pharmacy["location"]["latitude"], pharmacy["location"]["longitude"])
#         user_loc = (user_lat, user_lon)
#         pharmacy["distance"] = distance.distance(pharmacy_location, user_loc).km

#     # Sort pharmacies by distance
#     sorted_pharmacies = sorted(pharmacies, key=lambda x: x["distance"])[:5]

#     return pharmaciesEntity(sorted_pharmacies)




# # Function to search for multiple drugs
# async def search_for_drugs_service(drug_names: List[str], drug_barcode,user_lat: float, user_lon: float):
#     """
#     Takes a list of drug names along with user's latitude and longitude,
#     then returns the top 5 pharmacies based on the distance.
#     """
#     flag = False

#     if drug_names 

#     if not drug_names:
#         raise HTTPException(status_code=400, detail="No drug names provided")

#     # Find pharmacies that have any of the specified drugs
#     query = {"drugs.drugName": {"$in": [re.compile(r'^{}$'.format(drug_name), re.IGNORECASE) for drug_name in drug_names]}}
#     # query = {"drugs.drugName": {"$in": drug_names}}
#     pharmacies = await collection_name.find(query).to_list(1000)

    
#     if not pharmacies:
#         raise HTTPException(status_code=404, detail="No pharmacies found with the specified drugs")

    
#     for pharmacy in pharmacies:
#         pharmacy_location = (pharmacy["location"]["latitude"], pharmacy["location"]["longitude"])
#         user_loc = (user_lat, user_lon)
#         pharmacy["distance"] = distance.distance(pharmacy_location, user_loc).km

#     sorted_pharmacies = sorted(pharmacies, key=lambda x: x["distance"])[:5]

#     return pharmaciesEntity(sorted_pharmacies)



async def search_for_drugs_service(drug_names: Union[List[str], None], drug_barcode: Union[str, None], user_lat: float, user_lon: float):
    """
    Takes a list of drug names or a drug barcode along with user's latitude and longitude,
    then returns the top 5 pharmacies based on the distance.
    """
    if not drug_names and not drug_barcode:
        raise HTTPException(status_code=400, detail="No drug names or barcode provided")

    
    query = {}

    
    if drug_names:
        query["drugs.drugName"] = {"$in": [re.compile(r'^{}$'.format(drug_name), re.IGNORECASE) for drug_name in drug_names]}
    elif drug_barcode:
        print("barcode is provided")
        query["drugs.drugBarcode"] = re.compile(r'^{}$'.format(drug_barcode), re.IGNORECASE)

    pharmacies = await collection_name.find(query).to_list(1000)

    if not pharmacies:
        raise HTTPException(status_code=404, detail="No pharmacies found with the specified drugs or barcode")

    for pharmacy in pharmacies:
        pharmacy_location = (pharmacy["location"]["latitude"], pharmacy["location"]["longitude"])
        user_loc = (user_lat, user_lon)
        pharmacy["distance"] = distance.distance(pharmacy_location, user_loc).km

    sorted_pharmacies = sorted(pharmacies, key=lambda x: x["distance"])[:5]

    return pharmaciesEntity(sorted_pharmacies)


async def search_for_nearest_pharmacies_service(user_lat: float, user_lon: float):
    """
    Takes user's latitude and longitude and returns the top 5 nearest pharmacies based on the distance.
    """
    pharmacies = await collection_name.find().to_list(1000)

    if not pharmacies:
        raise HTTPException(status_code=404, detail="No pharmacies found")

    for pharmacy in pharmacies:
        pharmacy_location = (pharmacy["location"]["latitude"], pharmacy["location"]["longitude"])
        user_loc = (user_lat, user_lon)
        pharmacy["distance"] = distance.distance(pharmacy_location, user_loc).km

    sorted_pharmacies = sorted(pharmacies, key=lambda x: x["distance"])[:5]

    return pharmaciesEntity(sorted_pharmacies)


async def add_drug_service(pharmacy_name, drug):
      # Fetch the pharmacy document by its name
    pharmacy = await collection_name.find_one({"name": pharmacy_name})
    if not pharmacy:
        raise HTTPException(status_code=404, detail="Pharmacy not found")

    # Append the new drug
    if "drugs" not in pharmacy:
        pharmacy["drugs"] = [drug.dict()]
    else:
        pharmacy["drugs"].append(drug.dict())

    # Update the pharmacy document
    await collection_name.update_one(
        {"name": pharmacy_name},
        {"$set": {"drugs": pharmacy["drugs"]}}
    )

    return {"message": "Drug added successfully"}



async def add_pharmacy_service(pharmacy):
    pharmacy_dict = pharmacy.dict()
    pharmacy_id = await collection_name.insert_one(pharmacy_dict)
    return {"id": str(pharmacy_id.inserted_id)}