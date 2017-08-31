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
        self.parameters = [Parameter(x) for x in document["parameters"]]
        self.responses = [Response(status, document["responses"][status]) for status in document["responses"].keys()]

class Parameter:
    def __init__(self, document):
        self.name = document["name"]
        self._in = document["in"]
        if document.has_key("description"):
            self.description = document["description"]
        else:
            self.description = ""
        self.required = document["required"]
        # self.schema = document["schema"]
        if document.has_key("type"):
            self.type = document["type"]
        else:
            self.type = None
        # self.format = document["format"]

class Response:
    def __init__(self, status, document):
        self.status = status
        self.description = document["description"]

# Load yaml structure
with open("sample.yml") as file:
    document = yaml.load(file)

# Display server information
host = document["host"]
basePath = document["basePath"]
print "Base: " + host + basePath

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


