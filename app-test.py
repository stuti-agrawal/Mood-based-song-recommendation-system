import unittest
import pandas as pd

from app import get_song, get_data_dict
class TestgetSong(unittest.TestCase):
    def test_getSong_success(self):
        """
        Test input values for getSong function
        """
         # Store data in pandas dataframe
        df = pd.DataFrame(get_data_dict())

        # Drop duplicates
        df.drop_duplicates(subset = "id", keep = "first", inplace = True)
        df.to_csv("arousal_dataset.csv", index = False)
        data = [df, 0.5, 0.5, 0.5]
        result = get_song(data)
        self.assertEqual(result, "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT")

if __name__ == '__main__':
    unittest.main()