import os
import pandas as pd


class LoadData(object):

    @staticmethod
    def load(data_dir):
        all_file_paths = os.listdir(data_dir)
        all_file_paths.sort()

        frames = []

        for file in all_file_paths:
            df = pd.read_csv(os.path.join(data_dir, file), encoding='iso-8859-1')
            frames.append(df)

        return pd.concat(frames).reset_index(drop=True)
