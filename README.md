# WAF

# How to use it

Install requirements

```
pip3 install -r requirements.txt
```

Edit config file `settings.yml`

- `waf_port` - port for web application firewall
- `app_url` - url of base application
- `check_output` - enable or disable check output mode
- `logfile` - path for log files

Run waf

```
python3 proxy.py
```

Run app

```
python3 app.py
```

# Rules

Path of rules - `rules/`

Rule example

```
100001:
  name: "SQL Injection"
  description: "the simplest sql attack"
  body: ["'or"]
```

Rule format

- `name` - short name of rule
- `description`- description of rule
- `body` - list of strings that will be searched in body of http requests
- `header` - list for search in header of http request

# Output rules

`check_output` argument for enable detect signatures in output traffic (by default `false`)

```

Rule format

- `name` - short name of rule
- `description`- description of rule
- `data` - list of strings that will be searched in http response

Rule example

```
200001:
  name: "linux users creds"
  description: "Linux remote execution cat /etc/passwd"
  data: ["sshd:x:133:65534::/run/sshd:/usr/sbin/nologin"]
