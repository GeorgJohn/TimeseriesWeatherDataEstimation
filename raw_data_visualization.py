"""
--- Climate Data Time-Series ---
We will be using Jena Climate dataset recorded by the
[Max Planck Institute for Biogeochemistry](https://www.bgc-jena.mpg.de/wetter/).
The dataset consists of 14 features such as temperature, pressure, humidity etc, recorded once per
10 minutes.
**Location**: Weather Station, Max Planck Institute for Biogeochemistry
in Jena, Germany
**Time-frame Considered**: Jan 10, 2009 - December 31, 2016
The table below shows the column names, their value formats, and their description.
Index| Features               |Format             |Description
-----|------------------------|-------------------|-----------------------
1    |Date Time               |01.01.2009 00:10:00|Date-time reference
2    |p (mbar)                |996.52             |The pascal SI derived unit of pressure used to quantify internal pressure. Meteorological reports typically state atmospheric pressure in millibars.
3    |T (degC)                |-8.02              |Temperature in Celsius
4    |Tpot (K)                |265.4              |Temperature in Kelvin
5    |Tdew (degC)             |-8.9               |Temperature in Celsius relative to humidity. Dew Point is a measure of the absolute amount of water in the air, the DP is the temperature at which the air cannot hold all the moisture in it and water condenses.
6    |rh (%)                  |93.3               |Relative Humidity is a measure of how saturated the air is with water vapor, the %RH determines the amount of water contained within collection objects.
7    |VPmax (mbar)            |3.33               |Saturation vapor pressure
8    |VPact (mbar)            |3.11               |Vapor pressure
9    |VPdef (mbar)            |0.22               |Vapor pressure deficit
10   |sh (g/kg)               |1.94               |Specific humidity
11   |H2OC (mmol/mol)         |3.12               |Water vapor concentration
12   |rho (g/m ** 3)          |1307.75            |Airtight
13   |wv (m/s)                |1.03               |Wind speed
14   |max. wv (m/s)           |1.75               |Maximum wind speed
15   |wd (deg)                |152.3              |Wind direction in degrees
16   |rain (mm)               |0.0                |Amount of the rainfall
17   |raining (s)             |0.0                |Duration of the rainfall
18   |SWDR (W/m ** 2)         |0.0                |Global radiation
19   |PAR (mu_mol/m**2/s)     |0.0                |Photosynthetically active radiation
20   |max. PAR (mu_mol/m**2/s)|0.0                |Maximum photosynthetically active radiation
21   |Tlog (degC)             |36.93              |Internal temperature of the data logger
22   |CO2 (ppm)               |434.1              |CO2 concentration of the outside air
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from loaddata import LoadData

data_dir = 'data/'

data = LoadData.load(data_dir=data_dir)

"""
-- Raw Data Visualization --
To give us a sense of the data we are working with, each feature has been plotted below.
This shows the distinct pattern of each feature over the time period from one day.
It also shows where anomalies are present, which will be addressed during normalization.
"""

titles = [
    "Pressure",
    "Temperature",
    "Temperature in Kelvin",
    "Temperature (dew point)",
    "Relative Humidity",
    "Saturation vapor pressure",
    "Vapor pressure",
    "Vapor pressure deficit",
    "Specific humidity",
    "Water vapor concentration",
    "Airtight",
    "Wind speed",
    "Maximum wind speed",
    "Wind direction in degrees",
    "Amount of the rainfall",
    "Duration of the rainfall",
    "Global radiation",
    "Photosynthetically radiation",
    "Maximum photosynthetically radiation",
    "Temperature of the data logger",
    "CO2 concentration",
]

feature_keys = [
    "p (mbar)",
    "T (degC)",
    "Tpot (K)",
    "Tdew (degC)",
    "rh (%)",
    "VPmax (mbar)",
    "VPact (mbar)",
    "VPdef (mbar)",
    "sh (g/kg)",
    "H2OC (mmol/mol)",
    "rho (g/m**3)",
    "wv (m/s)",
    "max. wv (m/s)",
    "wd (deg)",
    "rain (mm)",
    "raining (s)",
    "SWDR (W/m**2)",
    "PAR (mu_mol/m**2/s)",
    "max. PAR (mu_mol/m**2/s)",
    "Tlog (degC)",
    "CO2 (ppm)",
]

colors = [
    "blue",
    "orange",
    "green",
    "red",
    "purple",
    "brown",
    "pink",
    "gray",
    "olive",
    "cyan",
]

date_time_key = "Date Time"

print(data.head())

data.columns = ["Date Time"] + feature_keys


def show_raw_visualization(data_):
    time_data = data_[date_time_key]
    fig, axes = plt.subplots(
        nrows=7, ncols=3, figsize=(15, 20), dpi=80, facecolor="w", edgecolor="k"
    )
    for i in range(len(feature_keys)):
        key = feature_keys[i]
        c = colors[i % (len(colors))]
        t_data = data_[key]
        t_data.index = time_data
        t_data.head()
        ax = t_data.plot(
            ax=axes[i // 3, i % 3],
            color=c,
            title="{} - {}".format(titles[i], key),
            rot=25,
        )
        ax.legend([titles[i]])
    plt.tight_layout()
    plt.show()


def show_heatmap(data_):
    """
    This heat map shows the correlation
    between different features.
    """
    plt.matshow(data_.corr())
    plt.xticks(range(data_.shape[1]), data_.columns, fontsize=14, rotation=90)
    plt.gca().xaxis.tick_bottom()
    plt.yticks(range(data_.shape[1]), data_.columns, fontsize=14)

    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=14)
    plt.title("Feature Correlation Heatmap", fontsize=14)
    plt.show()


# visualize raw data
print('y := new plot of data \nn := no new plot')

for idx in range(data.shape[0] // 4320):

    choice = input('New plot? (y/n): ')

    if choice == 'y':
        df = data[idx*4320:idx*4320 + 4320]
        show_raw_visualization(df)
        show_heatmap(df)
    elif choice == 'n':
        break
