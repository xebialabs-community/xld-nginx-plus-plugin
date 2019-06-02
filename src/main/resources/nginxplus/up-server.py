#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import requests
import requests.packages.urllib3 as urllib3
import json

from nginxplus.Nginxplus import NginxPlusClient

requests.packages.urllib3.disable_warnings()

print "Marking server [%s] as up for upstream [%s] in nginxplus [%s]" % (server_name, upstream_name, nginx_url)
nginx = NginxPlusClient.get_client(nginx_url)
encoded_body = json.dumps({"down": "false"})
url = "%s/api/%s/http/upstreams/%s/servers/%s" % (nginx_url, api_version, upstream_name, nginx.get_server_id(upstream_name, server_name, api_version))
http = urllib3.PoolManager()
response = http.request('PATCH', url,
                        headers={'Content-Type': 'application/json'},
                        body=encoded_body)
if not response.status == 200:
    print "Error: [%s] - [%s]" % (response.status, response.data)
    raise Exception("Failed to mark server [%s] up for upstream [%s] in nginxplus [%s]" % (server_name, upstream_name, nginx_url))



