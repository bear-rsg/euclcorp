from django.test import TestCase
import cwb_input_search


class TestSearch(TestCase):
    """
    Non-CI friendly unit tests for the Search section of the website
    These must be run from a location that's able to access CWB on the RDS, e.g. the CAL Test VM
    CI-friendly tests (that don't require access to CWB) are located in 'tests.py'
    """

    def test_cwb_input_search(self):
        """
        Tests that the CWB Search input function returns expected data
        """

        # Query CWB with sample test data as inputs, to be used in multiple methods below
        cwb_search_query_results = cwb_input_search.query(primary_lang='BIRM_ENG',
                                                          context_left_or_right='',
                                                          context='1s',
                                                          show='+lemma +tag',
                                                          A='[word="plea"%c]',
                                                          start=1,
                                                          length=500)

        expected_data_samples = [
            '9458:',
            '<meta_case_name Judgment of the Court (Full Court)',
            '23 March 2004.'
        ]

        self.assertIsNotNone(cwb_search_query_results)  # Shouldn't return None
        self.assertIsInstance(cwb_search_query_results, str)  # Should be a string
        self.assertGreater(len(cwb_search_query_results), 1000)  # Should be more than 1000 chars in string
        # Should include all strings in expected_data_samples list
        for expected_data_sample in expected_data_samples:
            self.assertIn(expected_data_sample, self.cwb_search_query_results)
