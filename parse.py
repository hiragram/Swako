import yaml

# models
class Endpoint:
    def __init__(self, path, document):
        self.path = path
        methods = []
        for method in document.keys():
            methods.append(EndpointMethod(method, document[method]))
        
        self.methods = methods

class EndpointMethod:
    def __init__(self, method, document):
        self.method = method
        self.summary = document["summary"]
        if document.has_key("parameters"):
            self.parameters = [Parameter(x) for x in document["parameters"]]
        else:
            self.parameters = []

        successResponse = None
        if document["responses"].has_key(200):
            successResponse = document["responses"][200]
        elif document["responses"].has_key("default"):
            successResponse = document["responses"]["default"]
        if successResponse != None:
            self.response = Response(successResponse)
        else:
            self.response = None

class Parameter:
    def __init__(self, document):
        self.name = document["name"]
        self._in = document["in"]
        if document.has_key("description"):
            self.description = document["description"]
        else:
            self.description = ""
        if document.has_key("required"):
            self.required = document["required"]
        else:
            self.required = False
        if document.has_key("type"):
            self.type = document["type"]
            if document.has_key("items"):
                if document["items"].has_key("type"):
                    self.itemType = document["items"]["type"]
        elif document.has_key("schema"):
            if document["schema"].has_key("$ref"):
                self.type = document["schema"]["$ref"]
            else:
                self.type = document["schema"]["type"]
                if document["schema"]["items"].has_key("$ref"):
                    self.itemType = document["schema"]["items"]["$ref"]
                elif document["schema"]["items"].has_key("type"):
                    self.itemType = document["schema"]["items"]["type"]
        else:
            self.type = None
        # self.format = document["format"]
        if document.has_key("nullable"):
            self.nullable = document.has_key["nullable"]
        else:
            self.nullable = False

class Response:
    def __init__(self, document):
        self.description = document["description"]
        if document.has_key("schema"):
            if document["schema"].has_key("$ref"):
                self.type = document["schema"]["$ref"]
            elif document["schema"].has_key("items"):
                self.type = document["schema"]["type"]
                if document["schema"]["items"].has_key("$ref"):
                    self.itemType = document["schema"]["items"]["$ref"]
                elif document["schema"]["items"].has_key("type"):
                    self.itemType = document["schema"]["items"]["type"]
                else:
                    self.itemType = None

class ModelDefinition:
    def __init__(self, name, document):
        self.name = name
        self.type = document["type"]
        if self.type == "array":
            self.items_dref = document["items"]["$ref"]
            self.properties = []
        elif self.type == "object":
            self.items_dref = ""
            self.properties = [ModelProperty(name, data) for name, data in document["properties"].iteritems()]
        elif self.type == "string":
            self.items_dref = ""
            self.properties = []
            # do nothing

class ModelProperty:
    def __init__(self, name, document):
        self.name = name
        if document.has_key("$ref"):
            self.dref = document["$ref"]
            self.type = document["$ref"]
        else:
            self.type = document["type"]
            if self.type == "array":
                items = document["items"]
                if items.has_key("$ref"):
                    self.itemType = items["$ref"]
                else:
                    self.itemType = items["type"]
            if document.has_key("format"):
                self.format = document["format"]
            else:
                self.format = None
            if document.has_key("nullable"):
                self.nullable = document["nullable"]
            else:
                self.nullable = False
        
        if document.has_key("description"):
            self.description = document["description"]
        else:
            self.description = ""

def parseModels(filename):
    # Load yaml structure
    with open(filename) as file:
        document = yaml.load(file)

    # Parse model objects definition
    definitions = document["definitions"]
    models = []
    for name, model_dict in definitions.iteritems():
        models.append(ModelDefinition(name, model_dict))

    return models

def parseEndpoints(filename):
    # Load yaml structure
    with open(filename) as file:
        document = yaml.load(file)

    # Parse endpoints information
    paths = document["paths"]
    endpoints = []
    for path, endpoint_dict in paths.iteritems():
        endpoints.append(Endpoint(path, endpoint_dict))

    return endpoints

# Parse and display structure
def printInfo(filename):
    # Load yaml structure
    with open(filename) as file:
        document = yaml.load(file)

    # Parse endpoints information
    paths = document["paths"]
    endpoints = []
    for path, endpoint_dict in paths.iteritems():
        endpoints.append(Endpoint(path, endpoint_dict))

    for endpoint in endpoints:
        print ""
        print "Path: " + endpoint.path
        for endpointMethod in endpoint.methods:
            print "\tMethod: " + endpointMethod.method
            print "\t\tSummary: " + endpointMethod.summary
            print "\t\tParameters: "
            for parameter in endpointMethod.parameters:
                print "\t\t\tName: " + parameter.name
                print "\t\t\t\tDescription: " + parameter.description
                if parameter.type != None:
                    print "\t\t\t\tType: " + parameter.type
                print "\t\t\t\tRequired: " + str(parameter.required)
                print "\t\t\t\tIn: " + parameter._in
            
            print "\t\tResponses: "
            for response in endpointMethod.responses:
                print "\t\t\tStatus: " + str(response.status)
                print "\t\t\t\tDescription: " + response.description


    # Parse model objects definition
    definitions = document["definitions"]
    models = []
    for name, model_dict in definitions.iteritems():
        models.append(ModelDefinition(name, model_dict))

    for model in models:
        print "Model: " + model.name
        print "\tProperties: "
        for property in model.properties:
            print "\t\tName: " + str(property.name)
            if hasattr(property, "dref"):
                print "\t\t\t$ref: " + property.dref
            else:
                print "\t\t\tType: " + property.type
                print "\t\t\tNullable: " + str(property.nullable)
                if property.format != None:
                    print "\t\t\tFormat: " + property.format
                