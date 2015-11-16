"""
code generator factory
"""

import importlib
import os

prefix = 'generators.'
suffix = '_codegen'

def generate(config, swagger):
    '''
    generate the code by the given config and swagger object

    add {language}_codegen.py to ./generators to support the specific language
    each codegen.py must have a method <generate(swagger, templateDir, outputDir)>
    '''
    language = config.get('language')
    templateDir = config.get('template')
    outputDir = config.get('output')
    #fill with default value
    if not templateDir:
        templateDir = getDefaultTemplateDir(language)
    if not outputDir:
        outputDir = getDefaultOutputDir(language)
    
    #load specific generator by language
    try:
        generator = importlib.import_module(prefix + language + suffix)

        #path check
        if not os.path.exists(templateDir):
            print('The template directory "%s" is not exists. Use -t to offer a legal directory' % templateDir)
            exit(1)
        if not os.path.isdir(templateDir):
            print('The template directory "%s" is not a directory. Use -t to offer one' % templateDir)
            exit(1)
        if not os.path.exists(outputDir):
            print('The output directory "%s" is not exists. Create it.' % outputDir)
            os.makedirs(outputDir)
        else:
            if not os.path.isdir(outputDir):
                print('The output directory "%s" is not a directory. Use -o to offer one' % outputDir)
                exit(1)

        # begin
        generator.generate(swagger, templateDir, outputDir)
    except ImportError:
        print('unsupport language %s' % language)
        exit(1)

def getDefaultTemplateDir(language):
    '''
    return the default template dir by the given language
    '''
    path = "./template/" + str(language) + "/"
    return os.path.normcase(path)

def getDefaultOutputDir(language):
    '''
    return the output template dir by the given language
    '''
    path = "./output/" + str(language) + "_api/"
    return os.path.normcase(path)