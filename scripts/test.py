import unittest
import json

from reconciliator_all import *


class Clustering(unittest.TestCase):
    maxDiff = None

    def test_extract_all_data(self):
        """
        This function checks if the clustering of similar entries works or not.
        Informations of the three entries are the same, except from the ids and the sell dates.
        """
        input_data = {
            "CAT_000001_e1_d1": {
                "price": 75.0,
                "author": "S\u00e9vign\u00e9",
                "date": "1697-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1888-10",
                "desc": "Pi\u00e8ce de 3 lignes aut., mai 1697, 1/4 de p. in-4."
            },
            "CAT_000002_e1_d1": {
                "price": 75.0,
                "author": "S\u00e9vign\u00e9",
                "date": "1697-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1889-10",
                "desc": "Pi\u00e8ce de 3 lignes aut., mai 1697, 1/4 de p. in-4."
            },
            "CAT_000003_e1_d1": {
                "price": 75.0,
                "author": "S\u00e9vign\u00e9",
                "date": "1697-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1890-10",
                "desc": "Pi\u00e8ce de 3 lignes aut., mai 1697, 1/4 de p. in-4."
            }
        }

        output_test = reconciliator(input_data)

        test_dict = {
            "descs_processed": 3,
            "mss_reconciliated": 1,
            "single_sale_count": 0,
            "multiple_sales_count": 3,
            "multiple_sales": [
                {
                    "mss": [
                        {"price": 75.0,
                         "author": "S\u00e9vign\u00e9",
                         "date": "1697-05",
                         "number_of_pages": 0.25,
                         "format": 4,
                         "term": 3,
                         "sell_date": "1888-10",
                         "desc": "Pi\u00e8ce de 3 lignes aut., mai 1697, 1/4 de p. in-4.",
                         "id": "CAT_000001_e1_d1"
                         },
                        {
                            "price": 75.0,
                            "author": "S\u00e9vign\u00e9",
                            "date": "1697-05",
                            "number_of_pages": 0.25,
                            "format": 4,
                            "term": 3,
                            "sell_date": "1889-10",
                            "desc": "Pi\u00e8ce de 3 lignes aut., mai 1697, 1/4 de p. in-4.",
                            "id": "CAT_000002_e1_d1"
                        },
                        {
                            "price": 75.0,
                            "author": "S\u00e9vign\u00e9",
                            "date": "1697-05",
                            "number_of_pages": 0.25,
                            "format": 4,
                            "term": 3,
                            "sell_date": "1890-10",
                            "desc": "Pi\u00e8ce de 3 lignes aut., mai 1697, 1/4 de p. in-4.",
                            "id": "CAT_000003_e1_d1"
                        }
                    ],
                    "scores": [
                        [
                            "CAT_000001_e1_d1",
                            "CAT_000002_e1_d1",
                            1.2000000000000002
                        ],
                        [
                            "CAT_000001_e1_d1",
                            "CAT_000003_e1_d1",
                            1.2000000000000002
                        ],
                        [
                            "CAT_000002_e1_d1",
                            "CAT_000003_e1_d1",
                            1.2000000000000002
                        ]
                    ]
                }
            ],
            "single_sale": []
        }

        self.assertDictEqual(output_test, test_dict)


