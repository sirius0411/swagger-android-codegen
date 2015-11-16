import re
import os

urlRegex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def isUrl(string):
    '''
    return if the given string is an url
    '''
    return urlRegex.match(string)

def camelize(word, lowercaseFirstLetter=False):
    '''
    translate from swagger-codegen DefaultCodegen.java#camelize()
    '''
    # Replace all slashes with dots (package separator)
    word = word.replace('/', '.')

    # case out dots
    parts = re.split('\\.', word)
    f = []
    for z in parts:
        if len(z) > 0:
            f.append(z[0].upper())
            f.append(z[1:])
    word = ''.join(f)

    '''
    // why again? skip this segment. i have no idea what's this means
    m = p.matcher(word);
    while (m.find()) {
        word = m.replaceFirst("" + Character.toUpperCase(m.group(1).charAt(0)) + m.group(1).substring(1)/*.toUpperCase()*/);
        m = p.matcher(word);
    }
    '''

    # Uppercase the class name
    '''
    // seems that we don't need this segment
    p = Pattern.compile("(\\.?)(\\w)([^\\.]*)$");
    m = p.matcher(word);
    if (m.find()) {
        String rep = m.group(1) + m.group(2).toUpperCase() + m.group(3);
        rep = rep.replaceAll("\\$", "\\\\\\$");
        word = m.replaceAll(rep);
    }
    '''

    # Replace two underscores with $ to support inner classes.
    word = re.sub('(__)(.)', lambda matched : '$' + matched.group(2).upper(), word)

    # Remove all underscores
    parts = re.split('_', word)
    f = []
    for z in parts:
        if len(z) > 0:
            f.append(z[0].upper())
            f.append(z[1:])
    word = ''.join(f)

    if lowercaseFirstLetter:
        word = word[0].lower() + word[1:]
    
    return word

upperReg = re.compile('^[A-Z_]*$')
def isAllUpperCase(text):
    return upperReg.match(text)

def parseSwaggerRef(ref):
    '''
    parse swagger ref '#/{type}/{name}'
    return a tuple (type, name)
    '''
    # try to split to 3 parts
    parts = ref.split('/', 2)
    if not parts or len(parts) != 3:
        raise RuntimeError('"%s" is not a legal swagger reference' % ref)
    return parts[1], parts[2]