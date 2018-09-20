'''
EBAPI.py
(External Bitcoin API)
BlockChain.Info Json RPC Object.
Author: J
Version: Python3
Usage: client = External_Bitcoin_Chain()
client.method(args)
'''

import json
import hmac
import hashlib
import time
import requests
import base64
import pickle


class BlockChainError():
   def __init__(self, exception):
    print('We Have An Error!')
    try:
     error_log = pickle.load(open('EBAPI-Error.log','rb'))
     error_log['Error Number'] += 1
     error_log[error_log['Error Number']] = str(exception)
     pickle.dump(error_log,open('EBAPI-Error.log','wb'))
     print('Stored Error Number [{0}]: [{1}].'.format(error_log['Error Number'],exception))
     print('We Are Paused For Error Examination. Press [ENTER] To Try To Ressume.')
     paused = input('>>: ')
    except Exception as Pickle_Db_Needed:
     print('New Pickle Database Required Building Now.')
     error_log = dict()
     error_log['Error Number'] = 0
     error_log[error_log['Error Number']] = str(exception)
     error_log['Error Number'] += 1
     error_log[error_log['Error Number']] = str(exception)
     pickle.dump(error_log,open('EBAPI-Error.log','wb'))
     print('Stored Error Number [{0}]: [{1}].'.format(error_log['Error Number'],exception))
     print('We Are Paused For Error Examination. Press [ENTER] To Try To Ressume.')
     paused = input('>>: ')


class BaseClient(object):
    """
    A base class for the API Client methods that handles interaction with
    the requests library.
    """
    api_url = 'https://blockchain.info/'
    exception_on_error = True

    def __init__(self, proxydict=None, *args, **kwargs):
        self.proxydict = proxydict

    def _get(self, *args, **kwargs):
        """
        Make a GET request.
        """
        return self._request(requests.get, *args, **kwargs)

    def _post(self, *args, **kwargs):
        """
        Make a POST request.
        """
        data = self._default_data()
        data.update(kwargs.get('data') or {})
        kwargs['data'] = data
        return self._request(requests.post, *args, **kwargs)

    def _default_data(self):
        """
        Default data for a POST request.
        """
        return {}

    def _request(self, func, url, *args, **kwargs):
        """
        Make a generic request, adding in any proxy defined by the instance.

        Raises a ``requests.HTTPError`` if the response status isn't 200, and
        raises a :class:`BlockChainError` if the response contains a json encoded
        error message.
        """
        return_json = kwargs.pop('return_json', False)
        url = self.api_url + url
        response = func(url, *args, **kwargs)

        if 'proxies' not in kwargs:
            kwargs['proxies'] = self.proxydict
            

        # Check for error, raising an exception if appropriate.
        response.raise_for_status()

        try:
            json_response = response.json()
        except ValueError:
            json_response = None
        if isinstance(json_response, dict):
            error = json_response.get('error')
            if error:
                raise BlockChainError(error)

        if return_json:
            if json_response is None:
                raise BlockChainError(
                    "Could not decode json for: " + response.text)
            return json_response

        return response

class External_Bitcoin_Chain(BaseClient):
    def get_address(self, address):
      ''' Returns Address Information Via Json RPC '''
      return self._get('rawaddr/'+str(address), return_json=True)

    def get_block(self, tx):
      ''' Returns Block Based On Tx Givin '''
      return self._get('block/'+str(tx), return_json=True)

    def get_tx(self, tx):
      ''' Returns Tx.ID Data '''
      return self._get('rawtx/'+str(tx), return_json=True)
    
    
