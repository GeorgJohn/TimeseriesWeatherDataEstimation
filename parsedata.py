import numpy as np

rng = np.random.default_rng()


class ParseData(object):

    """
    Date Time format: 01.01.2009 00:10:00
    """
    date_time_key = "Date Time"

    titles = [
        "Pressure",                              # 0
        "Temperature",                           # 1
        "Temperature in Kelvin",                 # -
        "Temperature (dew point)",               # -
        "Relative Humidity",                     # -
        "Saturation vapor pressure",             # 5
        "Vapor pressure",                        # -
        "Vapor pressure deficit",                # 7
        "Specific humidity",                     # 8
        "Water vapor concentration",             # -
        "Airtight",                              # 10
        "Wind speed",                            # 11
        "Maximum wind speed",                    # -
        "Wind direction in degrees",             # -
        "Amount of the rainfall",                # 14
        "Duration of the rainfall",              # 15
        "Global radiation",                      # 16
        "Photosynthetically radiation",          # -
        "Maximum photosynthetically radiation",  # -
        "Temperature of the data logger",        # -
        "CO2 concentration",                     # 20
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

    selected_features = [0, 1, 5, 7, 8, 10, 11, 14, 15, 16, 20]

    def parse(self, data):

        # update header of data frame
        data.columns = [self.date_time_key] + self.feature_keys
        print(
            "The selected parameters are:\n",
            ", ".join([self.titles[i] for i in self.selected_features]),
        )

        selected_feature_keys = [self.feature_keys[i] for i in self.selected_features]

        """
        Transform the data set from one dataframe to numpy arrays that can be used for training
        
        training set contains includes measurements every 10 minutes with selected features
        shape: [number of days, number of measurements, number of features]
        
        label is the amount of rain in one day
        shape: [number of days, ]
        """
        x = None
        y = None

        curr_date = ' '
        rain_sum = 0.0
        sample = None

        next_date = [data[self.date_time_key][0][0:10]]
        for idx in range(1, data.shape[0]):

            sample_entry = data[selected_feature_keys].iloc[[idx]].to_numpy()
            rain_sum += data.iloc[idx][self.feature_keys[14]]

            if sample is None:
                # update date
                curr_date = next_date
                # create new sample
                sample = sample_entry
            elif next_date == curr_date:
                # append new sample entry
                sample = np.concatenate([sample, sample_entry], axis=0)
            else:
                # append last sample entry for current date
                sample = np.concatenate([sample, sample_entry], axis=0)

                # check if sample is a complete day 6 * 24h = 144 entries
                if sample.shape[0] == 144:
                    if x is None:
                        # initialize x and y
                        x = np.expand_dims(sample, axis=0)
                        y = np.expand_dims(rain_sum, axis=0)
                    else:
                        # append new sample to x_train
                        sample = np.expand_dims(sample, axis=0)
                        x = np.concatenate([x, sample], axis=0)
                        # append sum of rain to y_train
                        label = np.expand_dims(rain_sum, axis=0)
                        y = np.concatenate([y, label], axis=0)

                sample = None
                rain_sum = 0.0

            next_date = [data[self.date_time_key][idx][0:10]]

        """ Select as many rainy days as non rainy days """
        non_rain_days = np.squeeze(np.argwhere(y == 0.0))
        rain_days = np.squeeze(np.argwhere(y != 0.0))

        non_rain_days = rng.choice(non_rain_days, rain_days.shape[0], replace=False)

        y_choice = np.concatenate([y[non_rain_days], y[rain_days]], axis=0)
        x_choice = np.concatenate([x[non_rain_days, :, :], x[rain_days, :, :]], axis=0)

        # test
        n_non_rain_days = non_rain_days.shape[0]
        n_rainy_days = rain_days.shape[0]

        print(f'Number of rainy days: {n_rainy_days}')
        print(f'Number of non rainy days: {n_non_rain_days}')

        print(x_choice.shape)
        print(y_choice.shape)

        return None, None

    @staticmethod
    def normalize(data, train_split):
        data_mean = data[:train_split].mean(axis=0)
        data_std = data[:train_split].std(axis=0)
        return (data - data_mean) / data_std
