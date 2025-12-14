from tools import get_weather
from prompt import AGENT_INSTRUCTIONS
import logging

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
)
from livekit.plugins import noise_cancellation, openai, silero
from openai.types.beta.realtime.session import TurnDetection


load_dotenv(".env")
logger = logging.getLogger("agent")


class Assistant(Agent):
    def __init__(self):
        super().__init__(
            instructions=AGENT_INSTRUCTIONS,
            tools=[get_weather],
        )

    async def on_enter(self):
        await self.session.generate_reply()


def prewarm(proc: JobProcess):
    """Load models (VAD) before accepting jobs."""
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    """Main LiveKit entrypoint (console or deployed)."""
    ctx.log_context_fields = {"room": ctx.room.name}

    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            modalities=["text", "audio"],
            voice="marin",
            turn_detection=TurnDetection(
                type="semantic_vad",
                eagerness="low",
                interrupt_response=False,
            ),
        ),
    )

    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    agent = Assistant()

    await session.start(
        agent=agent,
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    print("Connecting to LiveKit room:", ctx.room.name)
    await ctx.connect()
    print("Connected successfully.")


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm, agent_name="eva")
    )
