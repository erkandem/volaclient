"""
auto-generated 2020-02-08 18:11:49
... using [swagccg-py2py](https://erkandem.github.io/swagccg-py2py)' version 0.3.3

your module level doc-string goes here
"""

# #######################################################################
# DO NOT MODIFY THIS FILE!
# Your changes will be lost if you rerun ``make_client.py``! 
# Edit the template!
# #######################################################################

from datetime import datetime as dt, timedelta
import json
import urllib
import urllib3
import certifi
import warnings


class VolaClient(object):
    """your client class level doc-string goes here"""

    def __init__(self, deployment='remote'):
        if deployment == 'remote':
            self.API_PORT = '80'
            self.API_URL_BASE = 'api.volsurf.com'
            self.API_PROTOCOL = 'https'
        elif deployment == 'local':
            self.API_PORT = '5000'
            self.API_URL_BASE = '127.0.0.1'
            self.API_PROTOCOL = 'http'

        self.BASE_PATH = ''
        self.LOGIN_TIMESTAMP = None
        self.API_TOKEN = None
        self.REFRESH_TIMESTAMP = None

        self.AUTH_HEADER_NAME = 'Authorization'
        self.AUTH_PREFIX = 'Bearer '  # mind the whitespace
        self.AUTH_TOKEN_KEY = 'access_token'
        self.AUTH_TOKEN_KEY_REFRESH = 'refreshed_token'
        self.REFRESH_KEY = 'token'

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

        self.API_LOGIN_URL = f'{self.API_URL}{self.BASE_PATH}/login'
        self.API_REFRESH_URL = f'{self.API_URL}{self.BASE_PATH}/refresh'
        self.API_BASE_URL = f'{self.API_URL}{self.BASE_PATH}'

    def __dir__(self):
        method_names = [
            'get_heartbeat_r',
            'get_api_users_r',
            'post_add_new_api_user_r',
            'delete_api_user_r',
            'put_change_user_pw_r',
            'get_user_roles_r',
            'put_add_user_role_r',
            'delete_user_role_r',
            'post_api_user_login_r',
            'get_ivol_r',
            'get_atm_ivol_r',
            'get_ivol_smile_r',
            'get_surface_by_delta_r',
            'get_ivol_calendar_r',
            'get_inter_spread_r',
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
    
    def login_with_api(self, *, body, headers=None, **kwargs):
        """
        login with the target API and save the JWT token within the class
        
        Args:
            data: login data externally supplied
            body: data to be sent in body (typically credentials)
            headers: option to supply custom headers if needed
        """
        if headers is None:
            headers = {'Content-Type': 'application/json'}
        else:
            if 'content-type' not in [h.lower() for h in headers]:
                headers['Content-Type'] = 'application/json'
        r = self._do_call(
                method='POST',
                url=self.API_LOGIN_URL,
                headers=headers,
                body=body,
                pass_through=True,
                **kwargs
        )
        if r.status == 200:
            res = json.loads(r.data.decode('utf-8'))
            self.API_TOKEN = res[self.AUTH_TOKEN_KEY]
            self.LOGIN_TIMESTAMP = dt.now()
            self.REFRESH_TIMESTAMP = None
        else:
            print(f'login failed =/: \nstatus:{r.status} \n \nurl {r._request_url}')

    # -----------------------------------------------------------------------
    # ---------- Token Management
    # -----------------------------------------------------------------------

    def is_it_time_to_refresh_the_token(self):
        """
        Return True or False depending on the ``LOGIN_TIMESTAMP`` for the
        first refresh or the ``REFRESH_TIMESTAMP`` if the JWT was already
        refreshed once
        
        expiry is server specific
        """
        if self.REFRESH_TIMESTAMP is None:
            if (self.LOGIN_TIMESTAMP + timedelta(hours=10)) < dt.now():
                self.refresh_the_login()
                return True
            else:
                return False
        else:
            if (self.REFRESH_TIMESTAMP + timedelta(hours=10)) < dt.now():
                self.refresh_the_login()
                return True
            else:
                return False

    def refresh_the_login(self):
        """ server specific refresh routine"""
        encoded_data = json.dumps({'token': self.API_TOKEN}).encode('utf-8')
        r = self.http.request(
                'POST',
                self.API_REFRESH_URL,
                headers={'Content-Type': 'application/json'},
                body=encoded_data
        )
        res = json.loads(r.data.decode('utf-8'))
        self.API_TOKEN = res[self.AUTH_TOKEN_KEY_REFRESH]
        self.REFRESH_TIMESTAMP = dt.now()
    
    def _add_auth_header(self, headers=None):
        """ adds the preconfigured authorization header """
        if headers is None:
            headers = dict()
        headers[self.AUTH_HEADER_NAME] = f'{self.AUTH_PREFIX}{self.API_TOKEN}'
        return headers

    def _do_call(self, method=None, url=None, headers=None, fields=None, body=None, **kwargs):
        """
        A way to separate each resource from the actual request dispatching point
        Response is assumed to be json by default. any other mapping can be hooked here.

        Use ``pass_through = True`` to receive the untouched response object

        Args:
            method (str): HTTP-Method
            url (str): endpoint
            headers (dict): each key:value pair represents one header field:value. Don't nest!
            fields (dict):  each key:value pair will be urlencoded and passed as query string. Don't nest!
            body (dict): will be encoded to JSON and bytes afterwards
                         You can get a urlencoding by setting
                         'Content-Type': 'application/x-www-form-urlencoded'

        """

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
                    is not accounted for in the client.\n If you would like to add it look for:\n\n
                    client_point_of_execution_f to build the logic\n
                    client_encoding_decoding_point_f for handling encoding\n\n
                    -1 (negative one) was returned to avoid a RunTimeError'''
                    warnings.warn(msg)
                    return -1
        else:
            r = self.http.request_encode_url(
                    method=method,
                    url=url,
                    headers=headers,
                    fields=fields
            )
        if kwargs.get('pass_through'):
            return r

        if r.status == 200:
            if len(r.data) > 0:
                return self._decode(r.data)
            else:
                return r.status
        elif r.status == 401:
            self.refresh_the_login()
            return 401
        else:
            return -1
    
    def _encode(self, data, format=None):
        """
        Abstracted encoding point. Mount your custom function.
        Focus here is on built in JSON.

        Args:
            data(): python object
            format(str): json or url

        Returns:
            data_encoded: :func:`json.dumps` and encode from utf-8 to binary

        """
        if type(data) is bytes:
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

    def _decode(self, data):
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
    
    def get_heartbeat_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_api_users_r(self, headers=None, body=None, fields_data=None, **kwargs):
        """ Get Api Users """
        r = self._do_call(
                method='GET',
                url=f'{self.API_BASE_URL}/users',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def post_add_new_api_user_r(self, headers=None, body=None, fields_data=None, **kwargs):
        """ Post Add New Api User """
        r = self._do_call(
                method='POST',
                url=f'{self.API_BASE_URL}/users',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def delete_api_user_r(self, username, headers=None, body=None, fields_data=None, **kwargs):
        """ Delete Api User """
        r = self._do_call(
                method='DELETE',
                url=f'{self.API_BASE_URL}/users/{username}',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def put_change_user_pw_r(self, username, headers=None, body=None, fields_data=None, **kwargs):
        """ Put Change User Pw """
        r = self._do_call(
                method='PUT',
                url=f'{self.API_BASE_URL}/users/{username}/pw',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def get_user_roles_r(self, username, headers=None, body=None, fields_data=None, **kwargs):
        """ Get User Roles """
        r = self._do_call(
                method='GET',
                url=f'{self.API_BASE_URL}/users/{username}/roles',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def put_add_user_role_r(self, username, role, headers=None, body=None, fields_data=None, **kwargs):
        """ Put Add User Role """
        r = self._do_call(
                method='PUT',
                url=f'{self.API_BASE_URL}/users/{username}/roles/{role}',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def delete_user_role_r(self, username, role, headers=None, body=None, fields_data=None, **kwargs):
        """ Delete User Role """
        r = self._do_call(
                method='DELETE',
                url=f'{self.API_BASE_URL}/users/{username}/roles/{role}',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def post_api_user_login_r(self, headers=None, body=None, fields_data=None, **kwargs):
        """ Post Api User Login """
        r = self._do_call(
                method='POST',
                url=f'{self.API_BASE_URL}/login',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def get_ivol_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_atm_ivol_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_ivol_smile_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_surface_by_delta_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_ivol_calendar_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_inter_spread_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_intraday_prices_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_pvp_intraday_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_continuous_eod_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_continuous_eod_spread_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_continuous_eod_as_array_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_regular_futures_eod_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def post_raw_option_data_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_api_info_usts_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_api_info_exchanges_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_api_info_symbols_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_api_info_ltd_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_api_info_option_month_and_underlying_month_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_api_info_first_and_last_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def post_api_info_strikes_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_all_options_single_underlying_single_day_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def post_top_oi_and_volume_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def post_delta_data_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_risk_reversal_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_ivol_summary_single_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_ivol_summary_cme_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_ivol_summary_ice_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_ivol_summary_usetf_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
    
    def get_ivol_summary_eurex_r(self, headers=None, body=None, fields_data=None, **kwargs):
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
