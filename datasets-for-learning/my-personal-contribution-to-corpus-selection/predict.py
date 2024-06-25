import numpy as np
from datetime import datetime, timedelta

# Best seed trouvé
best_seed = [3.07884074e-02, -3.93571226e-02, 1.31884283e+00, 4.50809659e-02,
             -2.47606217e-01, 5.84794615e-01, -5.39112384e-01, 4.96286112e-01,
             9.23451878e-01, -6.24043719e-01, 6.33211042e-01, -3.20163657e-02,
             1.68033491e-01, -5.99763720e-01, -4.33616230e-01, 3.43189124e-01,
             8.46544825e-01, 6.97983727e-01, -1.16251357e+00, -2.82604501e-05,
             -6.57868849e-01, 1.80093859e-01, 7.75894392e-01, -2.04552299e-01,
             -3.17693894e-01, -7.91174209e-01, -4.77260944e-01, 8.82751697e-01,
             -6.31264341e-01, 9.31562141e-01, -5.89906433e-01, -7.57313860e-01,
             -1.80197754e-01, -4.69141811e-02, -4.58976024e-01, -4.42463598e-01,
             -6.64891940e-01]

def universalist_universe_equation(Ev, Ed, Em, C_values, Pz, Re, Ec, Is, Ws, H, T):
    E = Ev + Ed + Em
    C = sum(C_values)
    S = Pz + Re + Ec
    L = Is + Ws
    P = f(T)
    U = (E + (C * S * L) / H) * P
    return U

def f(T):
    return T

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
    
    Ev = individual[23]
    Ed = individual[24]
    Em = individual[25]
    C_values = individual[26:26+5]
    Pz = individual[31]
    Re = individual[32]
    Ec = individual[33]
    Is = individual[34]
    Ws = individual[35]
    H = individual[36]
    T = (date - datetime(2010, 1, 1)).days / 365
    
    U = universalist_universe_equation(Ev, Ed, Em, C_values, Pz, Re, Ec, Is, Ws, H, T)

    temp_fahrenheit = (base_temp + lat_effect + lon_effect + time_effect + altitude_effect + 
                       humidity_effect + urban_heat_effect + ocean_current_effect + 
                       solar_activity_effect + climate_change_effect + el_nino_effect +
                       volcanic_activity + jet_stream_effect + land_use_change +
                       air_pollution_effect + ocean_oscillation + latitude_season_interaction +
                       urban_heat_pollution_interaction + climate_change_ocean_interaction +
                       gravity_effect + human_appearance_effect + stock_market_effect +
                       random_effect + long_term_trend + U)
    
    temp_celsius = (temp_fahrenheit - 32) * 5.0/9.0
    return temp_celsius

# Prédire les températures pour les 6 prochains mois à Lyon
lat_lyon = 45.7640
lon_lyon = 4.8357
start_date = datetime(2024, 6, 25)
end_date = start_date + timedelta(days=182)  # 6 mois

dates = []
temperatures = []

current_date = start_date
while current_date <= end_date:
    temp = temperature_generator(current_date, lat_lyon, lon_lyon, best_seed)
    dates.append(current_date)
    temperatures.append(temp)
    current_date += timedelta(days=1)

# Affichage des résultats
for date, temp in zip(dates, temperatures):
    print(f"{date.strftime('%Y-%m-%d')}: {temp:.2f}°C")

# Optionnel : Visualisation des résultats
plt.figure(figsize=(12, 6))
plt.plot(dates, temperatures, label='Température à Lyon')
plt.xlabel('Date')
plt.ylabel('Température (°C)')
plt.title('Prédiction de la température pour les 6 prochains mois à Lyon')
plt.legend()
plt.grid(True)
plt.show()
