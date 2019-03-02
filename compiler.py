import subprocess


def compile(type, source, binary):
  if type == "c.gcc":
    command = ["/usr/bin/gcc", "-DONLINE_JUDGE", "-O2", "-lm", "-o", binary, source]
  elif type.startswith("cpp.g++"):
    std = "98"
    if type[-2:].isdigit():
      std = type[-2:]
    command = ["/usr/bin/g++", "-DONLINE_JUDGE", "-O2", "-lm", "-std=c++" + std, "-o", binary, source]
  else:
    return True
  subprocess.check_call(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
  return True
