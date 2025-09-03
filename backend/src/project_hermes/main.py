#!/usr/bin/env python
from random import randint
import os
import sys
from typing import Optional

# Ensure package root (backend/src) is on path when executed directly
_pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
src_dir = os.path.join(_pkg_root, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from project_hermes.crews.poem_crew.poem_crew import PoemCrew


class PoemState(BaseModel):
    topic: str = ""
    sentence_count: int = 1
    poem: str = ""


class PoemFlow(Flow[PoemState]):
    @start()
    def generate_sentence_count(self) -> None:
        print("Generating sentence count")
        # Allow deterministic override via env for testing
        override = os.getenv("POEM_SENTENCE_COUNT")
        if override and override.isdigit():
            self.state.sentence_count = max(1, min(20, int(override)))
        else:
            self.state.sentence_count = randint(1, 5)

    @listen(generate_sentence_count)
    def generate_poem(self) -> None:
        print("Generating poem")
        try:
            result = (
                PoemCrew()
                .crew()
                .kickoff(
                    inputs={
                        "sentence_count": self.state.sentence_count,
                        "topic": self.state.topic,
                    }
                )
            )
            raw = getattr(result, "raw", str(result))
            print("Poem generated", raw)
            self.state.poem = raw
        except Exception as e:  # broad catch to keep flow alive
            print(f"Error generating poem: {e}", file=sys.stderr)
            self.state.poem = "<error generating poem>"

    @listen(generate_poem)
    def save_poem(self) -> None:
        print("Saving poem")
        try:
            with open("poem.txt", "w", encoding="utf-8") as f:
                f.write(self.state.poem)
        except OSError as e:
            print(f"Failed to write poem.txt: {e}", file=sys.stderr)


def kickoff(prompt: str) -> str:
    """Run the poem flow for a given prompt/topic and return the poem text."""
    poem_flow = PoemFlow()
    # Ensure state includes topic before kicking off
    poem_flow.state.topic = prompt
    poem_flow.kickoff()
    return poem_flow.state.poem


def plot() -> None:
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    # Allow topic via CLI arg or env, fallback to default
    topic_arg: Optional[str] = None
    if len(sys.argv) > 1:
        topic_arg = " ".join(sys.argv[1:]).strip()
    if not topic_arg:
        topic_arg = os.getenv("POEM_TOPIC", "crewai & gemini integration")
    print(f"Running poem flow for topic: {topic_arg}")
    print(kickoff(topic_arg))
