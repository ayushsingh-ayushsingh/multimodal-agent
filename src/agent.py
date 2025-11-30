import logging
from livekit.agents import function_tool, RunContext
from dotenv import load_dotenv
from livekit import rtc
import asyncio
from yt import youtube_search
from groq_search import web_search_assistant
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    cli,
    inference,
    room_io,
)
from livekit.plugins import noise_cancellation, silero
from livekit.agents import AgentSession
from livekit.plugins import google
from google.genai import types
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a helpful voice AI assistant. The user is interacting with you via voice, even if you perceive the conversation as text.
            You eagerly assist users with their questions by providing information from your extensive knowledge.
            Your responses are concise, to the point, and without any complex formatting or punctuation including emojis, asterisks, or other symbols.
            You are curious, friendly, and have a sense of humor.""",
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
    
    @function_tool()
    async def search_on_youtube(
        self,
        context: RunContext,
        query: str,
    ):
        """
        Use this tool to play the first video based on a query.
        Just put some search query as an argument in this function
        and the function will navigate to the browser and search the youtube.
        """
        
        youtube_search(query)

        return


server = AgentServer()


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


@server.rtc_session()
async def my_agent(ctx: JobContext):
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    session = AgentSession(
        stt=inference.STT(
            model="assemblyai/universal-streaming", language="en"),
        # llm=inference.LLM(model="google/gemini-2.5-pro"),
        # llm=inference.LLM(model="openai/gpt-5-nano"),
        llm=inference.LLM(model="openai/gpt-4.1-mini"),
        tts=inference.TTS(
            model="cartesia/sonic-3", voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
    )

    await ctx.connect()
    await session.start(
        agent=Assistant(),
        room=ctx.room,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony()
                if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                else noise_cancellation.BVC(),
            ), video_input=room_io.VideoInputOptions()
        ),
    )

    print("\n\n\nYou can begin your conversation...\n\n\n")


if __name__ == "__main__":
    cli.run_app(server)
