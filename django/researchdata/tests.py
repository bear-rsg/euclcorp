from django.test import TestCase
import os
from . import (cwb_output_collocations, cwb_output_frequency, cwb_output_search, cwb_output_ngrams)


class TestSearch(TestCase):
    """
    CI-friendly unit tests for the Search section of the website
    These tests don't require access to CWB on the RDS
    Manual tests (not suitable for CI) are located in 'cwb_input_search_test.py'
    """

    # Query CWB with sample test data as inputs, to be used in multiple methods below
    with open(os.path.join(os.path.dirname(__file__), 'testdata', 'testdata_cwb_input_search.txt')) as f:
        cwb_search_results = f.read().splitlines()

    def test_cwb_output_search(self):
        """
        Tests that the CWB Search output function returns expected data
        """

        test_options = {
                    'primary_language': 'English',
                    'languages': ' +birm_deu +birm_fra',
                    'entriesperpage': '',
                    'bigsizelimit': ''
                }

        # Returned data from the function being tested
        cwb_search_results_processed = cwb_output_search.process(cwb_query='[word="plea"%c]',
                                                                 cwb_output=self.cwb_search_results,
                                                                 options=test_options)

        expected_data_sample = {
            "meta": {
                "case_name": "Judgment of the Court (Full Court) of 23 March 2004. # French Republic v Commission of the European Communities. # Guidelines on regulatory cooperation and transparency concluded with the United States of America - Non-binding character. # Case C-233/02.",  # NOQA
                "case_number": "62002CJ0233",
                "case_date": "2004/03/23",
                "doc_cellar": "68158cdb-85ef-40b7-817d-1d1e79d1ee64"
            },
            "languages": [
                {
                    "language_name": "English",
                    "content": "  By its first <plea, the French Government claims that the Commission is not competent to adopt the contested measure, inasmuch as the Guidelines amount to a binding international agreement the conclusion of which, under the division of powers pursuant to Article 300 EC, lies within the competence of the Council (Case C-327  91 France v Commission [ 1994 ] ECR I-3641).",  # NOQA
                    "kwic": {
                        "left_context": "By its first",
                        "match": "plea,",
                        "right_context": "the French Government claims that the Commission is not"
                    }
                }
            ]
        }

        # Shouldn't return None
        self.assertIsNotNone(cwb_search_results_processed)
        # Should be a list
        self.assertIsInstance(cwb_search_results_processed, list)
        # 1st item in list should be a dictionary
        self.assertIsInstance(cwb_search_results_processed[0], dict)
        # 1st item should have a dict value assigned to key 'meta'
        self.assertIsInstance(cwb_search_results_processed[0]['meta'], dict)
        # 1st item should have a list value assigned to key 'languages'
        self.assertIsInstance(cwb_search_results_processed[0]['languages'], list)
        # Should be more than 100 items in list
        self.assertGreater(len(cwb_search_results_processed), 100)
        # Should include expected sample data
        self.assertIn(expected_data_sample, cwb_search_results_processed)


class TestFrequency(TestCase):
    """
    CI-friendly unit tests for the Frequency section of the website
    These tests don't require access to CWB on the RDS
    Manual tests (not suitable for CI) are located in 'cwb_input_frequency_test.py'
    """

    # Query CWB with sample test data as inputs, to be used in multiple methods below
    with open(os.path.join(os.path.dirname(__file__), 'testdata', 'testdata_cwb_input_frequency.txt')) as f:
        cwb_frequency_results = f.read()

    def test_cwb_output_frequency(self):
        """
        Tests that the CWB Frequency output function returns expected data
        """

        # Returned data from the function being tested
        cwb_frequency_results_processed = cwb_output_frequency.process(cwb_output=self.cwb_frequency_results)

        expected_data_samples = [
            ['12472', 'plea'],
            ['142', 'Plea'],
            ['109', 'PLEA']
        ]

        # Shouldn't return None
        self.assertIsNotNone(cwb_frequency_results_processed)
        # Should be a list
        self.assertIsInstance(cwb_frequency_results_processed, list)
        # 1st item in list should be a list
        self.assertIsInstance(cwb_frequency_results_processed[0], list)
        # 1st item in 1st item should be a string
        self.assertIsInstance(cwb_frequency_results_processed[0][0], str)
        # 1st item in 1st item should be an int
        self.assertIsInstance(int(cwb_frequency_results_processed[0][0]), int)
        # Should be 3 items in list
        self.assertEquals(len(cwb_frequency_results_processed), 3)
        # Should include all lists in expected_data_samples list
        for expected_data_sample in expected_data_samples:
            self.assertIn(expected_data_sample, cwb_frequency_results_processed)


