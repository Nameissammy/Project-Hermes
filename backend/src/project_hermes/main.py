#!/usr/bin/env python
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

try:
    from project_hermes.crews.poem_crew.poem_crew import PoemCrew
except ModuleNotFoundError:  # give user a helpful message
    if __name__ == "__main__":
        print(
            (
                "Could not import 'project_hermes'. Install editable (cd backend && "
                "uv pip install -e .) or run with: uv run -m project_hermes.main '<topic>'"
            ),
            file=sys.stderr,
        )
    raise

logger = logging.getLogger("project_hermes.flow")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")


class PoemState(BaseModel):
    topic: str = ""
    sentence_count: int = 1
    poem: str = ""
    model_used: str | None = None
    attempts: int = 0
    error_message: str | None = None
    success: bool = True


class PoemFlow(Flow[PoemState]):
    @start()
    def generate_sentence_count(self) -> None:
        logger.info("Generating sentence count")
        # Allow deterministic override via env for testing
        override = os.getenv("POEM_SENTENCE_COUNT")
        if override and override.isdigit():
            self.state.sentence_count = max(1, min(20, int(override)))
        else:
            self.state.sentence_count = randint(1, 5)

    @listen(generate_sentence_count)
    def generate_poem(self) -> None:
        logger.info(
            "Generating poem (topic='%s', sentence_count=%s)",
            self.state.topic,
            self.state.sentence_count,
        )
        if os.getenv("POEM_FORCE_ERROR"):
            logger.warning("POEM_FORCE_ERROR set; simulating failure before LLM call")
            self.state.success = False
            self.state.error_message = "Forced error (POEM_FORCE_ERROR=1)"
            self.state.poem = "<error generating poem>"
            return

        fake = os.getenv("POEM_FAKE_OUTPUT")
        if fake:
            logger.info("Using POEM_FAKE_OUTPUT short-circuit (len=%d)", len(fake))
            self.state.poem = fake
            self.state.model_used = "fake"
            return

        primary = os.getenv("POEM_PRIMARY_MODEL")
        fallbacks_env = os.getenv("POEM_FALLBACK_MODELS", "")
        fallback_models = [m.strip() for m in fallbacks_env.split(",") if m.strip()]
        models_chain = [primary] if primary else []
        # Always include None sentinel to use YAML default at least once
        if None not in models_chain:
            models_chain.append(None)
        for m in fallback_models:
            if m and m not in models_chain:
                models_chain.append(m)

        max_attempts = int(os.getenv("POEM_RETRY_ATTEMPTS", "3"))
        base_delay = float(os.getenv("POEM_RETRY_BASE_DELAY", "0.6"))
        transient_phrases = [
            "overloaded",
            "timeout",
            "temporarily",
            "unavailable",
            "rate limit",
            "503",
        ]

        def is_transient(err: Exception) -> bool:
            msg = str(err).lower()
            return any(p in msg for p in transient_phrases)

        last_error: Exception | None = None
        for model_override in models_chain:
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                self.state.attempts += 1
                try:
                    if model_override:
                        os.environ["POEM_MODEL_RUNTIME_OVERRIDE"] = model_override
                    elif "POEM_MODEL_RUNTIME_OVERRIDE" in os.environ:
                        del os.environ["POEM_MODEL_RUNTIME_OVERRIDE"]

                    crew_instance = PoemCrew().crew()
                    result = crew_instance.kickoff(
                        inputs={
                            "sentence_count": self.state.sentence_count,
                            "topic": self.state.topic,
                        }
                    )
                    raw = getattr(result, "raw", str(result))
                    self.state.poem = raw
                    self.state.model_used = model_override or os.getenv(
                        "POEM_LAST_AGENT_MODEL", "unknown"
                    )
                    self.state.success = True
                    logger.info(
                        "Poem generated (chars=%d, model=%s, attempts=%d)",
                        len(raw),
                        self.state.model_used,
                        self.state.attempts,
                    )
                    last_error = None
                    break  # success for this model
                except Exception as e:  # noqa: BLE001
                    last_error = e
                    self.state.success = False
                    self.state.error_message = str(e)
                    transient = is_transient(e)
                    logger.warning(
                        "Attempt %d failed for model=%s transient=%s: %s",
                        attempts,
                        model_override or "(yaml-default)",
                        transient,
                        e,
                    )
                    if attempts < max_attempts and transient:
                        sleep_for = base_delay * (2 ** (attempts - 1))
                        time.sleep(sleep_for)
                        continue
                    break  # break inner loop if not transient or maxed attempts
            if last_error is None and self.state.success:
                break  # overall success, exit model chain
            # else try next model

        if last_error is not None and not self.state.success:
            strict = os.getenv("POEM_STRICT") == "1"
            if strict:
                logger.error("All attempts failed and POEM_STRICT=1; raising error")
                raise RuntimeError(
                    f"Poem generation failed after {self.state.attempts} attempts: {last_error}"
                )
            logger.error(
                "Poem generation failed after %d attempts (last error: %s)",
                self.state.attempts,
                last_error,
            )
            self.state.poem = "<error generating poem>"

    @listen(generate_poem)
    def maybe_save_poem(self) -> None:
        if not self.state.poem or not self.state.success:
            return
        if os.getenv("POEM_SAVE") != "1":
            return
        out_dir = Path(os.getenv("POEM_OUTPUT_DIR", "poems"))
        out_dir.mkdir(parents=True, exist_ok=True)
        timestamped = os.getenv("POEM_SAVE_TIMESTAMPED", "1") == "1"
        fname_base = self.state.topic.replace(" ", "_")[:40] or "poem"
        if timestamped:
            fname = f"{fname_base}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.txt"
        else:
            fname = f"{fname_base}.txt"
        path = out_dir / fname
        path.write_text(self.state.poem)
        logger.info("Saved poem to %s", path)


def run_flow(prompt: str) -> PoemState:
    """Run the poem flow and return full state (for API/meta use)."""
    poem_flow = PoemFlow()
    poem_flow.state.topic = prompt
    poem_flow.kickoff()
    return poem_flow.state


def kickoff(prompt: str) -> str:
    """Backward compatible helper returning only poem text."""
    return run_flow(prompt).poem


def plot() -> None:
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    # Allow topic via CLI arg or env, fallback to default
    topic_arg: str | None = None
    if len(sys.argv) > 1:
        topic_arg = " ".join(sys.argv[1:]).strip()
    if not topic_arg:
        topic_arg = os.getenv("POEM_TOPIC", "crewai & gemini integration")
    logger.info("Running poem flow for topic: %s", topic_arg)
    print(kickoff(topic_arg))
