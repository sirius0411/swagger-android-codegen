"""
rxandroid codegen for code_generator.py
works with RxJava & RxAndroid
generate a standalone gradle module

pacakge com.guokr.android
structure:
----src/main--java/com/guokr/android--model/
  |         |                       |-api/
  |         |                       |-NetManager.java
  |         |-AndroidManifest.xml
  |-build.gradle

issues:
# model
-- format is ignored(all 'number' 'integer' will be parsed as 'int'), format info will be placed in descriptions
-- enum won't be parsed at a java Enum(marked in description instead)
# api
-- api method name may confilct
-- only the last tag in 'tags' will be parsed
-- many swagger tags are ignored
"""

import pystache
import os
import util
import re

modulePackage = 'com.guokr.android'
modelPackage = modulePackage + '.model'
apiPackage = modulePackage + '.api'
rootDir = ''
srcMainDir = ''
codeRootDir = ''
modelDir = ''
apiDir = ''

def generate(swagger, templateDir, outputDir):
    '''
    render the templates by pystache and save the results to the given path
    '''
    global rootDir, srcMainDir, codeRootDir, modelDir, apiDir
    rootDir = formatPath(outputDir)
    srcMainDir = formatPath(rootDir + '/src/main')
    codeRootDir = formatPath(srcMainDir + '/java/' + modulePackage.replace('.', '/'))
    modelDir = formatPath(codeRootDir + '/model')
    apiDir = formatPath(codeRootDir + '/api')
    try:
        os.makedirs(modelDir)
        os.makedirs(apiDir)
    except:
        pass

    renderBuildGradle(swagger, formatPath(templateDir + '/build.gradle.mustache'))
    renderProguard(swagger, formatPath(templateDir + '/proguard-rules.pro.mustache'))
    renderAndroidManifest(swagger, formatPath(templateDir + '/AndroidManifest.xml.mustache'))
    renderModel(swagger, formatPath(templateDir + '/model.mustache'))
    renderApi(swagger, formatPath(templateDir + '/api.mustache'))
    renderNetManager(swagger, formatPath(templateDir + '/NetManager.mustache'))

def renderBuildGradle(swagger, templatePath):
    if not isTemplatePathValid(templatePath):
        return
    with open(templatePath) as templateFile:
        templateData = templateFile.read()
        #nothing needs to render.  simply save it
        savePath = rootDir + '/build.gradle'
        saveTo(savePath, templateData)

def renderProguard(swagger, templatePath):
    if not isTemplatePathValid(templatePath):
        return
    with open(templatePath) as templateFile:
        templateData = templateFile.read()
        #nothing needs to render.  simply save it
        savePath = rootDir + '/proguard-rules.pro'
        saveTo(savePath, templateData)

def renderAndroidManifest(swagger, templatePath):
    if not isTemplatePathValid(templatePath):
        return
    with open(templatePath) as templateFile:
        templateData = templateFile.read()
        context = {}
        context['modulePackage'] = modulePackage
        result = pystache.render(templateData, context)
        savePath = srcMainDir + '/AndroidManifest.xml'
        saveTo(savePath, result)

