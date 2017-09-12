import re

def typeNameFromProperty(property):
    primitive = typeNameString(property.type)
    if primitive != None:
        return primitive

    if property.type == "array":
        elementName = typeNameString(property.itemType)
        return "[" + elementName + "]"

def typeNameFromParameter(parameter):
    typeName = ""
    
    if parameter.type == "array":
        elementName = typeNameString(parameter.itemType)
        typeName = "[" + elementName + "]"
    else:
        typeName = typeNameString(parameter.type)

    if parameter.nullable:
        typeName += "?"

    return typeName

def typeNameFromResponse(response):
    if response == None:
        return "Void"
    elif hasattr(response, "type") == False:
        return "Void"

    typeName = ""
    
    if response.type == "array":
        elementName = typeNameString(response.itemType)
        typeName = "Array<" + elementName + ">"
    else:
        typeName = typeNameString(response.type)

    return typeName  

def typeNameString(typeName):
    if typeName == "integer":
        return "Int"
    elif typeName == "string":
        return "String"
    elif typeName == "boolean":
        return "Bool"
    elif typeName == "array":
        return None
    elif typeName == "file":
        return "File is not supported"
    elif typeName == None:
        return None
    else:
        m = re.search(r"#/definitions/(.*)", typeName)
        return m.group(1)

def endpointTypeName(endpoint):
    pathComponents = endpoint.path.replace("{", "").replace("}", "").split("/")

    words = [pathComponent[0].upper() + pathComponent[1:] for pathComponent in pathComponents if pathComponent != ""]

    return "_".join(words)

def makeCamelCase(snakeCaseString):
    return re.sub("_(.)",lambda x:x.group(1).upper(), snakeCaseString)

def makePascalCase(snakeCaseString):
    camelCase = makeCamelCase(snakeCaseString)
    return camelCase[0].upper() + camelCase[1:]

def pathToPropertyInterpolation(path):
    return path.replace("{", "\(").replace("}", ")")