import unittest
from unittest.mock import patch
import pandas as pd
from bike_investigation import get_filters, load_data, clean_data, time_stats, station_stats, trip_duration_stats, user_stats


class TestBikeShareData(unittest.TestCase):

    def setUp(self):
        self.mock_data = {
            '': [123, 456545, 15987],
            'Start Time': pd.to_datetime(['2017-01-01 09:13:21', '2017-01-02 09:07:57', '2017-03-03 00:08:20']),
            'End Time': pd.to_datetime(['2017-01-01 10:17:12', '2017-01-02 09:20:53', '2017-03-03 00:20:53']),
            'Trip Duration': [3831.35, 780, 750],
            'Start Station': ['Wood St & Hubbard St', 'May St & Taylor St', 'May St & Taylor St'],
            'End Station': ['Larrabee St & Kingsbury St', 'St. Louis Ave & Balmoral Ave', 'St. Louis Ave & Balmoral Ave'],
            'User Type': ['Subscriber', 'Customer', 'Customer'],
            'Gender': ['Male', 'Female', 'Male'],
            'Birth Year': [1990, 1990, 2001]
        }
        self.mock_df = pd.DataFrame(self.mock_data)

    # =================
    # test_get_filters
    # -----------------
    @patch('builtins.input')
    def test_get_filters(self, mock_input):
        test_cases = [
            # (input_values, expected_city, expected_month, expected_day)
            (['chicago', 'all', 'all'], 'chicago', 'all', 'all'),
            (['new york city', 'march', 'monday'], 'new york city', 'march', 'monday'),
            (['washington', 'june', 'all'], 'washington', 'june', 'all'),
            (['invalid city', 'chicago', 'july', '', 'february', 'invalid day', '7', 'wednesday'],
             'chicago', 'february', 'wednesday')  # Invalid sequence & error handling
        ]
        for inputs, expected_city, expected_month, expected_day in test_cases:
            mock_input.side_effect = inputs

            city, month, day = get_filters()
            self.assertEqual(city, expected_city)
            self.assertEqual(month, expected_month)
            self.assertEqual(day, expected_day)

    # ===============
    # test_load_data
    # ---------------
    @patch('pandas.read_csv')
    def test_load_data_filters(self, mock_read_csv):
        mock_read_csv.return_value = self.mock_df

        test_cases = [
            # (city, month, day, expected_row_count)
            ('chicago', 'all', 'all', 3),  # No filters
            ('washington', 'january', 'all', 2),  # Month filter
            ('new york city', 'all', 'monday', 1),  # Day filter
            ('chicago', 'march', 'friday', 1),  # All filters, 1 row in mock_df
            ('washington', 'march', 'sunday', 0)  # All, no march/sunday in mock_df
        ]
        for city, month, day, expected_row_count in test_cases:
            result_df = load_data(city, month, day)
            self.assertIn('Month', result_df.columns)
            self.assertIn('Weekday', result_df.columns)
            self.assertIn('Hour', result_df.columns)
            self.assertEqual(result_df.shape[0], expected_row_count)

    # ================
    # test_clean_data
    # ----------------
    def test_clean_data(self):
        cleaned_df = clean_data(self.mock_df)
        # No cleaning needed
        self.assertEqual(len(cleaned_df), 3)

    def test_clean_data_no_duplicates(self):
        df = pd.concat([self.mock_df, self.mock_df.iloc[0:1]], ignore_index=True)
        cleaned_df = clean_data(df)
        # Dropped duplicated line
        self.assertEqual(len(cleaned_df), 3)

    def test_clean_data_drop_relevant_na(self):
        df = self.mock_df.copy()
        df.loc[1, 'Start Time'] = None
        cleaned_df = clean_data(df)
        # Dropped missing relevant value line
        self.assertEqual(len(cleaned_df), 2)

    def test_clean_data_fill_na(self):
        df = self.mock_df.copy()
        df.loc[1, 'User Type'] = None
        df.loc[2, 'Gender'] = None
        cleaned_df = clean_data(df)
        # Replaced missing values
        self.assertEqual(cleaned_df['User Type'].iloc[1], 'Unknown')
        self.assertEqual(cleaned_df['Gender'].iloc[2], 'Unknown')

    def test_clean_data_drop_duration_outliers(self):
        df = self.mock_df.copy()
        df.loc[0, 'Trip Duration'] = 9999999
        cleaned_df = clean_data(df)
        # Dropped duration outlier line
        self.assertEqual(len(cleaned_df), 2)

    def test_clean_data_drop_negative_duration(self):
        df = self.mock_df.copy()
        df.loc[1, 'Trip Duration'] = -800
        df.loc[2, 'End Time'] = pd.to_datetime('2017-01-01 00:20:53')
        cleaned_df = clean_data(df)
        # Dropped negative duration lines
        self.assertEqual(len(cleaned_df), 1)

    def test_clean_data_drop_inconsistent_duration(self):
        df = self.mock_df.copy()
        df.loc[0, 'Trip Duration'] = 5000
        cleaned_df = clean_data(df)
        # Dropped inconsistent duration line
        self.assertEqual(len(cleaned_df), 2)

    # ================
    # test_time_stats
    # ----------------
    @patch('builtins.print')
    def test_time_stats(self, mock_print):
        data = {
            'Month': ['january', 'january', 'february', 'march', 'march'],
            'Weekday': ['monday', 'monday', 'wednesday', 'wednesday', 'wednesday'],
            'Hour': [8, 9, 10, 8, None]
        }
        result_df = pd.DataFrame(data)
        time_stats(result_df)
        printed_output = [call[0][0] for call in mock_print.call_args_list]

        # Most common month
        self.assertIn("The most common month is January, with 2 occurrences.", printed_output)
        # Most common weekday
        self.assertIn("The most common weekday is Wednesday, with 3 occurrences.", printed_output)
        # Most common start hour
        self.assertIn("The most common start hour is 8h, with 2 occurrences.", printed_output)

    @patch('builtins.print')
    def test_time_stats_filters(self, mock_print):
        data_f_month = {
            'Month': ['january', 'january', 'january'],
            'Weekday': ['monday', 'wednesday', 'wednesday'],
            'Hour': [8, 9, 8]
        }
        data_f_day = {
            'Month': ['january', 'march', 'january'],
            'Weekday': ['wednesday', 'wednesday', 'wednesday'],
            'Hour': [9, 9, 8]
        }
        df_f_month = pd.DataFrame(data_f_month)
        df_f_day = pd.DataFrame(data_f_day)

        time_stats(df_f_month)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # Month filter on
        self.assertIn("Filter set to January", printed_output)

        time_stats(df_f_day)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # Weekday filter on
        self.assertIn("Filter set to Wednesday", printed_output)

    @patch('builtins.print')
    def test_time_stats_missing_data(self, mock_print):
        data = {
            'Month': [],
            'Weekday': [],
            'Hour': []
        }
        result_df = pd.DataFrame(data)
        time_stats(result_df)
        printed_output = [call[0][0] for call in mock_print.call_args_list]

        # Empty DataFrame identified
        self.assertIn("/!\\ No data available to display time statistics.", printed_output)

    # ===================
    # test_station_stats
    # -------------------
    @patch('builtins.print')
    def test_station_stats(self, mock_print):
        station_stats(self.mock_df)
        printed_output = [call[0][0] for call in mock_print.call_args_list]

        # Most common start station
        self.assertIn("The most commonly used start station is May St & Taylor St, with 2 occurrences.", printed_output)
        # Most common end station
        self.assertIn("The most commonly used end station is St. Louis Ave & Balmoral Ave, with 2 occurrences.", printed_output)
        # Most common trip
        self.assertIn("The most common trip is: May St & Taylor St --> St. Louis Ave & Balmoral Ave, with 2 occurrences.", printed_output)

    @patch('builtins.print')
    def test_station_stats_missing_data(self, mock_print):
        data = {
            'Start Station': [],
            'End Station': []
        }
        result_df = pd.DataFrame(data)
        station_stats(result_df)
        printed_output = [call[0][0] for call in mock_print.call_args_list]

        # Empty DataFrame identified
        self.assertIn("/!\\ No data available to display station statistics.", printed_output)

    # ====================
    # test_duration_stats
    # --------------------
    @patch('builtins.print')
    def test_trip_duration_stats(self, mock_print):
        trip_duration_stats(self.mock_df)
        printed_output = [call[0][0] for call in mock_print.call_args_list]

        # Total travel time
        self.assertIn("Total travel time : 5,361.35sec = 89.36min = 1.49h = 0.06 days", printed_output)
        # Mean travel time
        self.assertIn("Mean travel time : 1,787.12sec = 29.79min = 0.50h", printed_output)

    @patch('builtins.print')
    def test_trip_duration_stats_missing_data(self, mock_print):
        data = {
            'Trip Duration': []
        }
        result_df = pd.DataFrame(data)
        trip_duration_stats(result_df)
        printed_output = [call[0][0] for call in mock_print.call_args_list]

        # Empty DataFrame identified
        self.assertIn("/!\\ No data available to display duration statistics.", printed_output)

    # ================
    # test_user_stats
    # ----------------
    @patch('builtins.print')
    def test_user_stats(self, mock_print):
        user_stats(self.mock_df)
        printed_output = [call[0][0] for call in mock_print.call_args_list]

        # Counts of user types
        self.assertIn("User Type\nCustomer      2\nSubscriber    1\n", printed_output)
        # Counts of gender
        self.assertIn("Gender\nFemale    1\nMale      2\n", printed_output)
        # Birth year stats
        self.assertIn("Earliest year of birth: 1990", printed_output)
        self.assertIn("Most recent year of birth: 2001", printed_output)
        self.assertIn("Most common year of birth: 1990", printed_output)

    @patch('builtins.print')
    def test_user_stats_missing_data(self, mock_print):
        data = {
            'User Type': []
        }
        result_df = pd.DataFrame(data)
        no_gender_df = self.mock_df.drop(columns=['Gender'])
        no_birth_year_df = self.mock_df.drop(columns=['Birth Year'])

        user_stats(result_df)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # Empty DataFrame identified
        self.assertIn("/!\\ No data available to display user statistics.", printed_output)

        user_stats(no_gender_df)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # No Gender identified
        self.assertIn('No gender data available for this city.', printed_output)

        user_stats(no_birth_year_df)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # No Birth Year identified
        self.assertIn('No data on dates of birth available for this city.', printed_output)


if __name__ == '__main__':
    unittest.main()