def renderModel(swagger, templatePath):
    if not isTemplatePathValid(templatePath):
        return
    with open(templatePath) as templateFile:
        templateData = templateFile.read()
        '''
        context sample
        {
            'package': 'xxx',
            'imports': [{'import':'xxx'}, {'import':'xxx'}, ...],
            'classname': 'xxx',
            'fields': [
                {
                    'baseName': 'xxx',
                    'dataType': 'xxx',
                    'name': 'xxx',
                    'description': 'xxx',
                    'getter': 'xxx',
                    'setter': 'xxx',
                    'format': 'xxx',
                    'enum': [xxx, xxx, xxx]
                    'isEnum': true|false
                }, ...
            ]
        }
        '''
        for model in swagger.models:
            context = {}
            context['package'] = modelPackage
            context['classname'] = toClassName(model.name)
            fields = []
            imports = set()
            # parse model
            for modelField in model.properties:
                field = {}
                field['baseName'] = modelField.name
                datatype = None
                if modelField.type:
                    datatype = toDataType(modelField.type)
                elif modelField.ref: # no type key, should have '$ref'
                    datatype = refToClassName(modelField.ref, True)
                field['datatype'] = datatype
                field['name'] = toFieldName(modelField.name)
                if modelField.description:
                    field['description'] = modelField.description
                if modelField.format:
                    if not field.get('description'):
                        # format will be rendered only if there's description
                        field['description'] = 'accepted format'
                    field['format'] = modelField.format
                if modelField.enum:
                    if not field.get('description'):
                        # enum will be rendered only if there's description
                        field['description'] = 'accepted value'
                    field['enum'] = modelField.enum
                    field['isEnum'] = 'true'
                field['getter'] = toGetter(field['name'])
                field['setter'] = toSetter(field['name'])
                fields.append(field)
                # get the import set for 'imports'
                if modelField.type == 'array':
                    imports.add('array')
                    # when type == array, the property should have a key 'items'
                    if modelField.itemref:
                        # item type defined in '$ref'
                        imports.add(modelField.itemref)
                        field['datatype'] = field['datatype'] % refToClassName(modelField.itemref, True)
                    elif modelField.itemtype:
                        field['datatype'] = field['datatype'] % toDataType(modelField.itemtype, True)
                        if modelField.itemenum:
                            if not field.get('description'):
                                # enum will be rendered only if there's description
                                field['description'] = 'accepted item value'
                            field['enum'] = modelField.itemenum
                            field['isEnum'] = 'true'
                if modelField.ref:
                    imports.add(modelField.ref)

            context['fields'] = fields
            context['imports'] = toImports(imports)
            result = pystache.render(templateData, context)
            savePath = modelDir + '/' + context['classname'] + '.java'
            saveTo(savePath, result)

