CANDIDATE_METROS = [
    "San Diego, CA",
    "Los Angeles, CA",
    "Inland Empire, CA",
    "Phoenix, AZ",
    "Tucson, AZ",
    "El Paso, TX",
    "Laredo, TX",
    "McAllen, TX",
    "Brownsville, TX",
    "San Antonio, TX",
    "Austin, TX",
    "Dallas-Fort Worth, TX",
    "Houston, TX",
    "Monterrey, MX",      
]

# Assumed existing hubs / PoPs (proxy)
FLO_HUBS = [
    "Phoenix, AZ",
    "Dallas-Fort Worth, TX",
    "San Diego, CA",
]

# Base scenario weights
BASE_WEIGHTS = {
    "demand": 0.30,
    "enterprise_fit": 0.20,
    "cloud_adjacency": 0.20,
    "resilience": 0.15,
    "capex_friction": -0.15,
}
