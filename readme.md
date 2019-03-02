This is actually a runner for Linux platform for Codeforces Polygon package.

It will search for all the executables (written in C/C++) referenced in `problem.xml` and recompile for Linux platform, then run `doall.sh`.

The typical usage is like this:

* Download the standard package and save as `package.zip` in `destination_location`, then
* Run:

```
logs = client.containers.run("registry.cn-hangzhou.aliyuncs.com/ultmaster/polygon-package-downloader:latest",
                           environment=environments, network_mode="none",
                           volumes={destination_location: {"bind": "/store", "mode": "rw"}})
```

Of course you need to pull the standard package from Polygon first. See eoj3 for details.
