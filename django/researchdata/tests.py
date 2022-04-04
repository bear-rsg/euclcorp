from django.test import TestCase
from django.urls import reverse
import os
from . import cwb_output_collocations


class TestCollocations(TestCase):
    """
    CI-friendly unit tests for the Collocations section of the website
    These tests don't require access to CWB on the RDS
    Manual tests (not suitable for CI) are located in 'cwb_input_collocations_test.py'
    """

    # Query CWB with sample test data as inputs, to be used in multiple methods below
    f = open(os.path.join(os.path.dirname(__file__), 'testdata', 'testdata_cwb_input_collocations.txt'))
    cwb_collocations_query_results = f.read()


    def test_cwb_output_collocations(self):
        """
        Tests that the CWB Collocations output function returns expected data
        """

        test_options = {
            'countby': 'word',
            'spanleft': 3,
            'spanright': 3,
            'threshold': 2,
            'chosen_stats': ['llr', 'mi', 'mi3', 't-score', 'z-score', 'dice', 'frequency'],
            'primlang': 'BIRM_ENG'
        }

        # Returned data from the function being tested
        cwb_collocations_results_processed = cwb_output_collocations.process(cwb_query='[word="plea"%c]',
                                                                             cwb_output=self.cwb_collocations_query_results,
                                                                             options=test_options)[0]

        expected_data_samples = [
            {
                'word': 'the',
                'llr': '33850.44',
                'mi': '3.13',
                'tscore': '85.22',
                'zscore': '251.86',
                'dice': '0.0043',
                'mi3': '29.48',
                'frequency': '9263'
            },
            {
                'word': 'law',
                'llr': '20944.94',
                'mi': '6.64',
                'tscore': '52.32',
                'zscore': '522.08',
                'dice': '0.0442',
                'mi3': '29.53',
                'frequency': '2793'
            },
            {
                'word': 'alleging',
                'llr': '17631.40',
                'mi': '10.17',
                'tscore': '37.46',
                'zscore': '1273.75',
                'dice': '0.1591',
                'mi3': '31.09',
                'frequency': '1406'
            }
        ]

        self.assertIsNotNone(cwb_collocations_results_processed)  # Shouldn't return None
        self.assertIsInstance(cwb_collocations_results_processed, list)  # Should be a list
        self.assertIsInstance(cwb_collocations_results_processed[0], dict)  # First item in list should be a dictionary
        self.assertGreater(len(cwb_collocations_results_processed), 1000)  # Should be more than 1000 items in list
        # Should include all dicts in expected_data_samples list
        for expected_data_sample in expected_data_samples:
            self.assertIn(expected_data_sample, cwb_collocations_results_processed)
