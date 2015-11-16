"""
swagger parser
parse swagger json to a tuple
"""

import json
import util
import models as beans
from urllib import request
from urllib import parse as urlparse

def parse(config):
    """
    parse the given json to a Swagger object
    """

    path = config['json']
    jsonStr = _getJson(path)
    swaggerObj = json.loads(jsonStr)

    #parse info
    infoDict = swaggerObj.get('info')
    info = beans.Info()
    if infoDict:
        info.title = infoDict.get('title')
        info.version = infoDict.get('version')
        info.description = infoDict.get('description')

    #parse url
    schemes = swaggerObj.get('schemes') #required
    host = swaggerObj.get('host') #required
    basePath = swaggerObj.get('basePath') #optional

    #parse model
    models = []
    definitions = swaggerObj.get('definitions')
    if definitions:
        for key in definitions:
            models.append(beans.Model(key, definitions.get(key)))

    #parse parameters
    parameters = []
    parametersArray = swaggerObj.get('parameters')
    if parametersArray:
        for key in parametersArray:
            parameters.append(beans.Parameter(key, parametersArray.get(key)))

    #parse paths
    paths = []
    pathsArray = swaggerObj.get('paths')
    if pathsArray:
        for key in pathsArray:
            paths.append(beans.Path(key, pathsArray.get(key)))

    #parse tags
    tags = swaggerObj.get('tags')

    #responses
    responses = []
    responseArray = swaggerObj.get('responses')
    if responseArray:
        for key in responseArray:
            responses.append(beans.Response(key, responseArray.get(key)))

    inputMissingField = config.get('input', False)
    if inputMissingField:
        if not schemes:
            schemes = []
            schemes.append(input("'schemes' is missing, please input:"))
        if not host:
            host = input("'host' is missing, please input:")
    else:
        if util.isUrl(path):
            pathParseTuple = urlparse.urlparse(path)
            if not schemes:
                schemes = []
                schemes.append(pathParseTuple[0])
            if not host:
                host = pathParseTuple[1]
        if not schemes or not host:
            print('Missing field(s). Auto complete failed. Try using -i or --input to fill missing field(s) by yourself')
            exit(1)

    swagger = beans.Swagger()
    swagger.info = info
    swagger.schemes = schemes
    swagger.host = host
    swagger.basePath = basePath
    swagger.models = models
    swagger.parameters = parameters
    swagger.paths = paths
    swagger.tags = tags
    swagger.responses = responses
    return swagger

def _getJson(path):
    if util.isUrl(path):
        with request.urlopen(path) as r:
            data = r.read()
            return data.decode('utf-8')
    else:
        with open(path) as f:
            return f.read()
