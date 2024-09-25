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
        return "Ask the user for their name."
    
    if user.email is None:
        return "Ask the user for their email."
    
    if user.phone is None:
        return "Ask the user for their phone number."        
        
    return "You have successfully extracted the information. Ask the user whats their favorite color."


extract_information_definition = {
    "name": schema["name"],
    "schema": schema,
    "executable": executable,
}
