import logging
from dotenv import load_dotenv
import asyncio
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    cli,
)
from livekit.agents import room_io
from livekit.plugins import google
from livekit.agents import function_tool, RunContext

from groq_search import web_search_assistant

load_dotenv(".env.local")

logger = logging.getLogger("vision-assistant")


class VideoAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="You are a helpful voice assistant with live video input from your user.",
            llm=google.realtime.RealtimeModel(
                voice="Puck",
                temperature=0.8,
            ),
        )

    @function_tool
    async def lookup_weather(self, context: RunContext, location: str):
        """Use this tool to look up current weather information in the given location.

        If the location is not supported by the weather service, the tool will indicate this. You must tell the user the location's weather is unavailable.

        Args:
            location: The location to look up weather information for (e.g. city name)
        """

        logger.info(f"Looking up weather for {location}")

        return "sunny with a temperature of 70 degrees."

    @function_tool()
    async def search_the_web(
        self,
        context: RunContext,
        query: str,
    ) -> str:
        """
        Use this tool to search the web.
        Just put some search query in here and the function will respond
        with a summary from the web

        If the response turns out empty or blank,
        return a message telling the user that no response was found.
        """

        # --- MAIN WORK (runs web search + summary) ---
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, lambda: web_search_assistant(query)
            )
        except Exception as e:
            result = f"Search failed: {str(e)}"

        # --- Handle empty or blank responses ---
        if not result or not result.strip():
            return f"No information was found for the query: \"{query}\"."

        print(result)

        return result


server = AgentServer()


@server.rtc_session()
async def my_agent(ctx: JobContext):
    session = AgentSession(
        # If you want audio conversation, add STT + TTS here.
    )

    await session.start(
        agent=VideoAssistant(),
        room=ctx.room,
        room_options=room_io.RoomOptions(
            video_input=room_io.VideoInputOptions()
        ),
    )

    await session.generate_reply(
        instructions="Greet the user tell them your name and offer your assistance."
    )

    await ctx.connect()


def entrypoint():
    return server


if __name__ == "__main__":
    cli.run_app(entrypoint())
