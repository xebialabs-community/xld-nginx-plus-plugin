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

requests.packages.urllib3.disable_warnings()


class NginxPlusClient(object):
    def __init__(self, url):
        self.url = url

    @staticmethod
    def get_client(url):
        return NginxPlusClient(url)

    def get_server_id(self, upstream_name, server_name, api_version):
        http = urllib3.PoolManager()
        response = http.request('GET', "%s/api/%s/http/upstreams/%s/servers" % (self.url, api_version, upstream_name))
        if not response.status == 200:
            print "Error: [%s] - [%s]" % (response.status_code, response.text)
            raise Exception("Failed to get upstream conf from [%s] for [%s] using api [%s]" % (upstream_name, self.url, api_version))
        else:
            data = json.loads(response.data.decode('utf-8'))
            id = "-1"
            for server in data:
                if server["server"] == server_name:
                    id = str(server["id"])
                    print "Found server "+server_name+", id = "+id
            if id == "-1":
                raise Exception("Did not find servername [%s] in upstream conf from [%s] for [%s] using api [%s]" % (server_name, upstream_name, self.url, api_version))
            else:
                return id
