#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


def emptyOrNone(s):
    return s is None or len(s.strip()) == 0


def extract_nginx_aware_containers(deltas):
    nothing_to_do = determine_if_noop(deltas)
    if nothing_to_do:
        return []
    containers = {}
    for delta in deltas.deltas:
        delta_op = str(delta.operation)
        deployed = delta.previous if delta_op == "DESTROY" else delta.deployed
        container = deployed.container
        if container.hasProperty("serverName") and not emptyOrNone(
            container.serverName) and container.nginxServer is not None:
            if container.name in containers.keys():
                continue
            containers[container.name] = container
    return [containers[ke] for ke in containers.keys()]

def determine_if_noop(deltas):
    nothing_to_do = True
    for delta in deltas.deltas:
        if str(delta.operation) != "NOOP":
            nothing_to_do = False
            break
    return nothing_to_do


def generate_steps(containers, context):
    for container in containers:
        server_name = container.serverName
        upstream_name = container.upstreamName
        api_version = container.apiVersion
        vn = container.nginxServer
        sick_step = steps.jython(description="Mark test [%s] as down in Nginx [%s], api version is [%s]" % (server_name, vn.name, api_version), order=5,
                                 script="nginxplus/down-server.py",
                                 jython_context={"server_name": server_name, "upstream_name": upstream_name, "api_version": api_version,
                                                 "nginx_url": vn.url})
        health_step = steps.jython(description="Mark test [%s] as up in Nginx [%s], api version is [%s]" % (server_name, vn.name, api_version), order=95,
                                   script="nginxplus/up-server.py",
                                   jython_context={"server_name": server_name, "upstream_name": upstream_name, "api_version": api_version,
                                                   "nginx_url": vn.url})
        context.addStep(sick_step)
        context.addStep(health_step)


generate_steps(extract_nginx_aware_containers(deltas), context)
