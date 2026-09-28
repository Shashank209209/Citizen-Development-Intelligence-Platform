"""
Geographic hierarchy for India Prototype
Covers 5 states across South, North, and East regions:
- Karnataka (South)
- Tamil Nadu (South)
- Telangana (South)
- West Bengal (East)
- Uttar Pradesh (North)
"""

STATES_AND_DISTRICTS = [
    # Karnataka
    {
        "state": "Karnataka",
        "state_code": "KA",
        "district": "Kalaburagi",
        "district_code": "KA-KLB",
        "region": "South India",
        "lat": 17.3297,
        "lng": 76.8343,
        "is_aspirational_district": True
    },
    {
        "state": "Karnataka",
        "state_code": "KA",
        "district": "Belagavi",
        "district_code": "KA-BLG",
        "region": "South India",
        "lat": 15.8497,
        "lng": 74.4977,
        "is_aspirational_district": False
    },
    {
        "state": "Karnataka",
        "state_code": "KA",
        "district": "Shivamogga",
        "district_code": "KA-SHV",
        "region": "South India",
        "lat": 13.9299,
        "lng": 75.5681,
        "is_aspirational_district": False
    },
    {
        "state": "Karnataka",
        "state_code": "KA",
        "district": "Mysuru",
        "district_code": "KA-MYS",
        "region": "South India",
        "lat": 12.2958,
        "lng": 76.6394,
        "is_aspirational_district": False
    },
    {
        "state": "Karnataka",
        "state_code": "KA",
        "district": "Bengaluru Urban",
        "district_code": "KA-BLR",
        "region": "South India",
        "lat": 12.9716,
        "lng": 77.5946,
        "is_aspirational_district": False
    },

    # Tamil Nadu
    {
        "state": "Tamil Nadu",
        "state_code": "TN",
        "district": "Madurai",
        "district_code": "TN-MDU",
        "region": "South India",
        "lat": 9.9252,
        "lng": 78.1198,
        "is_aspirational_district": False
    },
    {
        "state": "Tamil Nadu",
        "state_code": "TN",
        "district": "Tiruchirappalli",
        "district_code": "TN-TRI",
        "region": "South India",
        "lat": 10.7905,
        "lng": 78.7047,
        "is_aspirational_district": False
    },
    {
        "state": "Tamil Nadu",
        "state_code": "TN",
        "district": "Salem",
        "district_code": "TN-SLM",
        "region": "South India",
        "lat": 11.6643,
        "lng": 78.1460,
        "is_aspirational_district": False
    },
    {
        "state": "Tamil Nadu",
        "state_code": "TN",
        "district": "Coimbatore",
        "district_code": "TN-CBE",
        "region": "South India",
        "lat": 11.0168,
        "lng": 76.9558,
        "is_aspirational_district": False
    },
    {
        "state": "Tamil Nadu",
        "state_code": "TN",
        "district": "Chennai",
        "district_code": "TN-CHN",
        "region": "South India",
        "lat": 13.0827,
        "lng": 80.2707,
        "is_aspirational_district": False
    },

    # Telangana
    {
        "state": "Telangana",
        "state_code": "TG",
        "district": "Khammam",
        "district_code": "TG-KHM",
        "region": "South India",
        "lat": 17.2473,
        "lng": 80.1514,
        "is_aspirational_district": True
    },
    {
        "state": "Telangana",
        "state_code": "TG",
        "district": "Warangal",
        "district_code": "TG-WRG",
        "region": "South India",
        "lat": 17.9689,
        "lng": 79.5941,
        "is_aspirational_district": False
    },
    {
        "state": "Telangana",
        "state_code": "TG",
        "district": "Nizamabad",
        "district_code": "TG-NZB",
        "region": "South India",
        "lat": 18.6725,
        "lng": 78.0941,
        "is_aspirational_district": False
    },
    {
        "state": "Telangana",
        "state_code": "TG",
        "district": "Karimnagar",
        "district_code": "TG-KRM",
        "region": "South India",
        "lat": 18.4386,
        "lng": 79.1288,
        "is_aspirational_district": False
    },
    {
        "state": "Telangana",
        "state_code": "TG",
        "district": "Hyderabad",
        "district_code": "TG-HYD",
        "region": "South India",
        "lat": 17.3850,
        "lng": 78.4867,
        "is_aspirational_district": False
    },

    # West Bengal
    {
        "state": "West Bengal",
        "state_code": "WB",
        "district": "Murshidabad",
        "district_code": "WB-MSD",
        "region": "East India",
        "lat": 24.1837,
        "lng": 88.2718,
        "is_aspirational_district": True
    },
    {
        "state": "West Bengal",
        "state_code": "WB",
        "district": "North 24 Parganas",
        "district_code": "WB-N24",
        "region": "East India",
        "lat": 22.7188,
        "lng": 88.4779,
        "is_aspirational_district": False
    },
    {
        "state": "West Bengal",
        "state_code": "WB",
        "district": "Howrah",
        "district_code": "WB-HWR",
        "region": "East India",
        "lat": 22.5958,
        "lng": 88.2636,
        "is_aspirational_district": False
    },
    {
        "state": "West Bengal",
        "state_code": "WB",
        "district": "Darjeeling",
        "district_code": "WB-DAR",
        "region": "East India",
        "lat": 27.0410,
        "lng": 88.2663,
        "is_aspirational_district": False
    },
    {
        "state": "West Bengal",
        "state_code": "WB",
        "district": "Kolkata",
        "district_code": "WB-KOL",
        "region": "East India",
        "lat": 22.5726,
        "lng": 88.3639,
        "is_aspirational_district": False
    },

    # Uttar Pradesh
    {
        "state": "Uttar Pradesh",
        "state_code": "UP",
        "district": "Varanasi",
        "district_code": "UP-VNS",
        "region": "North India",
        "lat": 25.3176,
        "lng": 82.9739,
        "is_aspirational_district": False
    },
    {
        "state": "Uttar Pradesh",
        "state_code": "UP",
        "district": "Lucknow",
        "district_code": "UP-LKO",
        "region": "North India",
        "lat": 26.8467,
        "lng": 80.9462,
        "is_aspirational_district": False
    },
    {
        "state": "Uttar Pradesh",
        "state_code": "UP",
        "district": "Kanpur Nagar",
        "district_code": "UP-KNP",
        "region": "North India",
        "lat": 26.4499,
        "lng": 80.3319,
        "is_aspirational_district": False
    },
    {
        "state": "Uttar Pradesh",
        "state_code": "UP",
        "district": "Agra",
        "district_code": "UP-AGR",
        "region": "North India",
        "lat": 27.1767,
        "lng": 78.0081,
        "is_aspirational_district": False
    },
    {
        "state": "Uttar Pradesh",
        "state_code": "UP",
        "district": "Prayagraj",
        "district_code": "UP-PRY",
        "region": "North India",
        "lat": 25.4358,
        "lng": 81.8463,
        "is_aspirational_district": False
    },

    # Bihar
    {
        "state": "Bihar",
        "state_code": "BR",
        "district": "Gaya",
        "district_code": "BR-GAY",
        "region": "East India",
        "lat": 24.7914,
        "lng": 85.0002,
        "is_aspirational_district": True
    }
]
