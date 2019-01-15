import os
import stat
import subprocess
import sys
from zipfile import ZipFile

from logger import logger
from polygon_api import PolygonAPI, JsonHandler, BinaryFileHandler

PACKAGE_ZIP = "store/package.zip"


def fetch_package(problem_id):
  api = PolygonAPI(api_key, api_secret, proxy)
  json_handler = JsonHandler()
  file_handler = BinaryFileHandler(PACKAGE_ZIP)
  revision_packages = api.get("problem.packages", json_handler, problemId=problem_id)
  latest_revision_num, package_id = 0, 0
  for package in revision_packages:
    if package["state"] == "READY" and "verification" in package["comment"] and \
        package["revision"] > latest_revision_num:
      latest_revision_num = package["revision"]
      package_id = package["id"]
  logger.debug(package_id)
  if not package_id:
    logger.error("No package with verification found.")
    sys.exit(1)
  api.get("problem.package", file_handler, problemId=problem_id, packageId=package_id)


def run_package():
  with ZipFile(PACKAGE_ZIP) as zipFile:
    zipFile.extractall("store/package")
  os.chdir("store/package")
  for top, dirs, files in os.walk("."):
    for file in files:
      if file.endswith(".sh"):
        path = os.path.join(top, file)
        os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)
  with open("../logs/stdout.log", "a") as stdout, \
      open("../logs/stderr.log", "a") as stderr:
    subprocess.run(["./doall.sh"], stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                   timeout=time_limit, check=True)


if __name__ == "__main__":
  api_key = os.environ["KEY"]
  api_secret = os.environ["SECRET"]
  problem_id = os.environ.get("PROBLEM_ID", "")
  time_limit = float(os.environ.get("TIME_LIMIT", 3600))

  del os.environ["KEY"]
  del os.environ["SECRET"]
  del os.environ["PROBLEM_ID"]
  logger.debug(os.environ)

  proxy = os.environ.get("PROXY", "")
  if "NON_FETCH" not in os.environ:
    fetch_package(problem_id)
  run_package()
