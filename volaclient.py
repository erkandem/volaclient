"""
auto-generated 2020-12-27 19:08:15
... using [swagccg-py2py](https://erkandem.github.io/swagccg-py2py)' version 0.4.0

your module level doc-string goes here
"""

# #######################################################################
# DO NOT MODIFY THIS FILE!
# Your changes will be lost if you rerun ``make_client.py``!
# Edit the template!
# #######################################################################

from datetime import datetime as dt
import json
import typing as t
import urllib
import urllib3
from urllib3.response import HTTPResponse
import certifi

JSONEncodable = t.Union[t.List[t.Any], t.Dict[str, t.Any]]


class VolaClient(object):
    """your client class level doc-string goes here"""

    def __init__(self, deployment: str = 'remote', base_path: str = None):
        if deployment == 'remote':
            self.API_PORT = '80'
            self.API_URL_BASE = 'api.volsurf.com'
            self.API_PROTOCOL = 'https'
        elif deployment == 'local':
            self.API_PORT = '5000'
            self.API_URL_BASE = '127.0.0.1'
            self.API_PROTOCOL = 'http'

        self.BASE_PATH = ''
        if base_path:
            self.BASE_PATH = base_path

        self.LOGIN_TIMESTAMP = None
        self.API_TOKEN = None

        self.AUTH_HEADER_NAME = 'Authorization'
        self.AUTH_PREFIX = 'Bearer '  # mind the whitespace
        self.AUTH_TOKEN_KEY = 'access_token'

        if self.API_PORT == '80':
            self.API_URL = f'{self.API_PROTOCOL}://{self.API_URL_BASE}'
        else:
            self.API_URL = f'{self.API_PROTOCOL}://{self.API_URL_BASE}:{self.API_PORT}'

        if self.API_PROTOCOL == 'https':
            self.http = urllib3.PoolManager(
                cert_reqs='CERT_REQUIRED',
                ca_certs=certifi.where()
            )
        else:
            self.http = urllib3.PoolManager()

        self.API_LOGIN_URL = f'{self.API_URL}{self.BASE_PATH}/token'
        self.API_BASE_URL = f'{self.API_URL}{self.BASE_PATH}'

    def __dir__(self) -> t.List[str]:
        method_names = [
            'get_heartbeat_r',
            'get_user_by_username_r',
            'post_create_user_r',
            'delete_user_by_username_r',
            'post_login_for_access_token_r',
            'get_ivol_r',
            'get_atm_ivol_r',
            'get_ivol_smile_r',
            'get_surface_by_delta_r',
            'get_ivol_calendar_r',
            'get_ivol_inter_spread_r',
            'get_intraday_prices_r',
            'get_pvp_intraday_r',
            'get_continuous_eod_r',
            'get_continuous_eod_spread_r',
            'get_continuous_eod_as_array_r',
            'get_regular_futures_eod_r',
            'post_raw_option_data_r',
            'get_api_info_usts_r',
            'get_api_info_exchanges_r',
            'get_api_info_symbols_r',
            'get_api_info_ltd_r',
            'get_api_info_option_month_and_underlying_month_r',
            'get_api_info_first_and_last_r',
            'get_api_info_strikes_r',
            'post_api_info_strikes_r',
            'get_all_options_single_underlying_single_day_r',
            'post_top_oi_and_volume_r',
            'post_delta_data_r',
            'get_risk_reversal_r',
            'get_ivol_summary_single_r',
            'get_ivol_summary_cme_r',
            'get_ivol_summary_ice_r',
            'get_ivol_summary_usetf_r',
            'get_ivol_summary_eurex_r'
        ]
        return method_names

    def login_with_api(
            self,
            *,
            body,
            headers: t.Dict[str, t.Any] = None,
            **kwargs: t.Dict[str, t.Any],
    ):
        """
        login with the target API and save the JWT token within the class

        Args:
            data: login data externally supplied
            body: data to be sent in body (typically credentials)
            headers: option to supply custom headers if needed
        """
        if headers is None:
            headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        r = self._do_call(
            method='POST',
            url=self.API_LOGIN_URL,
            headers=headers,
            body=body,
            **kwargs
        )
        if r.status == 200:
            res = json.loads(r.data.decode('utf-8'))
            self.API_TOKEN = res[self.AUTH_TOKEN_KEY]
            self.LOGIN_TIMESTAMP = dt.now()
        else:
            print(f'login failed \nstatus:{r.status} \n \nurl: {self.API_LOGIN_URL}'
                  '\nIs the username and password correct?')

    def _add_auth_header(
            self,
            headers: t.Union[None, t.Dict[str, t.Any]] = None,
    ) -> t.Dict[str, t.Any]:
        """ adds the preconfigured authorization header """
        if headers is None:
            headers = {}
        headers[self.AUTH_HEADER_NAME] = f'{self.AUTH_PREFIX}{self.API_TOKEN}'
        return headers

    def _do_call(
            self,
            method: str = None,
            url: str = None,
            headers: t.Dict[str, str] = None,
            fields: t.Dict[str, t.Any] = None,
            body: JSONEncodable = None,
            **kwargs: t.Dict[str, t.Any],
    ) -> HTTPResponse:
        """
        A way to separate each resource from the actual request dispatching point
        Response is assumed to be json by default.
        Good point to add hooks.

        Args:
            method (str): HTTP-Method
            url (str): endpoint
            headers (dict): each key:value pair represents one header field:value. Don't nest!
            fields (dict):  each key:value pair will be urlencoded and passed as query string. Don't nest!
            body (dict): will be encoded to JSON and bytes afterwards
                         You can get a urlencoding by setting
                         'Content-Type': 'application/x-www-form-urlencoded'

        """
        r = HTTPResponse()
        headers = self._add_auth_header(headers)
        if body is not None and method in ['POST', 'PUT', 'PATCH']:
            if 'Content-Type' not in headers:
                headers['Content-Type'] = 'application/json'
                r = self.http.request(
                    method=method,
                    url=url,
                    body=self._encode(body),
                    headers=headers
                )
            else:
                if headers['Content-Type'] == 'application/x-www-form-urlencoded':
                    r = self.http.urlopen(
                        method,
                        url,
                        body=self._encode(body, 'url'),
                        headers=headers
                    )
                elif headers['Content-Type'] == 'application/json':
                    r = self.http.request(
                        method=method,
                        url=url,
                        body=self._encode(body),
                        headers=headers
                    )
                else:
                    msg = f''' The Content-Type header was set to {headers['Content-Type']}\n
                    However, anything else than 'application/json' or 'application/x-www-form-urlencoded'\n
                    is not accounted for in the client.\n If you would like to add it, look for:\n\n
                    "_do_call" to hook the logic\n
                    client_encoding_decoding_point_f for handling encoding\n\n
                    '''
                    raise NotImplementedError(msg)
        else:
            r = self.http.request_encode_url(
                method=method,
                url=url,
                headers=headers,
                fields=fields
            )
        return r

    def _encode(self, data, format: str = None) -> bytes:
        """
        Abstracted encoding point. Mount your custom function.
        Main focus here is on building a JSON or URL/"percent" encoded bytes.

        Args:
            data(): python object
            format(str): `json` or `url`

        Returns:
            data_encoded: :func:`json.dumps` and encode from utf-8 to binary

        """
        if isinstance(data, bytes):
            return data
        if format == 'url':
            return (urllib.parse.urlencode(data)).encode('utf-8')
        if format is None:
            return (json.dumps(data)).encode('utf-8')
        elif format == 'json':
            return (json.dumps(data)).encode('utf-8')
        else:
            msg = f"received format = {format}.\nUse 'json' or 'url'.\n 'json' is default."
            raise NotImplementedError(msg)

    def _decode(self, data: bytes):
        """
        abstracted decoding point
        Mount your custom function. Focus here is on JSON.

        Args:
            data: python object (dict, list, ...)

        Returns:
           data_decoded: first decode from binary to utf-8 and parse with
                         built-in :func:`json.loads`
        """

        return json.loads(data.decode('utf-8'))

    def get_heartbeat_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Get Heartbeat """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/heartbeat',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_user_by_username_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Get User By Username """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/users/',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def post_create_user_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Post Create User """
        r = self._do_call(
            method='POST',
            url=f'{self.API_BASE_URL}/users/',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def delete_user_by_username_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Delete User By Username """
        r = self._do_call(
            method='DELETE',
            url=f'{self.API_BASE_URL}/users/',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def post_login_for_access_token_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Post Login For Access Token """
        if headers is None:
            headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        r = self._do_call(
            method='POST',
            url=f'{self.API_BASE_URL}/token',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_ivol_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Get implied volatility data for a single delta and single tte """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/ivol',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_atm_ivol_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Get ATM implied volatility data """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/ivol/atm',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_ivol_smile_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ smile """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/ivol/smile',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_surface_by_delta_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ returns a surface parameterized by delta and constant time """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/ivol/surface',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_ivol_calendar_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Calculate the spread between different expiries """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/ivol/calendar',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_ivol_inter_spread_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ get ivol spread between options with different underlying """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/ivol/inter-spread',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_intraday_prices_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Get Intraday Prices """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/prices/intraday',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_pvp_intraday_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ price volume profile. histogram of intraday price data """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/prices/intraday/pvp',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_continuous_eod_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Get Conti Eod """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/prices/eod/conti',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_continuous_eod_spread_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Get Continuous Eod Spread """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/prices/eod/conti/spread',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_continuous_eod_as_array_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Get Continuous Eod As Array """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/prices/eod/conti/array',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_regular_futures_eod_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Get Regular Futures Eod """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/prices/eod',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def post_raw_option_data_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Post Raw Option Data """
        r = self._do_call(
            method='POST',
            url=f'{self.API_BASE_URL}/option-data',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_api_info_usts_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Get Api Info Usts """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/info/usts',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_api_info_exchanges_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Get Api Info Exchanges """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/info/exchanges',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_api_info_symbols_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Get Api Info Symbols """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/info/symbols',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_api_info_ltd_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Get Api Info Ltd """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/info/last-trading-days',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_api_info_option_month_and_underlying_month_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Get Api Info Option Month And Underlying Month """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/info/option-month-and-underlying-month',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_api_info_first_and_last_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Get Api Info First And Last """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/info/first-and-last',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_api_info_strikes_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Get Api Info Strikes """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/info/strikes',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def post_api_info_strikes_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Post Api Info Strikes """
        r = self._do_call(
            method='POST',
            url=f'{self.API_BASE_URL}/info/strikes',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_all_options_single_underlying_single_day_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Returns all options for one underlying for one (business)day """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/option-data/single-underlying-single-day',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def post_top_oi_and_volume_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Post Top Oi And Volume """
        r = self._do_call(
            method='POST',
            url=f'{self.API_BASE_URL}/top-oi-and-volume',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def post_delta_data_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Post Delta Data """
        r = self._do_call(
            method='POST',
            url=f'{self.API_BASE_URL}/delta-contour',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_risk_reversal_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ Get the risk reversal of fitted implied volatility data """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/ivol/risk-reversal',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_ivol_summary_single_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ get min, max, std, average and weekly data points """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/ivol/summary/single',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_ivol_summary_cme_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ get min, max, std, average and weekly data points for symbols on CME """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/ivol/summary/cme',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_ivol_summary_ice_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ get min, max, std, average and weekly data points for sybmols on ICE """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/ivol/summary/ice',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_ivol_summary_usetf_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ get min, max, std, average and weekly data points for US ETFs """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/ivol/summary/usetf',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r

    def get_ivol_summary_eurex_r(
            self,

            headers: t.Dict[str, str] = None,
            body: JSONEncodable = None,
            fields_data: t.Dict[str, str] = None,
            **kwargs
    ):
        """ get min, max, std, average and weekly data points for symbols on EUREX """
        r = self._do_call(
            method='GET',
            url=f'{self.API_BASE_URL}/ivol/summary/eurex',
            headers=headers,
            body=body,
            fields=fields_data,
            **kwargs
        )
        return r
