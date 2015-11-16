import sys
import getopt

__version__ = '0.0.1'

def printVersion():
    print('swagger codegen version %s' % __version__)

def printHelp():
    print('usage: python swagger_codegen.py [option] -j jsonPath -l language [-i | -t template | -o output]')
    print('Options and arguments:')
    print('-j jsonPath : the source swagger json path (url or file path) (also --json=jsonPath)')
    print('-l language : destination language, support values["android", "rxandroid"] (also --language=language)')
    print('-v          : print the version info (also --version)')
    print('-h          : print the help info (also --help)')
    print('-i          : input missing field (e.g.: mooc swagger don\'t have host info) (also --input)')
    print('-t template : template directory that will be used (also --template==)')
    print('-o output   : output directory that the code will be placed (also --output==)')

def getConfig():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hvj:il:t:o:', ['help', 'version', 'json=', 'input', 'language', 'template', 'output'])
    except getopt.GetoptError as e:
        print(e)
        exit(1)

    config = {}

    for opt, val in opts:
        if opt in ('-v', '--version'): #version
            printVersion()
            exit(0)
        elif opt in ('-h', '--help'): #help
            printHelp()
            exit(0)
        elif opt in ('-j', '--json'): #input json path(required)
            config['json'] = val
        elif opt in ('-i', '--input'): #input missing field
            config['input'] = True
        elif opt in ('-l', '--language'): #generate language(required)
            config['language'] = val
        elif opt in ('-t', '--template'): #template dir
            config['template'] = val
        elif opt in ('-o', '--output'): #output dir
            config['output'] = val

    if not 'json' in config.keys():
        print('-j missing')
        printHelp()
        exit(1)
    if not 'language' in config.keys():
        print('-l missing')
        printHelp()
        exit(1)

    return config