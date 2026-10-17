from pydantic import BaseModel

class TraceEvent(BaseModel):
    run_id: str
    step: int
    agent: str
    input: str
    output: str
    model: str
    latency_ms: float
    timestamp: str


event = TraceEvent(
    run_id="run_001", 
    step=1,
    agent="extractor",
    input="invoice 1 raw text",
    output="{...}",
    model="gemini-3.8-flash",
    latency_ms=812.5,
    timestamp="2026-10-14T14:50:00Z"
    )

line = event.model_dump_json()
print(line)
print(event)

with open("traces/test.jsonl", "a", encoding="utf-8") as f:
    f.write(line + "\n")