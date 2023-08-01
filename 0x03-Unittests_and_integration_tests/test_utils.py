#!/usr/bin/env python3
"""unit test for utils.access_nested_map"""
import unittest
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from unittest.mock import Mock, patch


class TestAccessNestedMap(unittest.TestCase):
    """class that inherits from unittest testcase"""
    def setUp(self):
        """method invoked for each test"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {'b': 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
        ])
    def test_access_nested_map(self, nested_map, path, result):
        """test that it returns what it should"""
        self.assertEqual(access_nested_map(nested_map, path), result)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
        ])
    def test_access_nested_map_exception(self, nested_map, path):
        """raise key errors for these inputs"""
        with self.assertRaises(KeyError):
            (access_nested_map(nested_map, path))


class TestGetJson(unittest.TestCase):
    """Tests the get json method"""
    def setUp(self):
        """method called for every test"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
        ])
    def test_get_json(self, test_url, test_payload):
        """tests with mock response"""
        class Mocked(Mock):
            """
            class that inherits from Mock
            """

            def json(self):
                """
                json returning a payload
                """
                return test_payload

        with patch("requests.get") as MockClass:
            MockClass.return_value = Mocked()
            self.assertEqual(get_json(test_url), test_payload)


class TestMemoize(unittest.TestCase):
    """Tests the memoize function"""
    def test_memoize(self):
        """test function"""
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mocked:
            spec = TestClass()
            spec.a_property
            spec.a_property
            mocked.assert_called_once()
