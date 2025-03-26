import asyncio
from typing import Any

import orjson
from agents import (
    Runner,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
    trace,
)
from openai.types.responses import (
    EasyInputMessageParam,
    ResponseFunctionToolCall,
    ResponseInputItemParam,
    ResponseOutputItemAddedEvent,
    ResponseTextDeltaEvent,
)

from .agents import supervisor_agent
from .clients import openai_client
from .config import config

set_default_openai_client(client=openai_client)

# Azure config
if config.openai_base_url:
    set_tracing_disabled(True)
    set_default_openai_api("chat_completions")


async def main() -> None:
    """
    OpenAI Agents
    """
    convo_msgs: list[ResponseInputItemParam] = []
    tool_calls: dict[str, Any] = {}

    with trace(workflow_name="Conversation", group_id="1"):
        while True:
            user_input = input("📝: ").strip()
            if not user_input or user_input.lower() == "q":
                break

            result = Runner.run_streamed(
                starting_agent=supervisor_agent,
                input=[
                    *convo_msgs,
                    EasyInputMessageParam(role="user", content=user_input),
                ],
                max_turns=20,
            )

            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(
                    event.data, ResponseTextDeltaEvent
                ):
                    print(event.data.delta, end="", flush=True)
                elif (
                    event.type == "raw_response_event"
                    and isinstance(event.data, ResponseOutputItemAddedEvent)
                    and isinstance(event.data.item, ResponseFunctionToolCall)
                    and not event.data.item.name.startswith("transfer_to_")
                ):
                    print(f"TOOL CALL: {event.data.item.name}")
                elif (
                    event.type == "run_item_stream_event"
                    and event.name == "tool_called"
                ):
                    args = None
                    if event.item.raw_item.arguments:
                        args = orjson.loads(event.item.raw_item.arguments)

                    tool_calls[event.item.raw_item.call_id] = {
                        "name": event.item.raw_item.name,
                        "arguments": args,
                    }
                elif (
                    event.type == "run_item_stream_event"
                    and event.name == "tool_output"
                ):
                    call_id = event.item.raw_item["call_id"]
                    if call_id and isinstance(call_id, str):
                        tool_call = tool_calls.get(call_id)
                        if tool_call:
                            if tool_call["arguments"]:
                                print(
                                    f"TOOL: {tool_call['name']} - {tool_call['arguments']} \n\n {event.item.raw_item['output']}"  # noqa: E501
                                )
                            else:
                                print(
                                    f"TOOL: {tool_call['name']} \n\n {event.item.raw_item['output']}"  # noqa: E501
                                )
                        else:
                            print(f"TOOL: {event.item.raw_item['output']}")

            print()

            convo_msgs = result.to_input_list()


if __name__ == "__main__":
    asyncio.run(main())
