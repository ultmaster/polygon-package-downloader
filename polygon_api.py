import hashlib
import random
import string
import sys
import time
from abc import abstractmethod

import requests

from logger import logger


class DefaultHandler():
  @abstractmethod
  def handle(self, request):
    pass


class JsonHandler(DefaultHandler):
  def handle(self, request):
    data = request.json()
    if data["status"] != "OK":
      logger.error(data.get("comment", ""))
      sys.exit(1)
    return data["result"]


class BinaryFileHandler(DefaultHandler):
  def __init__(self, destination):
    self.destination = destination

  def handle(self, request):
    with open(self.destination, "wb") as f:
      for chunk in request:
        f.write(chunk)


class PolygonAPI:

  def __init__(self, key, secret, proxy):
    self.key = key
    self.secret = secret
    self.proxy = proxy

  def get(self, methodName, handler: DefaultHandler, **params):
    request_address = "https://polygon.codeforces.com/api/{methodName}".format(methodName=methodName)
    params["apiKey"] = self.key
    params["time"] = int(time.time())
    params["apiSig"] = self._get_sig(methodName, params)
    proxies = {"https": self.proxy} if self.proxy else None
    r = requests.get(request_address, params=params, proxies=proxies)
    return handler.handle(r)

  def _get_sig(self, methodName, params):
    rand_str = ''.join([random.choice(string.ascii_lowercase) for _ in range(6)])
    params_str = '&'.join(['%s=%s' % s for s in sorted(params.items())])
    sig_str = rand_str + '/' + methodName + '?' + params_str + '#' + self.secret
    logger.debug(sig_str)
    return rand_str + hashlib.sha512(sig_str.encode()).hexdigest()
