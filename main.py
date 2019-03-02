import os
import stat
import subprocess
from xml.etree import ElementTree
from zipfile import ZipFile

from compiler import compile
from logger import logger

PACKAGE_ZIP = "store/package.zip"


def run_package():
  with ZipFile(PACKAGE_ZIP) as zipFile:
    zipFile.extractall("store/package")
  os.chdir("store/package")
  for top, dirs, files in os.walk("."):
    for file in files:
      if file.endswith(".sh"):
        path = os.path.join(top, file)
        os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)
  problem_node = ElementTree.parse("problem.xml")
  for element in problem_node.iter():
    source, binary = element.find("source"), element.find("binary")
    if source is not None and binary is not None:
      source_file = source.attrib["path"]
      binary_file = binary.attrib["path"]
      language = source.attrib["type"]
      logger.info("compiling %s -> %s (%s)" % (source_file, binary_file, language))
      assert compile(language, source_file, binary_file)
  with open("../logs/stdout.log", "a") as stdout, \
      open("../logs/stderr.log", "a") as stderr:
    subprocess.run(["./doall.sh"], stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                   timeout=time_limit, check=True)


if __name__ == "__main__":
  time_limit = float(os.environ.get("TIME_LIMIT", 3600))
  logger.debug(os.environ)
  run_package()
