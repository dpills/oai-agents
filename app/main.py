import asyncio
from typing import Any

import orjson
from agents import (
    Runner,
    enable_verbose_stdout_logging,
    set_default_openai_client,
    set_tracing_disabled,
    trace,
)
from openai.types.responses import (
    EasyInputMessageParam,
    ResponseFunctionToolCall,
    ResponseInputItemParam,
    ResponseTextDeltaEvent,
)

from .agents import supervisor_agent
from .clients import openai_client
from .config import config
from .log import log

set_default_openai_client(client=openai_client)


if config.openai_verbose_logging:
    log.info("Verbose Logging Enabled")
    enable_verbose_stdout_logging()  # type: ignore

# Azure config
if config.openai_base_url:
    set_tracing_disabled(True)


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

                elif event.type == "agent_updated_stream_event":
                    print(f"Agent updated: {event.new_agent.name}")

                elif event.type == "run_item_stream_event":
                    if event.item.type == "tool_call_item" and isinstance(
                        event.item.raw_item, ResponseFunctionToolCall
                    ):
                        call_id = event.item.raw_item.call_id
                        name = event.item.raw_item.name
                        args = orjson.loads(event.item.raw_item.arguments)

                        tool_calls[event.item.raw_item.call_id] = {
                            "name": name,
                            "arguments": args,
                        }

                        print(f"TOOL - {name} ({call_id}): {args}")
                    elif event.item.type == "tool_call_output_item":
                        if result_call_id := event.item.raw_item.get("call_id"):
                            tool_call = tool_calls.get(result_call_id)
                            if tool_call:
                                if tool_call["arguments"]:
                                    print(
                                        f"TOOL: {tool_call['name']} - {tool_call['arguments']} \n\n {event.item.output}"  # noqa: E501
                                    )
                                else:
                                    print(
                                        f"TOOL: {tool_call['name']} \n\n {event.item.output}"  # noqa: E501
                                    )

            convo_msgs = result.to_input_list()


if __name__ == "__main__":
    asyncio.run(main())
