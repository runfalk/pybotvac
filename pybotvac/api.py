import hashlib
import hmac
import itertools
import requests

from email.utils import formatdate
from requests.auth import AuthBase
from requests_oauthlib import OAuth2Session

from ._compat import ustr


__all__ = [
    "Beehive",
    "Nucleo",
]


class NucleoAuth(AuthBase):
    def __init__(self, serial, secret):
        self.serial = serial

        if isinstance(secret, ustr):
            secret = secret.encode("utf-8")
        self.secret = secret

    def _sign(self, msg):
        if isinstance(msg, ustr):
            msg = msg.encode("utf-8")
        return hmac.new(self.secret, msg, hashlib.sha256).hexdigest()

    def __call__(self, request):
        timestamp = formatdate(timeval=None, localtime=False, usegmt=True)

        signature = self._sign(u"\n".join([
            self.serial.lower(),
            timestamp,
            request.body,
        ]))

        request.headers["Accept"] = "application/vnd.neato.nucleo.v1"
        request.headers["X-Date"] = timestamp
        request.headers["Authorization"] = "NEATOAPP {}".format(signature)

        return request


class Nucleo(object):
    def __init__(self, serial, secret):
        self._counter = itertools.count()
        self.session = requests.Session()
        self.session.auth = NucleoAuth(serial, secret)

    def __call__(self, msg):
        data = {"reqId": next(self._counter)}
        data.update(msg)

        url = "https://nucleo.neatocloud.com:4443/vendors/neato/robots/{serial}/messages"
        req = self.session.post(
            url.format(serial=self.session.auth.serial),
            json=data)
        return req.json()


class Beehive(OAuth2Session):
    def __init__(
            self, client_id=None, client=None, auto_refresh_url=None,
            auto_refresh_kwargs=None, scope=None, redirect_uri=None,
            token=None, state=None, token_updater=None, client_secret=None,
            **kwargs):
        if client_secret is None:
            raise ValueError("No client secret provided")
        self.client_secret = client_secret

        if auto_refresh_url is None:
            auto_refresh_url = "https://beehive.neatocloud.com/oauth2/token"

        if auto_refresh_kwargs is None:
            auto_refresh_kwargs = {"client_secret": client_secret}

        if state is None:
            state = ["public_profile", "control_robots", "maps"]

        super(Beehive, self).__init__(
            client_id, client, auto_refresh_url, auto_refresh_kwargs, scope,
            redirect_uri, token, state, token_updater, **kwargs)

    def authorization_url(self, url=None, state=None, **kwargs):
        if url is None:
            url = "https://apps.neatorobotics.com/oauth2/authorize"
        return super(Beehive, self).authorization_url(url, state, **kwargs)

    def fetch_token(
            self, token_url=None, code=None, authorization_response=None,
            body='', auth=None, username=None, password=None, method='POST',
            timeout=None, headers=None, verify=True, proxies=None,
            client_secret=None, **kwargs):
        if token_url is None:
            token_url = "https://beehive.neatocloud.com/oauth2/token"

        if client_secret is None:
            client_secret = self.client_secret

        return super(Beehive, self).fetch_token(
            token_url, code, authorization_response, body, auth, username,
            password, method, timeout, headers, verify, proxies, client_secret,
            **kwargs)

    def request(
            self, method, url, data=None, headers=None, withhold_token=False,
            client_id=None, client_secret=None, **kwargs):
        if url.startswith("/"):
            url = "https://beehive.neatocloud.com{}".format(url)
        return super(Beehive, self).request(
            method, url, data, headers, withhold_token, client_id,
            client_secret, **kwargs)

