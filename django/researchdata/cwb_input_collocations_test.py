from django.test import TestCase
from django.urls import reverse
import .cwb_input_collocations


class TestCollocations(TestCase):
    """
    Non-CI friendly unit tests for the Collocations section of the website
    These must be run from a location that's able to access CWB on the RDS, e.g. the CAL Test VM
    CI-friendly tests (that don't require access to CWB) are located in 'tests.py'
    """

    def test_cwb_input_collocations(self):
        """
        Tests that the CWB Collocations input function returns expected data
        """

        # Query CWB with sample test data as inputs, to be used in multiple methods below
        cwb_collocations_query_results = cwb_input_collocations.query(primary_lang='BIRM_ENG',
                                                                      LeftContext=3,
                                                                      RightContext=3,
                                                                      query='[word="plea"%c]')

        expected_data_samples = [
            'first',
            'law',
            'Treaty',
            'argument',
            'in'
        ]

        self.assertIsNotNone(cwb_collocations_query_results)  # Shouldn't return None
        self.assertIsInstance(cwb_collocations_query_results, str)  # Should be a string
        self.assertGreater(len(cwb_collocations_query_results), 1000)  # Should be more than 1000 chars in string
        # Should include all strings in expected_data_samples list
        for expected_data_sample in expected_data_samples:
            self.assertIn(expected_data_sample, self.cwb_collocations_query_results)
