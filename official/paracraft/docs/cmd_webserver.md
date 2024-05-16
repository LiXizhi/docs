<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/webserver`**

**quick ref:**
> /webserver [doc_root_dir] [ip_host] [port]

**description:**

```
start web server at given directory:
@param ip_host: default to all ip addresses. 
@param port: default to 8099
@param doc_root_dir: www web root directory. it can be empty, "default", "test", "admin"
e.g.
	/webserver						start the default NPL/ParaEngine debug server (mostly for client debugging)
	/webserver script/apps/WebServer/test      start your own HTTP server.
	/webserver admin 127.0.0.1 8099   start admin server at given ip and port.
```

<!-- END_AUTOGEN-->
