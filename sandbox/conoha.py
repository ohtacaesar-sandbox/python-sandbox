import configparser
import json
import pathlib

import requests


def get_config():
  config = configparser.ConfigParser()
  config.read(pathlib.Path("./conoha.ini"))
  config = dict(config.items("conoha"))

  assert 'username' in config
  assert 'password' in config
  assert 'tenant_id' in config

  return config


class Client:
  BASE_HEADERS = {
    "Accept": "application/json"
  }

  def __init__(self, username, password, tenant_id):
    self.username = username
    self.password = password
    self.tenant_id = tenant_id
    self.token = self.fetch_token_and_services(
        self.username, self.password, self.tenant_id
    )

  def fetch_token_and_services(self, username, password, tenant_id):
    payload = {
      "auth": {
        "passwordCredentials": {
          "username": username,
          "password": password,
        }
      }
    }

    if tenant_id:
      payload["auth"]["tenantId"] = tenant_id

    r = requests.post(
        "https://identity.tyo1.conoha.io/v2.0/tokens",
        json.dumps(payload),
        headers=self.BASE_HEADERS,
    )

    assert r.ok
    data = r.json()
    data = data["access"]

    # print(json.dumps(data, indent=2))

    return data["token"]["id"]

  def servers_detail(self):
    url = "https://compute.tyo1.conoha.io/v2/{}/servers/detail".format(
        self.tenant_id)
    headers = dict(self.BASE_HEADERS)
    headers["X-Auth-Token"] = self.token

    r = requests.get(url, headers=headers)
    print(json.dumps(r.json(), indent=2))

  def networks(self, network_id=None):
    url = "https://networking.tyo1.conoha.io/v2.0/networks"
    if network_id: url = url + "/" + network_id
    headers = dict(self.BASE_HEADERS)
    headers["X-Auth-Token"] = self.token

    r = requests.get(url, headers=headers)
    assert r.ok
    return r.json()

  def subnets(self, subnet_id=None):
    url = "https://networking.tyo1.conoha.io/v2.0/subnets"
    if subnet_id: url = url + "/" + subnet_id

    headers = dict(self.BASE_HEADERS)
    headers["X-Auth-Token"] = self.token

    r = requests.get(url, headers=headers)
    assert r.ok
    return r.json()

  def security_groups(self, security_group_id=None):
    url = "https://networking.tyo1.conoha.io/v2.0/security-groups"
    if security_group_id: url = url + "/" + security_group_id

    headers = dict(self.BASE_HEADERS)
    headers["X-Auth-Token"] = self.token

    r = requests.get(url, headers=headers)
    assert r.ok
    return r.json()



import argparse


def main():
  config = get_config()
  client = Client(**config)

  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers()

  def command(f):
    parser = subparsers.add_parser(f.__name__)
    parser.set_defaults(handler=f)
    if hasattr(f, '__args'):
      for args, kwargs in reversed(f.__args):
        parser.add_argument(*args, **kwargs)

    return f

  def argument(*args, **kwargs):
    def _(f):
      if not hasattr(f, '__args'): f.__args = []
      f.__args.append((args, kwargs))
      return f

    return _

  @command
  def servers_detail(args=None):
    data = client.servers_detail()
    print(json.dumps(data, indent=2))

  @command
  @argument("--network-id", required=False)
  def networks(args=None):
    data = client.networks(args.network_id)
    if args.network_id:
      print(json.dumps(data, indent=2))
    else:
      networks = data["networks"]
      for network in networks:
        print(network["id"], network["name"])

  @command
  @argument("--subnet-id", required=False)
  def subnets(args=None):
    data = client.subnets(args.subnet_id)
    if args.subnet_id:
      print(json.dumps(data, indent=2))
    else:
      subnets = data["subnets"]
      for subnet in subnets:
        print(subnet["id"], subnet["cidr"])

  @command
  @argument("--security-group-id", required=False)
  def security_groups(args=None):
    data = client.security_groups(args.security_group_id)
    if args.security_group_id:
      print(json.dumps(data, indent=2))
    else:
      security_groups = data["security_groups"]
      print(json.dumps(security_groups, indent=2))
      #for sg in security_groups:
      #  print(sg["id"], sg["name"])

  args = parser.parse_args()
  if 'handler' in args:
    args.handler(args)


if __name__ == '__main__':
  main()