def renderApi(swagger, templatePath):
    if not isTemplatePathValid(templatePath):
        return
    with open(templatePath) as f:
        template = f.read()
        '''
        api context
        {
            'package': 'xxx',
            'modelPackage': 'xxx',
            'imports': [{'import': 'xxx'}, ...]
            'classname': 'xxx',  // seems that each class is created according to the 'tags''s last item
            'operations': [
                {
                    'summary': 'xxx',
                    'apiDescription': 'xxx',
                    'methodName': 'xxx',
                    'httpMethod': 'xxx',
                    'path': 'xxx',
                    'responseType': 'xxx',
                    'hasForm': true/false，
                    'parameters':[
                        {
                            'paramIn': 'xxx',
                            'inKey': 'xxx',
                            'paramName': 'xxx',
                            'paramDescription': 'xxx',
                            'paramType': 'xxx',
                            'isEnum': 'xxx',
                            'enumValues': [...],
                            'hasMore': true/false
                        }
                    ]
                }
            ]
        }
        '''
        # get tags list first, the list item claims the api class name
        contexts = {}
        tags = set()
        if swagger.tags:
            for tag in swagger.tags:
                tags.add(tag.get('name'))
        for path in swagger.paths:
            for operation in path.operations:
                if operation.tags:
                    tags.add(operation.tags[-1])
                else:
                    # this operation has no tags, generate one by the path. add the tag to the operation's 'tags'
                    tag = getTagByPath(path.path)
                    tags.add(tag)
                    operation.tags = [tag]
        # now we have all tags. create blank render context for each one
        for tag in tags:
            context = {}
            context['package'] = apiPackage
            context['modelPackage'] = modelPackage
            context['classname'] = toApiClassName(tag)
            context['operations'] = []
            contexts[tag] = context
        # fill operations
        for path in swagger.paths:
            for operation in path.operations:
                # tags has been filled above, won't be null
                tag = operation.tags[-1]
                context = contexts[tag]
                optContext = {}
                optContext['summary'] = operation.summary
                optContext['apiDescription'] = operation.description

                pathVar = path.path
                pathVar = re.sub(r'^/*(.*)', r'\1', pathVar)
                pathVar = re.sub(r'([^/]*)/*$', r'\1', pathVar)
                optContext['path'] = pathVar

                optContext['httpMethod'] = toFieldName(operation.method, True)
                optContext['methodName'] = toApiMethodName(operation.method, path.path)

                responseType = None
                for responseItem in operation.responses:
                    if responseItem.code.startswith('2'):
                        # try to parse response type
                        if not responseItem.schema:
                            responseType = 'Void'
                        else:
                            isArray = responseItem.schema.get('type')
                            if isArray:
                                items = responseItem.schema.get('items')
                                if items:
                                    itemRef = items.get('$ref')
                                    if itemRef:
                                        responseType = toDataType('array') % refToClassName(itemRef, True)
                            else:
                                ref = responseItem.schema.get('$ref')
                                responseType = refToClassName(ref, True)
                optContext['responseType'] = responseType

                parameters = []
                for parameter in operation.parameters:
                    paramSrc = None
                    if parameter.ref:
                        # parse the reference
                        type, name = util.parseSwaggerRef(parameter.ref)
                        for p in swagger.parameters:
                            if p.key == name:
                                paramSrc = p
                    else:
                        paramSrc = parameter
                    pContext = {}
                    # if paramter 'in' is 'formData', 'paramIn' value in Retrofit is 'Field'
                    if paramSrc.location == 'formData':
                        pContext['paramIn'] = 'Field'
                        optContext['hasForm'] = True
                    else:
                        pContext['paramIn'] = util.camelize(paramSrc.location)
                    # in retrofit annotations, @Body and @QueryMap(impossible in this parser) don't need a value
                    if str(paramSrc.location).lower() != 'body':
                        pContext['inKey'] = paramSrc.name
                    pContext['paramName'] = toFieldName(paramSrc.name)
                    pContext['paramDescription'] = paramSrc.description
                    pType = None
                    # now simply consider the schema is a json object, not an array
                    if paramSrc.schema:
                        ref = paramSrc.schema.get("$ref")
                        if ref:
                            pType = refToClassName(ref, True)
                    else:
                        pType = toDataType(paramSrc.type)
                    if paramSrc.type == 'array':
                        if paramSrc.itemRef:
                            pType = pType % refToClassName(paramSrc.itemRef, True)
                        elif paramSrc.itemType:
                            pType = pType % toDataType(paramSrc.itemType, True)
                            if paramSrc.itemEnum:
                                pContext['isEnum'] = 'true'
                                pContext['enumValues'] = paramSrc.itemEnum
                    pContext['paramType'] = pType
                    pContext['hasMore'] = True
                    parameters.append(pContext)
                if len(parameters) > 0:
                    parameters[-1]['hasMore'] = False
                optContext['parameters'] = parameters
                context['operations'].append(optContext)
        # now we have contexts. render each one
        for key in contexts:
            context = contexts.get(key)
            result = pystache.render(template, context)
            savePath = apiDir + '/' + context['classname'] + '.java'
            saveTo(savePath, result)

def renderNetManager(swagger, templatePath):
    if not isTemplatePathValid(templatePath):
        return
    with open(templatePath) as f:
        template = f.read()
        '''
        context sample
        {
            'package': 'xxx',
            'host': 'xxx',
            'basePath': 'xxx',
            'protocol': 'xxx'
        }
        '''
        context = {}
        context['package'] = modulePackage
        context['host'] = swagger.host
        context['basePath'] = swagger.basePath
        context['protocol'] = str(swagger.schemes[0]).lower()
        result = pystache.render(template, context)
        savePath = codeRootDir + '/NetManager.java'
        saveTo(savePath, result)

def saveTo(path, content):
    '''
    save content to path in utf-8
    '''
    #pass
    print('rendering %s' % path)
    with open(path, mode='w', encoding='utf-8') as f:
        f.write(content)

def isTemplatePathValid(path):
    if not os.path.exists(path):
        print('Could not find template file "%s", skip this' % path)
        return False
    if not os.path.isfile(path):
        print('The path "%s" is not a valid file, skip this' % path)
        return False
    return True

reservedWords = ("abstract", "continue", "for", "new", "switch", "assert",
        "default", "if", "package", "synchronized", "boolean", "do", "goto", "private",
        "this", "break", "double", "implements", "protected", "throw", "byte", "else",
        "import", "public", "throws", "case", "enum", "instanceof", "return", "transient",
        "catch", "extends", "int", "short", "try", "char", "final", "interface", "static",
        "void", "class", "finally", "long", "strictfp", "volatile", "const", "float",
        "native", "super", "while")

