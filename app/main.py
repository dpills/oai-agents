import asyncio

from agents import (
    Runner,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
    trace,
)
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionUserMessageParam,
)
from openai.types.responses import ResponseFunctionToolCallParam, ResponseTextDeltaEvent
from openai.types.responses.response_input_item_param import FunctionCallOutput

from .agents import supervisor_agent
from .clients import openai_client

set_default_openai_client(client=openai_client)
set_tracing_disabled(True)
set_default_openai_api("chat_completions")


async def main() -> None:
    """
    OpenAI Agents
    """
    messages: list[
        ChatCompletionUserMessageParam
        | ChatCompletionAssistantMessageParam
        | ResponseFunctionToolCallParam
        | FunctionCallOutput
    ] = []

    with trace(workflow_name="Conversation", group_id="1"):
        while True:
            messages.append(
                ChatCompletionUserMessageParam(role="user", content=input("📝: "))
            )

            result = Runner.run_streamed(supervisor_agent, messages, max_turns=20)

            assistant_msg = ""
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(
                    event.data, ResponseTextDeltaEvent
                ):
                    assistant_msg += event.data.delta
                    print(event.data.delta, end="", flush=True)
                elif (
                    event.type == "run_item_stream_event"
                    and event.name == "tool_called"
                ):
                    messages.append(
                        ResponseFunctionToolCallParam(
                            type="function_call",
                            id=event.item.raw_item.id,
                            call_id=event.item.raw_item.call_id,
                            name=event.item.raw_item.name,
                            arguments=event.item.raw_item.arguments,
                            status="completed",
                        )
                    )
                elif (
                    event.type == "run_item_stream_event"
                    and event.name == "tool_output"
                ):
                    messages.append(
                        FunctionCallOutput(
                            type="function_call_output",
                            call_id=event.item.raw_item["call_id"],
                            output=event.item.raw_item["output"],
                        )
                    )

            print()

            messages.append(
                ChatCompletionAssistantMessageParam(
                    role="assistant", content=assistant_msg
                )
            )

            print()


if __name__ == "__main__":
    asyncio.run(main())
