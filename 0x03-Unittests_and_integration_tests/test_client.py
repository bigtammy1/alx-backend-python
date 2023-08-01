#!/usr/bin/env python3
"""Test for githuborgclient class methods"""
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock, PropertyMock
from utils import access_nested_map, get_json, memoize
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """class inheriting unittest for githuborg class"""
    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch("client.get_json")
    def test_org(self, test_orgname, mock_getjson):
        """tests get_json for org details"""
        url = "https://api.github.com/orgs/{}".format(test_orgname)
        example = GithubOrgClient(test_orgname)
        example.org()
        mock_getjson.assert_called_once_with(url)

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google"})
     ])
    def test_public_repos_url(self, test_org, response):
        """test with the property get mock method"""
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as tester:
            tester.return_value = response
            example = GithubOrgClient(test_org)._public_repos_url
            self.assertEqual(example, response.get("repos_url"))

    @patch("client.get_json")
    def test_public_repos(self, mocked_getjson):
        """return a few dict for getjson"""
        payload = [{"name": "Thirsty"}, {"name": "Hungry"}]
        mocked_getjson.return_value = payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as testit:
            testit.return_value = "https://api.github.com/orgs/google"
            example = GithubOrgClient('test').public_repos()
            self.assertEqual(example, ["Thirsty", "Hungry"])
            testit.assert_called_once()
            mocked_getjson.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
        ])
    def test_has_license(self, test_dict, test_key, test_result):
        """test has license with parameters"""
        example = GithubOrgClient.has_license(test_dict, test_key)
        self.assertEqual(example, test_result)


@parameterized_class(['org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'], TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test"""
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('requests.get', side_effect=[
            cls.org_payload, cls.repos_payload
        ])
        cls.mocked_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        """test public repos """

    def test_public_repos_with_license(self):
        """test public with license"""


if __name__ == '__main__':
    unittest.main()