class TestCollocations(TestCase):
    """
    CI-friendly unit tests for the Collocations section of the website
    These tests don't require access to CWB on the RDS
    Manual tests (not suitable for CI) are located in 'cwb_input_collocations_test.py'
    """

    # Query CWB with sample test data as inputs, to be used in multiple methods below
    with open(os.path.join(os.path.dirname(__file__), 'testdata', 'testdata_cwb_input_collocations.txt')) as f:
        cwb_collocations_results = f.read()

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
                                                                             cwb_output=self.cwb_collocations_results,
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

        # Shouldn't return None
        self.assertIsNotNone(cwb_collocations_results_processed)
        # Should be a list
        self.assertIsInstance(cwb_collocations_results_processed, list)
        # 1st item in list should be a dictionary
        self.assertIsInstance(cwb_collocations_results_processed[0], dict)
        # Should be more than 1000 items in list
        self.assertGreater(len(cwb_collocations_results_processed), 1000)
        # Should include all dicts in expected_data_samples list
        for expected_data_sample in expected_data_samples:
            self.assertIn(expected_data_sample, cwb_collocations_results_processed)


class TestNgrams(TestCase):
    """
    CI-friendly unit tests for the Ngrams section of the website
    These tests don't require access to CWB on the RDS
    Manual tests (not suitable for CI) are located in 'cwb_input_ngrams_test.py'
    """

    # Query CWB with sample test data as inputs, to be used in multiple methods below
    with open(os.path.join(os.path.dirname(__file__), 'testdata', 'testdata_cwb_input_ngrams.txt')) as f:
        cwb_ngrams_results = f.read()

    def test_cwb_output_ngrams(self):
        """
        Tests that the CWB Ngrams output function returns expected data
        """

        test_options = {
            'countby': 'lemma',
            'size': 5,
            'frequencythreshold': 3
        }

        # Returned data from the function being tested
        cwb_ngrams_results_processed = cwb_output_ngrams.process(cwb_query='[word="plea"%c]',
                                                                 cwb_output=self.cwb_ngrams_results,
                                                                 options=test_options)

        expected_data_samples = [
            ['the first <strong>plea</strong> in law', 472],
            ['part of the first <strong>plea</strong>', 392],
            ['the second <strong>plea</strong> in law', 336],
            ['part of the second <strong>plea</strong>', 315],
            ['<strong>plea</strong> in law , allege', 250],
            ['<strong>plea</strong> in law , the', 245]
        ]

        # Shouldn't return None
        self.assertIsNotNone(cwb_ngrams_results_processed)
        # Should be a list
        self.assertIsInstance(cwb_ngrams_results_processed, list)
        # 1st item in list should be a list
        self.assertIsInstance(cwb_ngrams_results_processed[0], list)
        # 1st item in 1st item should be a string
        self.assertIsInstance(cwb_ngrams_results_processed[0][0], str)
        # Second item in 1st item should be an int
        self.assertIsInstance(cwb_ngrams_results_processed[0][1], int)
        # Should be more than 3000 items in list
        self.assertGreater(len(cwb_ngrams_results_processed), 3000)
        # Should include all dicts in expected_data_samples list
        for expected_data_sample in expected_data_samples:
            self.assertIn(expected_data_sample, cwb_ngrams_results_processed)
