import base64
import urllib2
import ssl
import json
import time
import sys
import xml.etree.ElementTree as ET
import urllib
import os, subprocess, argparse, shlex



args = shlex.split("hostname -f")
serverName = subprocess.check_output(args, shell=True).strip()


username=sys.argv[3]
password=sys.argv[4]

# disable proxy
proxy_support = urllib2.ProxyHandler({})
opener = urllib2.build_opener(proxy_support)
urllib2.install_opener(opener)

execution_url = 'https://dma.dca.demo.local:8443/dma/api/auto/running/'
data = urllib.urlencode({'workflow' : "%s" % sys.argv[2],
                         'deployment'  : "%s" % sys.argv[1],
                         'server': "%s" % serverName})


encoded_credentials = base64.b64encode(b"{0}:{1}".format(username, password))
headers = {
    #"Content-Type": "application/xml",
    "Authorization": "Basic {}".format(encoded_credentials)
}

req = urllib2.Request(execution_url, data=data, headers = headers)

try:
    response = urllib2.urlopen(req, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)).read()
    xml_response = response

    root = ET.fromstring(xml_response)
    jobstatusurl = root[0].text
    print >> sys.stderr, jobstatusurl

    get_execution_status_url = jobstatusurl
    req = urllib2.Request(get_execution_status_url, headers=headers)

    max_wait_time_in_seconds = 840
    check_interval_in_seconds = 20
    for attempt in xrange(max_wait_time_in_seconds / check_interval_in_seconds):
        time.sleep(check_interval_in_seconds)
        response = urllib2.urlopen(req, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)).read()
        xml_response = response
        root = ET.fromstring(xml_response)
        jobstatus = root.find("{http://www.hp.com/dma/api/sop}status").attrib['state']
        print >> sys.stderr, jobstatus
        if len(jobstatus) > 0 and jobstatus == "Success":
            print >> sys.stderr, "Job finished"
            sys.exit(0)
        if len(jobstatus) > 0 and jobstatus == "Failed":
            print >> sys.stderr, "Job Failed"
            sys.exit(1)
        if len(jobstatus) > 0 and jobstatus == "Aborted":
            print >> sys.stderr, "Job Aborted"
            sys.exit(1)
    # the flow did not complete in the allotted time
    print "Flow did not complete in %s seconds" % max_wait_time_in_seconds
    sys.exit(220)


except urllib2.HTTPError as err:
    print "Error"
    print err.read()