class Authors(unittest.TestCase):
    maxDiff = None

    def test_distinct_authors(self):
        """
        This function checks that entries with distinct authors are not clustered, even if the others data are the same.
        """

        input_data = {
            "CAT_000001_e1_d1": {
                "price": 75.0,
                "author": "Balzac",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1888-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            },
            "CAT_000002_e1_d1": {
                "price": 75.0,
                "author": "Hugo",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1889-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            }
        }

        output_test = reconciliator(input_data)

        test_dict = {
            "descs_processed": 2,
            "mss_reconciliated": 0,
            "single_sale_count": 2,
            "multiple_sales_count": 0,
            "multiple_sales": [],
            "single_sale": [
                {
                    "price": 75.0,
                    "author": "Balzac",
                    "date": "1847-05",
                    "number_of_pages": 0.25,
                    "format": 4,
                    "term": 3,
                    "sell_date": "1888-10",
                    "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                    "id": "CAT_000001_e1_d1"
                },
                {"price": 75.0,
                 "author": "Hugo",
                 "date": "1847-05",
                 "number_of_pages": 0.25,
                 "format": 4,
                 "term": 3,
                 "sell_date": "1889-10",
                 "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                 "id": "CAT_000002_e1_d1"
                 }
            ]
        }

        self.assertDictEqual(output_test, test_dict)

    def test_similar_authors(self):
        """
        This function checks that entries with similar authors (typo in the name for example) are clustered.
        In this test, two letters are missing : 'Balzac' and 'Balz'.
        """

        input_data = {
            "CAT_000001_e1_d1": {
                "price": 75.0,
                "author": "Balzac",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1888-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            },
            "CAT_000002_e1_d1": {
                "price": 75.0,
                "author": "Balz",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1889-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            }
        }

        output_test = reconciliator(input_data)

        test_dict = {
            "descs_processed": 2,
            "mss_reconciliated": 1,
            "single_sale_count": 0,
            "multiple_sales_count": 2,
            "multiple_sales": [
                {
                    "mss": [
                        {"price": 75.0,
                         "author": "Balzac",
                         "date": "1847-05",
                         "number_of_pages": 0.25,
                         "format": 4,
                         "term": 3,
                         "sell_date": "1888-10",
                         "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                         "id": "CAT_000001_e1_d1"
                         },
                        {
                            "price": 75.0,
                            "author": "Balz",
                            "date": "1847-05",
                            "number_of_pages": 0.25,
                            "format": 4,
                            "term": 3,
                            "sell_date": "1889-10",
                            "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                            "id": "CAT_000002_e1_d1"
                        }
                    ],
                    "scores": [
                        [
                            "CAT_000001_e1_d1",
                            "CAT_000002_e1_d1",
                            1.2000000000000002
                        ]
                    ]
                }
            ],
            "single_sale": []
        }

        self.assertDictEqual(output_test, test_dict)


class ID(unittest.TestCase):
    maxDiff = None

    def test_same_catalogue(self):
        """
        This function checks that two entries of a same catalogue are not clustered : a manuscript can't be sold more than once in a single catalogue.
        """
        input_data = {
            "CAT_000001_e1_d1": {
                "price": 75.0,
                "author": "Balzac",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1888-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            },
            "CAT_000001_e3_d1": {
                "price": 75.0,
                "author": "Balzac",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1889-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            }
        }

        output_test = reconciliator(input_data)

        test_dict = {
            "descs_processed": 2,
            "mss_reconciliated": 0,
            "single_sale_count": 2,
            "multiple_sales_count": 0,
            "multiple_sales": [],
            "single_sale": [
                {"price": 75.0,
                 "author": "Balzac",
                 "date": "1847-05",
                 "number_of_pages": 0.25,
                 "format": 4,
                 "term": 3,
                 "sell_date": "1888-10",
                 "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                 "id": "CAT_000001_e1_d1"
                 },
                {"price": 75.0,
                 "author": "Balzac",
                 "date": "1847-05",
                 "number_of_pages": 0.25,
                 "format": 4,
                 "term": 3,
                 "sell_date": "1889-10",
                 "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                 "id": "CAT_000001_e3_d1"
                 }
            ]
        }

        self.assertDictEqual(output_test, test_dict)

    def test_same_entry(self):
        """
        This function checks that two descs of a same entry (= a same catalogue) are not clustered : a manuscript can't be sold more than once in a single catalogue.
        """
        input_data = {
            "CAT_000001_e1_d1": {
                "price": 75.0,
                "author": "Balzac",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1888-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            },
            "CAT_000001_e1_d2": {
                "price": 75.0,
                "author": "Balzac",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1889-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            }
        }

        output_test = reconciliator(input_data)

        test_dict = {
            "descs_processed": 2,
            "mss_reconciliated": 0,
            "single_sale_count": 2,
            "multiple_sales_count": 0,
            "multiple_sales": [],
            "single_sale": [
                {"price": 75.0,
                 "author": "Balzac",
                 "date": "1847-05",
                 "number_of_pages": 0.25,
                 "format": 4,
                 "term": 3,
                 "sell_date": "1888-10",
                 "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                 "id": "CAT_000001_e1_d1"
                 },
                {"price": 75.0,
                 "author": "Balzac",
                 "date": "1847-05",
                 "number_of_pages": 0.25,
                 "format": 4,
                 "term": 3,
                 "sell_date": "1889-10",
                 "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                 "id": "CAT_000001_e1_d2"
                 }
            ]
        }

        self.assertDictEqual(output_test, test_dict)


