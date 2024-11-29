import unittest
from unittest.mock import patch, MagicMock, mock_open
from main import get_group_members_with_birthdays, post_birthday_congratulations


class TestBirthdayBot(unittest.TestCase):


    @patch('main.requests.get')
    def test_get_group_members_with_birthdays(self, mock_get):
        mock_response = {
            "response": {
                "items": [
                    {"id": 1, "first_name": "Ivan", "last_name": "Ivanov", "bdate": "29.11.1990"},
                    {"id": 2, "first_name": "Anna", "last_name": "Petrova", "bdate": "15.05.1988"},
                ]
            }
        }
        mock_get.return_value.json = MagicMock(return_value=mock_response)

        birthdays = get_group_members_with_birthdays()

        self.assertEqual(len(birthdays), 1)
        self.assertEqual(birthdays[0]["name"], "Ivan Ivanov")
        self.assertEqual(birthdays[0]["id"], 1)


    @patch('main.requests.get')
    @patch('main.open', new_callable=mock_open)
    def test_post_birthday_congratulations(self, mock_file, mock_get):
        mock_response_members = [
                    {"id": "1", "name": "Ivan Ivanov", "bdate": "29.11.1990"}
                ]
        mock_response_post = {"response": {"post_id": "test"}}
        mock_get.side_effect = [
            MagicMock(json=MagicMock(return_value=mock_response_members)),
            MagicMock(json=MagicMock(return_value={"response": "OK"}))
        ]

        post_birthday_congratulations(mock_response_members, 0)
        mock_file().write.assert_called_once()

        log_content = mock_file().write.call_args[0][0]
        self.assertIn(str(mock_response_post), log_content)
       


    @patch('main.requests.get')
    @patch('main.open', new_callable=mock_open)
    def test_post_birthday_congratulations_no_birthdays(self, mock_file, mock_get):
        mock_response_members = []
        mock_get.return_value.json = MagicMock(return_value=mock_response_members)

        post_birthday_congratulations(mock_response_members, 0)

        mock_file().write.assert_called()
        self.assertIn("Сегодня именинников нет.", mock_file().write.call_args[0][0])


if __name__ == "__main__":
    unittest.main()


#coverage run -m unittest discover 
# coverage html
