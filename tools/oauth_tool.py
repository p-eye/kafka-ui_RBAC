import jwt
import streamlit as st
import string
import random
import requests
from urllib.parse import urlencode

class OAuth:
    def __init__(self):
        self.SECRET_KEY = 'oauth'

    @st.cache_resource(ttl=86400)
    def jwks_client(_self, jwks_uri):
        return jwt.PyJWKClient(jwks_uri)
    
    def random_state_generator(self, size):
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    def validate_token(self, token, config) -> (bool, str):
        try:
            signing_key = self.jwks_client(config['jwks_uri']).get_signing_key_from_jwt(token['id_token'])
            data = jwt.decode(
                token['id_token'], 
                signing_key.key, 
                algorithms=["RS256"], 
                audience=config['audience'] if 'audience' in config else None
                )
        except (jwt.exceptions.ExpiredSignatureError):
            return False, 'Expired Token'
        except:
            return False, 'Invalid Token'
        return True, data[config['identity_field_in_token']] if 'identity_field_in_token' in config and config['identity_field_in_token'] in data else 'OK'

    def request_token(self, config, label):
        if 'code' in st.experimental_get_query_params():
            code = st.experimental_get_query_params()['code'][0]
            state = st.experimental_get_query_params()['state'][0]
            self.remove_query_params(state)
            token_headers = {'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
            token_data = {
                    'grant_type': 'authorization_code', 
                    'redirect_uri': config['redirect_uri'],
                    'client_id': config['client_id'],
                    'client_secret': config['client_secret'],
                    'scope': config['scope'],
                    'state': state,
                    'code': code,
                    }
            try:
                ret = requests.post(config["token_endpoint"], headers=token_headers, data=urlencode(token_data).encode("utf-8"))
                ret.raise_for_status()
            except requests.exceptions.RequestException as e:
                st.error(e)
                st.stop()
            return ret.json()
        else:
            return None

    def read_config(self):
        config = st.secrets[self.SECRET_KEY]
        required_config_options = ['authorization_endpoint',
                                   'token_endpoint',
                                   'jwks_uri',
                                   'redirect_uri',
                                   'client_id',
                                   'client_secret',
                                   'scope' ]
        is_valid: bool = all([k in config for k in required_config_options])
        if not is_valid:
            st.error("Invalid OAuth Configuration")
            st.stop()
        return config
    
    def create_auth_request_url(self, config):
        state_parameter = self.random_state_generator(15)
        query_params = urlencode({
            'redirect_uri': config['redirect_uri'], 
            'client_id': config['client_id'], 
            'response_type': 'code', 
            'state': state_parameter, 
            'scope': config['scope'],
            })
        request_url = f"{config['authorization_endpoint']}?{query_params}"
        # if st.experimental_get_query_params():
        #     qpcache = self.query_parms_cache(state_parameter)
        #     qpcache = st.experimental_get_query_params()
        return request_url
    
    @st.cache_resource(ttl=300)
    def query_parms_cache(_self, key):
        return {}
    
    def remove_query_params(self, state):
        qpcache = self.query_parms_cache(state)
        qparms = qpcache
        qpcache = {}
        st.experimental_set_query_params(**qparms)