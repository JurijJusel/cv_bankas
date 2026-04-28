# Constants for CV Bankas scraper
BASE_URL = "https://www.cvbankas.lt/?page="

PYTHON_URL = "https://www.cvbankas.lt/?keyw=python&page="


# JSON file path to store scraped job posts
CV_BANKAS_JSON_FILE_PATH = "data/cv_bankas_posts.json"


# List of job categories to scrape with their corresponding category IDs
categories = {
    "Administration_work_safety": 202,
    "Environmental_sustainability": 1161,
    "Security_protection": 945,
    "Design_architecture": 402,
    "Insurance": 72,
    "Export": 488,
    "Energy_electronics": 1043,
    "Finance_accounting_banking": 390,
    "Manufacturing_production": 390,
    "Information_technology": 76,
    "Engineering_mechanics": 203,
    "Customer_service_services": 489,
    "Food_production": 94,
    "Medicine_pharmacy": 408,
    "Real_estate": 946,
    "Sales_management": 396,
    "Human_resources_management": 207,
    "Purchasing_supply": 207,
    "Consulting_advisory": 71,
    "Marketing_advertising": 205,
    "Warehousing": 492,
    "Construction": 87,
    "Education_training_culture": 1045,
    "Law": 88,
    "Transport_driving": 1047,
    "Transport_logistics_management": 1049,
    "Leadership_quality_management": 204,
    "Government_public_administration": 92,
    "Agriculture": 931,
    "Media_communication": 398,
}