def toClassName(name):
    '''
    format class name to match java rules
    '''
    # model name cannot use reserved keyword, e.g.  return
    if name in reservedWords:
        raise RuntimeError('%s (reserved word) cannot be used as a model name' % name)

    # camelize the model name
    # phone_number => PhoneNumber
    return util.camelize(name)

def toApiClassName(name):
    '''
    format to api class name
    e.g.: /person/{id} => PersonPersonId
    '''
    return toClassName(name) + 'Api'

typeMap = {
        'string': 'String',
        'integer': 'int',
        'boolean': 'boolean',
        'array': 'List<%s>',
        'number': 'int'
    }

typeMapClass = {
        'string': 'String',
        'integer': 'Integer',
        'boolean': 'Boolean',
        'array': 'List<%s>',
        'number': 'Integer'
    }

def toDataType(type, castToClass = False):
    '''
    convert swagger type to java type
    '''
    result = None
    if castToClass:
        result = typeMapClass.get(type)
    else:
        result = typeMap.get(type)
    if not result:
        print('unknown data type %s' % type)
    return result

def toImports(typeSet):
    '''
    convert the set of classes to import to an array that used for mustache rendering
    '''
    result = []
    for type in typeSet:
        item = {}
        if type == 'array':
            item['import'] = 'java.util.List'
        else:
            item['import'] = refToClassName(type)
        result.append(item)
    return result

def refToClassName(ref, needSimple=False):
    '''
    convert a ref string to java class name
    '''
    try:
        refType, refName = util.parseSwaggerRef(ref)
    except RuntimeError:
        print('"%s" is not a swagger reference' % ref)
        return ref
    prefix = ''
    if refType == 'definitions': # models
        prefix = modelPackage
    location = refName.split('/')
    result = prefix
    if len(location) > 0:
        location[-1] = util.camelize(location[-1])
    for l in location:
        result += '.' + l

    # simple class name
    if needSimple:
        result = result.split('.')[-1]

    return result

def toFieldName(name, isStatic=False, isApiName = False):
    '''
    format field name to match java rules
    '''
    # replace - with _ e.g.  created-at => created_at
    name = name.replace('-', '_')

    # if it's all uppper case, do nothing
    if util.isAllUpperCase(name):
        return name

    # camelize (lower first character) the variable name
    # pet_id => petId
    name = util.camelize(name, True)

    if isStatic:
        # uppercase all characters with _ divider
        # pet_id => PET_ID
        name = re.sub(r'([A-Z])', r'_\1', name).upper()

    if isApiName:
        name = re.sub(r'{([^}]*)}', r'_\1', name)

    # for reserved word or word starting with number, append _
    if name in reservedWords or name[0].isdigit():
        name = escapeReservedWord(name)

    return name

def toDefaultValue(value):
    '''
    convert swagger value to java type
    '''
    result = str(value)
    # number, do nothing
    if result.isdigit():
        return result

    # boolean
    if result.lower() == 'true' or result.lower() == 'false':
        return result.lower()

    return result

def toGetter(name):
    '''
    format getter name to match java rules
    '''
    return 'get' + util.camelize(name)

def toSetter(name):
    '''
    format setter name to match java rules
    '''
    return 'set' + util.camelize(name)

def escapeReservedWord(word):
    return '_' + word

def formatPath(path):
    path = os.path.normcase(path)
    path = os.path.normpath(path)
    return path

def getTagByPath(path):
    '''
    when path doesn't have a tag. generate one by the path root
    e.g.  /product/info => tag = Product
    '''
    path = re.sub(r'/{1,}', '', path, 1)
    if '/' in path:
        parts = path.split('/')
        path = parts[0]
    return util.camelize(path)

def toApiMethodName(httpMethod, path):
    '''
    use the api http method + path to generate a java api method name
    e.g. GET /user/favorite/{favorite_id}/tag => getUserFavoriteTag
    '''
    result = util.camelize(path)
    result = re.sub(r'{([^}]*)}', '', result)
    #parts = result.split('{')
    return str(httpMethod).lower() + result