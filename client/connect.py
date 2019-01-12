import os
import sys

import docker


if __name__ == "__main__":
  api_key = sys.argv[1]
  api_secret = sys.argv[2]
  problem_id = sys.argv[3]
  destination_location = sys.argv[4]
  client = docker.from_env()

  cpu_count = os.cpu_count() or 1
  if cpu_count >= 2:
    cpu_count = cpu_count // 2
  cpu_set = ','.join(map(str, range(cpu_count)))

  environments = {
    "KEY": api_key,
    "SECRET": api_secret,
    "PROBLEM_ID": problem_id
  }

  ulimits = [docker.types.Ulimit(name="STACK", soft=1048576, hard=1048576)]

  logs = client.containers.run("polygon-package-downloader:v1",
                               cpuset_cpus=cpu_set,
                               environment=environments,
                               mem_limit="4g",
                               pids_limit=65535,
                               ulimits=ulimits,
                               volumes={destination_location: {"bind": "/store", "mode": "rw"}})

  with open(os.path.join(destination_location, "logs/docker.log"), "wb") as f:
    f.write(logs)
