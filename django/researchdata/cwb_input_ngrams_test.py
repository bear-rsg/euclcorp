from django.test import TestCase
import cwb_input_ngrams


class TestNgrams(TestCase):
    """
    Non-CI friendly unit tests for the Ngrams section of the website
    These must be run from a location that's able to access CWB on the RDS, e.g. the CAL Test VM
    CI-friendly tests (that don't require access to CWB) are located in 'tests.py'
    """

    def test_cwb_input_ngrams(self):
        """
        Tests that the CWB Ngrams input function returns expected data
        """

        # Query CWB with sample test data as inputs, to be used in multiple methods below
        cwb_ngrams_query_results = cwb_input_ngrams.query(primary_lang='BIRM_ENG',
                                                          Context=4,
                                                          query='[word="plea"%c]')

        expected_data_samples = [
            'First/first <plea/plea> in/in law/law',
            'the/the Ombudsman/Ombudsman raises/raise a/a single/single <plea/plea>',
            'The/the general/general <plea/plea> of/of inadmissibility/inadmissibility 69/[number]',
            'considered/consider the/the second/second <plea/plea>',
        ]

        self.assertIsNotNone(cwb_ngrams_query_results)  # Shouldn't return None
        self.assertIsInstance(cwb_ngrams_query_results, str)  # Should be a string
        self.assertGreater(len(cwb_ngrams_query_results), 10000)  # Should be more than 10000 chars in string
        # Should include all strings in expected_data_samples list
        for expected_data_sample in expected_data_samples:
            self.assertIn(expected_data_sample, self.cwb_ngrams_query_results)
