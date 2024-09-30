schema = {
    "name": "extract_information",
    "description": "Extract information provided by the user.",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Name of the client"},
            "email": {"type": "string", "description": "email of the client"},
            "phone": {"type": "string", "description": "Phone number of the client"},
        },
        "required": [],
    },
}

class User:
    def __init__(self, name=None, email=None, phone=None):
        self.name = name
        self.email = email
        self.phone = phone

user = User()

def executable(name=None, email=None, phone=None):
    for key, value in locals().items():
        if value is not None:
            setattr(user, key, value)
            
    if user.name is None:
        return "Preguntar el nombre.\n"
    
    if user.email is None:
        return "Preguntar su email.\n"
    
    if user.phone is None:
        return "Preguntar su numero de telefono.\n"        
        
    return "Ya tenemos toda la informacion. Pedile al usuario que te pregunte algo sobre la lic. en ciencias de datos"


extract_information_definition = {
    "name": schema["name"],
    "schema": schema,
    "executable": executable,
}
