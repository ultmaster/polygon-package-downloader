#!/usr/bin/env python3

import os
import sys

import docker


if __name__ == "__main__":
  if len(sys.argv) >= 5:
    api_key = sys.argv[1]
    api_secret = sys.argv[2]
    problem_id = sys.argv[3]
    destination_location = sys.argv[4]
    environments = {
      "KEY": api_key,
      "SECRET": api_secret,
      "PROBLEM_ID": problem_id
    }
  else:
    destination_location = sys.argv[1]
    environments = {"NON_FETCH": "1"}

  client = docker.from_env()
  logs = client.containers.run("registry.cn-hangzhou.aliyuncs.com/ultmaster/polygon-package-downloader:latest",
                               environment=environments,
                               volumes={destination_location: {"bind": "/store", "mode": "rw"}})

  with open(os.path.join(destination_location, "logs/docker.log"), "wb") as f:
    f.write(logs)
