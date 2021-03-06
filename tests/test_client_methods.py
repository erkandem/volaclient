from http import HTTPStatus
import pytest
from datetime import datetime as dt
from volaclient import VolaClient
import settings


class TestVolaClient:
    @classmethod
    def setup_class(cls):
        cls.client = VolaClient()
        cls.client.login_with_api(
            body=dict(
                username=settings.IVOLAPI_TEST_USERNAME,
                password=settings.IVOLAPI_TEST_PASSWORD,
            )
        )
        assert cls.client.LOGIN_TIMESTAMP is not None
        assert cls.client.API_TOKEN is not None

    def test_get_heartbeat_r(self):
        response = self.client.get_heartbeat_r()
        assert response.status == HTTPStatus.OK

    def test_get_user_by_username_r(self):
        """relevant for superusers only"""
        pass

    def test_post_create_user_r(self):
        """relevant for superusers only"""
        pass

    def test_delete_user_by_username_r(self):
        """relevant for superusers only"""
        pass

    def test_post_login_for_access_token_r(self):
        """already tested by logging in for test client"""
        pass

    def test_get_ivol_r(self):
        response = self.client.get_ivol_r(fields_data=dict(symbol='spy'))
        assert response.status == HTTPStatus.OK

    def test_get_atm_ivol_r(self):
        response = self.client.get_ivol_r(fields_data=dict(symbol='spy'))
        assert response.status == HTTPStatus.OK

    def test_get_ivol_smile_r(self):
        response = self.client.get_ivol_smile_r(fields_data=dict(symbol='spy'))
        assert response.status == HTTPStatus.OK

    def test_get_surface_by_delta_r(self):
        response = self.client.get_surface_by_delta_r(fields_data=dict(symbol='spy'))
        assert response.status == HTTPStatus.OK

    def test_get_ivol_calendar_r(self):
        response = self.client.get_ivol_calendar_r(fields_data=dict(symbol='spy'))
        assert response.status == HTTPStatus.OK

    def test_get_ivol_inter_spread_r(self):
        response = self.client.get_ivol_inter_spread_r(fields_data=dict(symbol1='spy', symbol2='qqq'))
        assert response.status == HTTPStatus.OK

    def test_get_intraday_prices_r(self):
        response = self.client.get_intraday_prices_r(fields_data=dict(symbol='spy'))
        assert response.status == HTTPStatus.OK

    def test_get_pvp_intraday_r(self):
        response = self.client.get_pvp_intraday_r(fields_data=dict(symbol='spy'))
        assert response.status == HTTPStatus.OK

    def test_get_continuous_eod_r(self):
        response = self.client.get_continuous_eod_r(fields_data=dict(symbol='cl'))
        assert response.status == HTTPStatus.OK

    def test_get_continuous_eod_spread_r(self):
        response = self.client.get_continuous_eod_spread_r(fields_data=dict(symbol='cl'))
        assert response.status == HTTPStatus.OK

    def test_get_continuous_eod_as_array_r(self):
        response = self.client.get_continuous_eod_as_array_r(fields_data=dict(symbol='cl'))
        assert response.status == HTTPStatus.OK

    def test_get_regular_futures_eod_r(self):
        response = self.client.get_regular_futures_eod_r(
            fields_data=dict(
                symbol='cl',
                month='f',
                year=dt.now().year+1
            ))
        assert response.status == HTTPStatus.OK

    def test_post_raw_option_data_r(self):
        pass

    def test_get_api_info_usts_r(self):
        response = self.client.get_api_info_usts_r()
        assert response.status == HTTPStatus.OK

    def test_get_api_info_exchanges_r(self):
        response = self.client.get_api_info_exchanges_r(fields_data=dict(ust='eqt'))
        assert response.status == HTTPStatus.OK

    def test_get_api_info_symbols_r(self):
        response = self.client.get_api_info_symbols_r(fields_data=dict(ust='eqt', exchange='usetf'))
        assert response.status == HTTPStatus.OK

    def test_get_api_info_ltd_r(self):
        response = self.client.get_api_info_ltd_r(fields_data=dict(symbol='spy', ust='eqt', exchange='usetf'))
        assert response.status == HTTPStatus.OK

    def test_get_api_info_option_month_and_underlying_month_r(self):
        response = self.client.get_api_info_option_month_and_underlying_month_r(fields_data=dict(symbol='cl', ust='fut', exchange='cme', ltd='20201120'))
        assert response.status == HTTPStatus.OK

    def test_get_api_info_first_and_last_r(self):
        response = self.client.get_api_info_first_and_last_r(
            fields_data=dict(
                symbol='cl',
                ust='fut',
                exchange='cme',
                ltd='20201120',
                option_month='202011',
                underlying_month='202101',
            ))
        assert response.status == HTTPStatus.OK

    @pytest.mark.skip(reason="identified and fixed in next release")
    def test_get_api_info_strikes_r(self):
        response = self.client.get_api_info_strikes_r(
            fields_data=dict(
                symbol='cl',
                ust='fut',
                exchange='cme',
                putcall='call',
                ltd='20201120',
                option_month='202011',
                underlying_month='202101',
            ))
        assert response.status == HTTPStatus.OK

    @pytest.mark.skip(reason="identified and fixed in next release")
    def test_post_api_info_strikes_r(self):
        response = self.client.post_api_info_strikes_r(
            body=dict(
                symbol='cl',
                ust='fut',
                exchange='cme',
                putcall='call',
                ltd='20201120',
                option_month='202011',
                underlying_month='202101',
            ))
        assert response.status == HTTPStatus.OK

    def test_get_all_options_single_underlying_single_day_r(self):
        response = self.client.get_all_options_single_underlying_single_day_r(
            fields_data=dict(
                symbol='spy',
                date='2020-12-22',
            )
        )
        assert response.status == HTTPStatus.OK

    def test_post_top_oi_and_volume_r(self):
        response = self.client.post_top_oi_and_volume_r(
            body={
                "ust": "eqt",
                "exchange": "usetf",
                "symbol": "spy",
                "startdate": "2019-01-01",
                "enddate": "2019-04-01",
                "putcall": "call",
                "ltd": "20200117",
                "metric": "oi",
                "dminus": 365,
                "top_n": 5,
                "order": "desc"
            }
        )
        assert response.status == HTTPStatus.OK

    def test_post_delta_data_r(self):
        response = self.client.post_delta_data_r(
            body={
                "ust": "fut",
                "exchange": "cme",
                "symbol": "cl",
                "option_month": "201912",
                "underlying_month": "201912",
                "startdate": "2019-01-01",
                "enddate": "2019-04-01",
                "ltd": "20191115"
            }
        )
        import pdb;pdb.set_trace()
        assert response.status == HTTPStatus.OK

    def test_get_risk_reversal_r(self):
        response = self.client.get_risk_reversal_r(fields_data=dict(symbol='spy'))
        assert response.status == HTTPStatus.OK

    def test_get_ivol_summary_single_r(self):
        response = self.client.get_ivol_summary_single_r(fields_data=dict(symbol='spy'))
        assert response.status == HTTPStatus.OK

    def test_get_ivol_summary_cme_r(self):
        response = self.client.get_ivol_summary_cme_r()
        assert response.status == HTTPStatus.OK

    def test_get_ivol_summary_ice_r(self):
        response = self.client.get_ivol_summary_ice_r()
        assert response.status == HTTPStatus.OK

    def test_get_ivol_summary_usetf_r(self):
        response = self.client.get_ivol_summary_usetf_r()
        assert response.status == HTTPStatus.OK

    def test_get_ivol_summary_eurex_r(self):
        response = self.client.get_ivol_summary_eurex_r()
        assert response.status == HTTPStatus.OK
