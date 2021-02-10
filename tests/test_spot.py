from unittest import TestCase

from src.spot import Spot


class TestSpot(TestCase):
    def setUp(self) -> None:
        self.spot = Spot()

    def test_validate_account_info_recvWindow_greater_than_60000(self):
        params = {'recvWindow': 60_001}
        self.assertRaisesRegex(ValueError, 'recvWindow cannot exceed 60_000', self.spot.validate_account_info, params)

    def test_validate_account_info_recvWindow_is_str_and_greater_than_60000(self):
        params = {'recvWindow': '60_001'}
        self.assertRaisesRegex(ValueError, 'recvWindow cannot exceed 60_000', self.spot.validate_account_info, params)

    def test_validate_account_info_locked_free_incorrect_value(self):
        params = {'locked_free': 'G'}
        self.assertRaisesRegex(ValueError, 'locked_free incorrect value. Possible values: L | F | B',
                               self.spot.validate_account_info, params)