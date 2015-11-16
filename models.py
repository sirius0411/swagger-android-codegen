class Swagger:

    @property
    def info(self):
        return self._info
    @info.setter
    def info(self, value):
        self._info = value

    @property
    def schemes(self):
        return self._schemes
    @schemes.setter
    def schemes(self, value):
        self._schemes = value

    @property
    def host(self):
        return self._host
    @host.setter
    def host(self, value):
        self._host = value

    @property
    def basePath(self):
        return self._basePath
    @basePath.setter
    def basePath(self, value):
        self._basePath = value

    @property
    def models(self):
        return self._models
    @models.setter
    def models(self, value):
        self._models = value

    @property
    def parameters(self):
        return self._parameters
    @parameters.setter
    def parameters(self, value):
        self._parameters = value

    @property
    def paths(self):
        return self._paths
    @paths.setter
    def paths(self, value):
        self._paths = value

    @property
    def tags(self):
        return self._tags
    @tags.setter
    def tags(self, value):
        self._tags = value

    @property
    def responses(self):
        return self._responses
    @responses.setter
    def responses(self, value):
        self._responses = value

    def __str__(self, **kwargs):
        return 'Swagger[info = %s, schemes = %s, host = %s, basePath = %s, models = %s]' % (self.info, self.schemes, self.host, self.basePath, self.models)
    def __repr__(self):
        return self.__str__()


class Property:
    def __init__(self, key, definition):
        self._name = key
        self._type = definition.get('type')
        self._format = definition.get('format')
        self._default = definition.get('default')
        self._description = definition.get('description')
        self._enum = definition.get('enum')
        self._items = definition.get('items')
        if self._items:
            self._itemref = self._items.get('$ref')
            self._itemtype = self._items.get('type')
            self._itemenum = self._items.get('enum')
        self._ref = definition.get('$ref')

    @property
    def name(self):
        return self._name
    @property
    def type(self):
        return self._type
    @property
    def format(self):
        return self._format
    @property
    def default(self):
        return self._default
    @property
    def description(self):
        return self._description
    @property
    def enum(self):
        return self._enum
    @property
    def items(self):
        return self._items
    @property
    def itemref(self):
        return self._itemref
    @property
    def itemtype(self):
        return self._itemtype
    @property
    def itemenum(self):
        return self._itemenum
    @property
    def ref(self):
        return self._ref

    def __str__(self, **kwargs):
        return 'Property[name = %s, type = %s, format = %s, default = %s, description = %s, enum = %s, items = %s, ref = %s]' % (self._name, self._type, self._format, self._default, self._description, self._enum, self._items, self._ref)
    def __repr__(self):
        return self.__str__()

class Model:
    def __init__(self, key, definition):
        self._name = key
        self._properties = []
        self._required = definition.get('required')
        properties = definition.get('properties')
        if properties:
            for key in properties:
                self._properties.append(Property(key, properties.get(key)))
        return

    @property
    def name(self):
        return self._name
    @property
    def required(self):
        return self._required
    @property
    def properties(self):
        return self._properties

    def __str__(self):
        return 'Model[name = %s, required = %s, properties = %s]' % (self._name, self._required, self._properties)
    def __repr__(self):
        return self.__str__()

class Info:
    
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, value):
        self._title = value

    @property
    def version(self):
        return self._version
    @version.setter
    def version(self, value):
        self._version = value

    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        self._description = value

    def __str__(self, **kwargs):
        return 'Info[title = %s, version = %s, description = %s]' % (self.title, self.version, self.description)
    def __repr__(self):
        return self.__str__()

class Parameter:

    def __init__(self, key, definition):
        self.key = key
        self.ref = definition.get('$ref')
        self.required = definition.get('required')
        self.type = definition.get('type')
        self.name = definition.get('name')
        self.location = definition.get('in')
        self.description = definition.get('description')
        self.default = definition.get('default')
        self.enum = definition.get('enum')
        self.schema = definition.get('schema')
        items = definition.get('items')
        if items:
            self.itemEnum = items.get('enum')
            self.itemType = items.get('type')
            self.itemRef = items.get('$ref')
        return

    @property
    def ref(self):
        return self._ref
    @ref.setter
    def ref(self, value):
        self._ref = value

    @property
    def key(self):
        return self._key
    @key.setter
    def key(self, value):
        self._key = value

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    # since 'in' is a reserved name in python, use 'location' instead.
    @property
    def location(self):
        return self._location
    @location.setter
    def location(self, value):
        self._location = value

    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        self._description = value

    @property
    def required(self):
        return self._required
    @required.setter
    def required(self, value):
        self._required = value

    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value

    @property
    def default(self):
        return self._default
    @default.setter
    def default(self, value):
        self._default = value

    @property
    def itemType(self):
        return self._itemType
    @itemType.setter
    def itemType(self, value):
        self._itemType = value

    @property
    def enum(self):
        return self._enum
    @enum.setter
    def enum(self, value):
        self._enum = value

    @property
    def itemEnum(self):
        return self._itemEnum
    @itemEnum.setter
    def itemEnum(self, value):
        self._itemEnum = value

    @property
    def schema(self):
        return self._schema
    @schema.setter
    def schema(self, value):
        self._schema = value

    @property
    def itemRef(self):
        return self._itemRef
    @itemRef.setter
    def itemRef(self, value):
        self._itemRef = value

class Path:

    def __init__(self, key, definition):
        self.path = key
        self.operations = []
        for methodKey in definition:
            self.operations.append(Operation(methodKey, definition.get(methodKey)))

    @property
    def path(self):
        return self._path
    @path.setter
    def path(self, value):
        self._path = value

    @property
    def operations(self):
        return self._operations
    @operations.setter
    def operations(self, value):
        self._operations = value

class Operation:

    def __init__(self, key, definition):
        self.method = key
        self.summary = definition.get('summary')
        self.description = definition.get('description')
        self.tags = definition.get('tags')
        self.parameters = []
        parametersArray = definition.get('parameters')
        if parametersArray:
            for i in parametersArray:
                self.parameters.append(Parameter(None, i))
        self.responses = []
        for i in definition.get('responses'):
            self.responses.append(Response(i, definition.get('responses').get(i)))

    @property
    def method(self):
        return self._method
    @method.setter
    def method(self, value):
        self._method = value

    @property
    def summary(self):
        return self._summary
    @summary.setter
    def summary(self, value):
        self._summary = value

    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        self._description = value

    @property
    def parameters(self):
        return self._parameters
    @parameters.setter
    def parameters(self, value):
        self._parameters = value

    @property
    def tags(self):
        return self._tags
    @tags.setter
    def tags(self, value):
        self._tags = value

    @property
    def responses(self):
        return self._responses
    @responses.setter
    def responses(self, value):
        self._responses = value

class Response:

    def __init__(self, code, definition):
        self.code = code
        self.description = definition.get('description')
        self.schema = definition.get('schema')
        
    @property
    def code(self):
        return self._code
    @code.setter
    def code(self, value):
        self._code = value

    @property
    def schema(self):
        return self._schema
    @schema.setter
    def schema(self, value):
        self._schema = value

    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        self._description = value