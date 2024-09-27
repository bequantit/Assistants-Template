from Assistant.Assistant import Assistant

assistant = Assistant()

print("Assistant: Hola, cual es tu nombre?")
message = input("User: ")
reply, thread = assistant.reply(message)

while True:
    print("Assistant:", reply)
    message = input("User: ")
    reply, thread = assistant.reply(message, thread)