class Missing_param(unittest.TestCase):
    maxDiff = None

    def test_author(self):
        """
        This function checks that if the author is missing, there is no clustering.
        """
        input_data = {
            "CAT_000001_e1_d1": {
                "price": 75.0,
                "author": "Balzac",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1888-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            },
            "CAT_000001_e1_d2": {
                "price": 75.0,
                "author": "",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1889-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            }
        }

        output_test = reconciliator(input_data)

        test_dict = {
            "descs_processed": 2,
            "mss_reconciliated": 0,
            "single_sale_count": 2,
            "multiple_sales_count": 0,
            "multiple_sales": [],
            "single_sale": [
                {"price": 75.0,
                 "author": "Balzac",
                 "date": "1847-05",
                 "number_of_pages": 0.25,
                 "format": 4,
                 "term": 3,
                 "sell_date": "1888-10",
                 "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                 "id": "CAT_000001_e1_d1"
                 },
                {"price": 75.0,
                 "author": "",
                 "date": "1847-05",
                 "number_of_pages": 0.25,
                 "format": 4,
                 "term": 3,
                 "sell_date": "1889-10",
                 "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                 "id": "CAT_000001_e1_d2"
                 }
            ]
        }

        self.assertDictEqual(output_test, test_dict)

    def test_price(self):
        """
        This function checks that if the price is missing/different, there is a clustering.
        """
        input_data = {
            "CAT_000001_e1_d1": {
                "price": None,
                "author": "Balzac",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1888-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            },
            "CAT_000002_e1_d1": {
                "price": 75.0,
                "author": "Balzac",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1889-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            }
        }

        output_test = reconciliator(input_data)

        test_dict = {
            "descs_processed": 2,
            "mss_reconciliated": 1,
            "single_sale_count": 0,
            "multiple_sales_count": 2,
            "multiple_sales": [
                {
                    "mss": [
                        {"price": None,
                         "author": "Balzac",
                         "date": "1847-05",
                         "number_of_pages": 0.25,
                         "format": 4,
                         "term": 3,
                         "sell_date": "1888-10",
                         "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                         "id": "CAT_000001_e1_d1"
                         },
                        {
                            "price": 75.0,
                            "author": "Balzac",
                            "date": "1847-05",
                            "number_of_pages": 0.25,
                            "format": 4,
                            "term": 3,
                            "sell_date": "1889-10",
                            "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                            "id": "CAT_000002_e1_d1"
                        }
                    ],
                    "scores": [
                        [
                            "CAT_000001_e1_d1",
                            "CAT_000002_e1_d1",
                            1.0
                        ]
                    ]
                }
            ],
            "single_sale": []
        }

        self.assertDictEqual(output_test, test_dict)

    def test_date(self):
        """
        This function checks that if the date is missing/different, there is a clustering.
        """
        input_data = {
            "CAT_000001_e1_d1": {
                "price": 75.0,
                "author": "Balzac",
                "date": "",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1888-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            },
            "CAT_000002_e1_d1": {
                "price": 75.0,
                "author": "Balzac",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1889-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            }
        }

        output_test = reconciliator(input_data)

        test_dict = {
            "descs_processed": 2,
            "mss_reconciliated": 1,
            "single_sale_count": 0,
            "multiple_sales_count": 2,
            "multiple_sales": [
                {
                    "mss": [
                        {"price": 75.0,
                         "author": "Balzac",
                         "date": "",
                         "number_of_pages": 0.25,
                         "format": 4,
                         "term": 3,
                         "sell_date": "1888-10",
                         "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                         "id": "CAT_000001_e1_d1"
                         },
                        {
                            "price": 75.0,
                            "author": "Balzac",
                            "date": "1847-05",
                            "number_of_pages": 0.25,
                            "format": 4,
                            "term": 3,
                            "sell_date": "1889-10",
                            "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                            "id": "CAT_000002_e1_d1"
                        }
                    ],
                    "scores": [
                        [
                            "CAT_000001_e1_d1",
                            "CAT_000002_e1_d1",
                            0.6
                        ]
                    ]
                }
            ],
            "single_sale": []
        }

        self.assertDictEqual(output_test, test_dict)

    def test_term(self):
        """
        This function checks that if the term is missing/different, there is a clustering.
        """
        input_data = {
            "CAT_000001_e1_d1": {
                "price": 75.0,
                "author": "Balzac",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": "",
                "sell_date": "1888-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            },
            "CAT_000002_e1_d1": {
                "price": 75.0,
                "author": "Balzac",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1889-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            }
        }

        output_test = reconciliator(input_data)

        test_dict = {
            "descs_processed": 2,
            "mss_reconciliated": 1,
            "single_sale_count": 0,
            "multiple_sales_count": 2,
            "multiple_sales": [
                {
                    "mss": [
                        {"price": 75.0,
                         "author": "Balzac",
                         "date": "1847-05",
                         "number_of_pages": 0.25,
                         "format": 4,
                         "term": "",
                         "sell_date": "1888-10",
                         "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                         "id": "CAT_000001_e1_d1"
                         },
                        {
                            "price": 75.0,
                            "author": "Balzac",
                            "date": "1847-05",
                            "number_of_pages": 0.25,
                            "format": 4,
                            "term": 3,
                            "sell_date": "1889-10",
                            "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                            "id": "CAT_000002_e1_d1"
                        }
                    ],
                    "scores": [
                        [
                            "CAT_000001_e1_d1",
                            "CAT_000002_e1_d1",
                            0.7999999999999999
                        ]
                    ]
                }
            ],
            "single_sale": []
        }

        self.assertDictEqual(output_test, test_dict)

    def test_format(self):
        """
        This function checks that if the format is missing/different, there is a clustering.
        """
        input_data = {
            "CAT_000001_e1_d1": {
                "price": 75.0,
                "author": "Balzac",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": "",
                "term": 3,
                "sell_date": "1888-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            },
            "CAT_000002_e1_d1": {
                "price": 75.0,
                "author": "Balzac",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1889-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            }
        }

        output_test = reconciliator(input_data)

        test_dict = {
            "descs_processed": 2,
            "mss_reconciliated": 1,
            "single_sale_count": 0,
            "multiple_sales_count": 2,
            "multiple_sales": [
                {
                    "mss": [
                        {"price": 75.0,
                         "author": "Balzac",
                         "date": "1847-05",
                         "number_of_pages": 0.25,
                         "format": "",
                         "term": 3,
                         "sell_date": "1888-10",
                         "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                         "id": "CAT_000001_e1_d1"
                         },
                        {
                            "price": 75.0,
                            "author": "Balzac",
                            "date": "1847-05",
                            "number_of_pages": 0.25,
                            "format": 4,
                            "term": 3,
                            "sell_date": "1889-10",
                            "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                            "id": "CAT_000002_e1_d1"
                        }
                    ],
                    "scores": [
                        [
                            "CAT_000001_e1_d1",
                            "CAT_000002_e1_d1",
                             0.9
                        ]
                    ]
                }
            ],
            "single_sale": []
        }

        self.assertDictEqual(output_test, test_dict)

    def test_page(self):
        """
        This function checks that if the number of page(s) is missing/different, there is a clustering.
        """
        input_data = {
            "CAT_000001_e1_d1": {
                "price": 75.0,
                "author": "Balzac",
                "date": "1847-05",
                "number_of_pages": None,
                "format": 4,
                "term": 3,
                "sell_date": "1888-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            },
            "CAT_000002_e1_d1": {
                "price": 75.0,
                "author": "Balzac",
                "date": "1847-05",
                "number_of_pages": 0.25,
                "format": 4,
                "term": 3,
                "sell_date": "1889-10",
                "desc": "L. a. s., mai &847, 1/4 de p. in-4"
            }
        }

        output_test = reconciliator(input_data)

        test_dict = {
            "descs_processed": 2,
            "mss_reconciliated": 1,
            "single_sale_count": 0,
            "multiple_sales_count": 2,
            "multiple_sales": [
                {
                    "mss": [
                        {"price": 75.0,
                         "author": "Balzac",
                         "date": "1847-05",
                         "number_of_pages": None,
                         "format": 4,
                         "term": 3,
                         "sell_date": "1888-10",
                         "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                         "id": "CAT_000001_e1_d1"
                         },
                        {
                            "price": 75.0,
                            "author": "Balzac",
                            "date": "1847-05",
                            "number_of_pages": 0.25,
                            "format": 4,
                            "term": 3,
                            "sell_date": "1889-10",
                            "desc": "L. a. s., mai &847, 1/4 de p. in-4",
                            "id": "CAT_000002_e1_d1"
                        }
                    ],
                    "scores": [
                        [
                            "CAT_000001_e1_d1",
                            "CAT_000002_e1_d1",
                            1.0000000000000002
                        ]
                    ]
                }
            ],
            "single_sale": []
        }

        self.assertDictEqual(output_test, test_dict)


# To improve : we need to add more data to test.
#class Evaluating_scores(unittest.TestCase):
#    maxDiff = None
#
#    def test_scores(self):
#        input = "json_test/input.json"
#        actual_path = os.path.dirname(os.path.abspath(__file__))
#        input_json = os.path.join(actual_path, input)
#
#        output = "json_test/output.json"
#        output_json = os.path.join(actual_path, output)
#
#        with open(input_json, 'r') as input:
#            input_to_test = json.load(input)
#        
#            output_test = reconciliator(input_to_test)
#        
#        output = "json_test/output.json"
#        output_json = os.path.join(actual_path, output)
#
#        with open(output_json, 'r') as output:
#            test_dict = json.load(output)
#
#        self.assertDictEqual(output_test, test_dict)


if __name__ == "__main__":
    unittest.main()
