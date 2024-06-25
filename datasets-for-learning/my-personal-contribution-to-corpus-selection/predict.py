import numpy as np
from datetime import datetime, timedelta

def temperature_generator(date, lat, lon, individual):
    day_of_year = date.timetuple().tm_yday
    seasonal_factor = np.sin(2 * np.pi * day_of_year / 365)
    
    base_temp = 15 + 10 * seasonal_factor
    lat_effect = (lat - 45) * individual[0]
    lon_effect = (lon - 4) * individual[1]
    time_effect = (date.year - 2010) * individual[2]
    
    altitude_effect = individual[3]
    humidity_effect = individual[4] * seasonal_factor
    urban_heat_effect = individual[5] * (1 + 0.1 * (date.year - 2010))
    ocean_current_effect = individual[6] * np.sin(2 * np.pi * (day_of_year + 60) / 365)
    solar_activity_effect = individual[7] * np.random.normal(0, 1)
    climate_change_effect = individual[8] * (date.year - 2010) ** 2 / 100
    
    el_nino_effect = individual[9] * np.sin(2 * np.pi * (date.year - 2010) / 5)
    volcanic_activity = individual[10] * np.random.poisson(0.1)
    jet_stream_effect = individual[11] * np.sin(4 * np.pi * day_of_year / 365)
    land_use_change = individual[12] * (date.year - 2010) / 10
    air_pollution_effect = individual[13] * (1 + np.sin(2 * np.pi * day_of_year / 365))
    ocean_oscillation = individual[14] * np.sin(2 * np.pi * (date.year - 2010) / 60)
    
    latitude_season_interaction = individual[15] * lat * seasonal_factor
    urban_heat_pollution_interaction = individual[16] * urban_heat_effect * air_pollution_effect
    climate_change_ocean_interaction = individual[17] * climate_change_effect * ocean_oscillation
    
    gravity_effect = individual[18] * 9.8
    human_appearance_effect = individual[19] * (date.year - 2000000)
    stock_market_effect = individual[20] * np.sin(2 * np.pi * (date.year - 2020) / 5)
    
    random_effect = np.random.normal(0, 1) * individual[21]
    long_term_trend = individual[22] * (date.year - 2010) ** 3 / 1000
    
    Ev, Ed, Em = individual[23:26]
    C_values = individual[26:31]
    Pz, Re, Ec, Is, Ws, H = individual[31:37]
    T = (date - datetime(2010, 1, 1)).days / 365
    
    U = universalist_universe_equation(Ev, Ed, Em, C_values, Pz, Re, Ec, Is, Ws, H, T)

    return (base_temp + lat_effect + lon_effect + time_effect + altitude_effect + 
            humidity_effect + urban_heat_effect + ocean_current_effect + 
            solar_activity_effect + climate_change_effect + el_nino_effect +
            volcanic_activity + jet_stream_effect + land_use_change +
            air_pollution_effect + ocean_oscillation + latitude_season_interaction +
            urban_heat_pollution_interaction + climate_change_ocean_interaction +
            gravity_effect + human_appearance_effect + stock_market_effect +
            random_effect + long_term_trend + U)

def universalist_universe_equation(Ev, Ed, Em, C_values, Pz, Re, Ec, Is, Ws, H, T):
    E = Ev + Ed + Em
    C = sum(C_values)
    S = Pz + Re + Ec
    L = Is + Ws
    P = T  # Simple linear function for potentialities
    U = (E + (C * S * L) / H) * P
    return U

def fahrenheit_to_celsius(temp_f):
    return (temp_f - 32) * 5 / 9


# Best seed from the training
best_seed = [-4.93440298e-01, -5.98752453e-02, 6.47938036e-02, -6.63734693e-01,
             -3.99001999e-01, 9.97820658e-01, -2.92085531e+00, 2.57289246e-01,
             6.08877557e-01, 2.82814702e-01, 9.74928891e-01, 1.79172991e-01,
             1.00980512e+00, -3.45265950e-01, -7.90314017e-01, -5.84403680e-01,
             7.27944361e-01, 5.96068779e-02, -9.58745656e-01, -2.93103484e-05,
             -9.69290942e-01, 2.98673210e-01, 1.11515554e+00, -2.94661242e-01,
             4.38859909e-01, -6.32265438e-01, -1.18962465e+00, 1.74232844e+00,
             -1.65077564e+00, 1.92057715e+00, 6.54284524e-01, 2.89676433e-01,
             3.49516897e-01, 8.72598418e-02, 2.71443582e-01, -7.84965796e-01,
             -8.33939369e-01]

# Cities to predict
cities = [
    ("Lyon", 45.7640, 4.8357),
    ("Istanbul", 41.0082, 28.9784),
    ("Tokyo", 35.6895, 139.6917),
    ("New York", 40.7128, -74.0060),
    ("Sydney", -33.8688, 151.2093)
]

# Predict temperatures for the next 10 years
start_date = datetime(2024, 6, 25)
end_date = datetime(2034, 6, 25)
date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days)]

for city, lat, lon in cities:
    print(f"\nPrédictions pour {city}:")
    print("Date\t\tTempérature (°C)")
    print("-" * 30)
    for date in date_range:
        if date.month in [1, 4, 7, 10] and date.day == 1:  # Print predictions for the 1st day of each quarter
            temp_f = temperature_generator(date, lat, lon, best_seed)
            temp_c = fahrenheit_to_celsius(temp_f)
            print(f"{date.strftime('%Y-%m-%d')}\t{temp_c:.2f}")


print("\nNote: These predictions are based on the trained model and include various factors. Actual temperatures may vary.")
