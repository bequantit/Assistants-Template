import os
import json
import time
from dotenv import load_dotenv
from Assistant.functions.extract_information import extract_information_definition
from openai import OpenAI

load_dotenv("Assistant/.env")

ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SLEEP_TIME_BETWEEN_RETRIEVALS = 1


class Assistant:
    def __init__(self):
        self.id = ASSISTANT_ID
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY, timeout=20)

        with open("Assistant/instructions.txt") as file:
            self.instructions = file.read()

        self.functions = {
            extract_information_definition["name"]: extract_information_definition,
        }

        self.tools = []
        for function_name, function in self.functions.items():
            self.tools.append({"type": "function", "function": function["schema"]})

        self.openai_client.beta.assistants.update(
            assistant_id=self.id,
            instructions=self.instructions,
            tools=self.tools,
        )

    def _submit_functions_output(self, run, thread, function_outputs):
        run = self.openai_client.beta.threads.runs.submit_tool_outputs(
                run_id=run.id,
                thread_id=thread.id,
                tool_outputs=function_outputs,
            )
        return run
        

    def _get_function_calls(self, run):
        function_calls = []
        for tool_call in run.required_action.submit_tool_outputs.tool_calls:
            if tool_call.type == "function":
                function_calls.append(
                    {
                        "id": tool_call.id,
                        "name": tool_call.function.name,
                        "arguments": json.loads(tool_call.function.arguments),
                    }
                )
        return function_calls

    def _get_last_message(self, thread):
        messages = self.openai_client.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value

    def _create_thread(self):
        thread = self.openai_client.beta.threads.create()
        return thread

    def _create_message(self, message, thread):
        self.openai_client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message,
        )

    def _create_run(self, thread):
        run = self.openai_client.beta.threads.runs.create(
            assistant_id=self.id,
            thread_id=thread.id,
        )
        return run

    def _retrieve_run(self, run, thread):
        run = self.openai_client.beta.threads.runs.retrieve(
            run_id=run.id,
            thread_id=thread.id,
        )

        while run.status not in ["completed", "requires_action", "failed"]:
            run = self.openai_client.beta.threads.runs.retrieve(
                run_id=run.id,
                thread_id=thread.id,
            )
            time.sleep(SLEEP_TIME_BETWEEN_RETRIEVALS)

        return run

    def call_function(self, function_name, parameters):
        function_ = self.functions[function_name]
        return function_(**parameters)

    def reply(self, message, thread=None):
        if thread is None:
            thread = self._create_thread()

        self._create_message(message, thread)
        run = self._create_run(thread)
        run = self._retrieve_run(run, thread)

        while run.status == "requires_action":
            
            outputs = []
            function_calls = self._get_function_calls(run)
            for function_call in function_calls:
                call_id = function_call["id"]
                function_name = function_call["name"]
                arguments = function_call["arguments"]
                
                output = self.functions[function_name]["executable"](**arguments)
                outputs.append({"tool_call_id": call_id, "output": output})
                
            run = self._submit_functions_output(run, thread, outputs)
            run = self._retrieve_run(run, thread)

        if run.status == "completed":
            reply = self._get_last_message(thread)

        return reply, thread
