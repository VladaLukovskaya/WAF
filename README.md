# WAF

# What is it

It is a simple Web Application Firewall (WAF) based on Flask that can protect a simple WEB application from SQL injections.


# How to use it

Install requirements

```
pip3 install -r requirements.txt
```

Edit the config file `settings.yml`

- `waf_port` - port for the WAF
- `app_url` - url of base application
- `check_output` - enable or disable check output mode
- `logfile` - path for log files

Run the WAF

```
python3 proxy.py
```

Run the app

```
python3 app.py
```

# Rules

Path - `rules/`

A rule example

```
100001:
  name: "SQL Injection"
  description: "the simplest sql attack"
  body: ["'or"]
```

A rule format

- `name` - short name of rule
- `description`- description of rule
- `body` - list of strings that will be searched in body of http requests
- `header` - list for search in header of http request

# Output rules

`check_output` argument for enable detect signatures in output traffic (by default `false`)

```

A rule format

- `name` - short name of rule
- `description`- description of rule
- `data` - list of strings that will be searched in http response

A rule example

```
200001:
  name: "linux users creds"
  description: "Linux remote execution cat /etc/passwd"
  data: ["sshd:x:123:65555::/run/sshd:/usr/sbin/nologin"]
