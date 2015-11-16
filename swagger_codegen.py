"""
swagger codegen entrance
"""

import shell
import swagger_parser
import code_generator
import util

def main():
    config = shell.getConfig()
    swagger = swagger_parser.parse(config)
    code_generator.generate(config, swagger)
    print('generate complete')
    
if __name__ == '__main__':
    main()