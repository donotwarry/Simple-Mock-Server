# coding=utf-8
# 
# API Mock Server (version 1.0.1 2013.12)
# 
# @author:dengjun86@gmail.com

import web
import httplib
import urllib
import os
import time
import codecs

import pdb

urls=(
    '/submit','Submit',
    '/clear','Clear',
    '/mock','Mock',
    '/(.*)','Index',
)
render=web.template.render('templates/')
rulesFilePath='rules.txt'
logsFilePath='logs.txt'

class Index:
 def GET(self,name):
    stringUtils = StringUtils()
    rules = stringUtils.readRules()
    logs = stringUtils.readLogs()
    # pdb.set_trace()
    return render.index(rules, logs)


class Submit:
    def POST(self):
        i = web.input()
        stringUtils = StringUtils()
        stringUtils.writeRules(i.content)
        return 'Success'

class Clear:
    def POST(self):
        os.remove(logsFilePath)
        stringUtils = StringUtils()
        rules = stringUtils.readRules()
        logs = stringUtils.readLogs()
        return render.index(rules, logs)

class Mock:
    def GET(self):
        i = web.input()
        resp = None
        # check mock rules
        stringUtils = StringUtils()
        rules = stringUtils.readRulesArray()
        for rule in rules:
            req = rule['req']
            # pdb.set_trace()
            if req in i.url:
                resp = rule['resp']
                break
        if not resp:
            # return data from real server
            proto, rest = urllib.splittype(i.url)  
            host, rest = urllib.splithost(rest)
            if not host:
                return 'Make sure the mock url is right.'
            conn = httplib.HTTPConnection(host)
            conn.request(method="GET",url=i.url) 
            # pdb.set_trace()
            response = conn.getresponse()
            resp= unicode(response.read(), 'utf-8')

        # pdb.set_trace()

        log = '\n\ntime:' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '\n\n'
        log += 'req:' + i.url + '\n\n'
        log += 'resp:' + resp + '\n\n'
        log += '================log end================='
        stringUtils.writeLogs(log)
        return resp


class StringUtils:
    def readRules(self):
        if not os.path.isfile(rulesFilePath) or os.path.getsize(rulesFilePath) == 0:
            ruleDemo = '#This is a demo for an api mock rule, keep the format and remove the "#" before.\n#\n'
            ruleDemo += '#req:http://tuan.baidu.com/remotedns?\n'
            ruleDemo += '#resp:{"data":[],"errmsg":"success","errno":0}\n'
            return ruleDemo
        rulesFile = codecs.open(rulesFilePath,'r', 'utf-8')
        rules = rulesFile.read()
        return rules

    def writeRules(self, rules):
        rulesFile = codecs.open(rulesFilePath,'w', 'utf-8')
        # pdb.set_trace()
        rulesFile.write(rules)
        rulesFile.close()

    def readLogs(self):
        if not os.path.isfile(logsFilePath) or os.path.getsize(logsFilePath) == 0:
            return 'Here will show you the request logs.'
        logsFile = codecs.open(logsFilePath, 'r', 'utf-8')
        logs = logsFile.read()
        logsFile.close()
        return logs

    def writeLogs(self, logs):
        if not os.path.isfile(logsFilePath):
            logsFile = codecs.open(logsFilePath,'w', 'utf-8')
            logsFile.write(logs)
            logsFile.close()
        else:
            size = os.path.getsize(logsFilePath)
            logsFile = None
            if size > 1000000:
                logsFile = codecs.open(logsFilePath,'w', 'utf-8')
            else:
                logsFile = codecs.open(logsFilePath,'a', 'utf-8')
            logsFile.write(logs)
            logsFile.close()

    def readRulesArray(self):
        rules = []
        if not os.path.isfile(rulesFilePath):
            return rules
        file = codecs.open(rulesFilePath, 'r', 'utf-8')
        req = None
        resp = None
        while 1:
            line = file.readline()
            if not line:
               break

            reqIndex = line.find('req:')
            if reqIndex == 0:
                req = line.replace('req:', '').replace('\r', '').replace('\n', '')
                resp = None

            respIndex = line.find('resp:')
            if respIndex == 0:
                if not req:
                    continue
                resp = line.replace('resp:', '').replace('\r', '').replace('\n', '')

            if req is None or resp is None:
                continue;
            
            rules.append({'req':req,'resp':resp})
        file.close()
        return rules

class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

if __name__=='__main__':
    app = MyApplication(urls, globals())
    app.run(port=8888)

