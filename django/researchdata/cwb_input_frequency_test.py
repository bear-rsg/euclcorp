
from django.test import TestCase
import cwb_input_frequency


class TestFrequency(TestCase):
    """
    Non-CI friendly unit tests for the Frequency section of the website
    These must be run from a location that's able to access CWB on the RDS, e.g. the CAL Test VM
    CI-friendly tests (that don't require access to CWB) are located in 'tests.py'
    """

    def test_cwb_input_frequency(self):
        """
        Tests that the CWB Frequency input function returns expected data
        """

        # Query CWB with sample test data as inputs, to be used in multiple methods below
        cwb_frequency_query_results = cwb_input_frequency.query(primary_lang='BIRM_ENG',
                                                                F='[word="plea"%c]',
                                                                countby='word')

        expected_data_samples = [
            '12472',
            'plea'
        ]

        self.assertIsNotNone(cwb_frequency_query_results)  # Shouldn't return None
        self.assertIsInstance(cwb_frequency_query_results, str)  # Should be a string
        # Should include all strings in expected_data_samples list
        for expected_data_sample in expected_data_samples:
            self.assertIn(expected_data_sample, self.cwb_frequency_query_results)
