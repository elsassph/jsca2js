#!/usr/bin/python

import json
from formatter import Formatter

METHOD_INDENTATION = 4

def decodeJsonFromFile(filePath):
    try:
        jsonFile = open(filePath, 'r')
    except IOError:
        raise Exception('Unable to find JSON API file in path: ' + filePath)

    return json.JSONDecoder().decode(jsonFile.read())


def generateMethodJSDoc(method):
    formatter = Formatter(METHOD_INDENTATION)
    formatter.newLine()
    formatter.addLine('/**')

    prefix = ' * '

    formatter.addLine(prefix, method['value'])
    formatter.addLine(prefix, 'platforms:', ', '.join(method['platforms']))

    for param in method['parameters']:
        formatter.addLine(prefix, '@param {', param['type'], '} ', param['name'], ' ', param['description'])

    if method['returntype'] != 'void':
        formatter.addLine(prefix, '@returns {', method['returntype'] + '}')

    formatter.addLine(' */')
    return formatter.getResult()


def formatParams(params):
    paramNames = [param['name'] for param in params]
    return ', '.join(paramNames)


def formatMethods(namespace):
    formatter = Formatter(METHOD_INDENTATION)
    for method in namespace['methods']:
        formatter.addLine(generateMethodJSDoc(method))
        formatter.addLine('this.', method['name'], ' = function(', formatParams(method['parameters']), ") {")
        formatter.addLine('}')
        formatter.newLine()
    return formatter.getResult()


def formatNamespace(namespace):
    formatter = Formatter()
    formatter.addLine(namespace[0], ' = (function() {').newLine()
    formatter.addLine(formatMethods(namespace[1]))
    formatter.addLine('}());').newLine()
    return formatter.getResult()


def writeFile(string):
    filename = 'titanium.js'
    file = open(filename, 'w')
    file.write(string)
    file.close()


def main():
    fileName = './api.json'
    jsonApi = decodeJsonFromFile(fileName)

    javascript = ''
    for namespace in sorted(jsonApi.items()):
        javascript += formatNamespace(namespace)

    writeFile(javascript)

if __name__ == "__main__":
    main()