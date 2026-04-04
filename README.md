# `vaf-alpha` Voice Assistant

- [ ] **Hotword** (for 'waking up' the assistant)
- [ ] **Barge-in** (interupting the assistant while it's speaking)
- [ ] **Context** of previous question(s)
- [ ] **Skills** (e.g. calendar, weather, music, etc.)
- [ ] **Deep Thinking** (use a better AI for complex questions and tasks)

## Model Overview

**Ratings:** 🔵 excellent 🟢 very good 🟡 okay 🟠 bad 🔴 critical

End to end latency includes processing time. Ranges can vary significantly based on input length, server load, and other factors.

For TTS: if streaming is supported, latency is measured until the first audio chunk is received. If not, it's measured until the entire audio is received.

| Task | Provider | Model | Cost | E2E Latency | Notes |
| ---- | -------- | ----- | ---- | ----------- | ----- ||
| ASR  | DeepInfra  | 🟢 Voxtral-Mini-3B-2507 | 🟢 $0.0030/min                        | 🔴 2s         | Too slow                           |
| ASR  | Mistral    | 🟢 voxtral-mini-latest  | 🟢 $0.001/min + $0.04/M output tokens | 🟡 0.45-0.9s  | Needs more quality testing         |
| LLM  | Cerebras   | 🟡 gpt-oss-120b         | 🟢 $0.35/M tokens                     | 🔴 2.5s-3s    | SOTA TPS speeds, but high latency  |
| LLM  | OpenRouter | 🟠 gpt-oss-20b          | 🟢 $0.1875/M blended                  | 🟢 0.4-0.7s   | Good latency, but low intelligence |
| TTS  | DeepInfra  | 🟢 Kokoro-82M           | 🟢 $0.7440/M characters               | 🔴 1.5–2.5s   | No mid-sentence language switching |
| TTS  | SAPI5      | 🟠 Microsoft David      | 🔵 Free (local)                       | 🔵 instant    | Very fast, but robotic voice       |
| TTS  | Together   | 🟢 Kokoro-82M           | 🔴 $10/M chars                        | ❔ claims low | UNTESTED                           |
| TTS  | Async.com  | 🟢 Async Flash 1.0      | 🟠 $0.5/h                             | 🟢 0.6-0.7s   | Streamed response                  |

*Info (especially pricing) may be inaccurate or outdated!*

Pricing links:

- [Mistral](https://mistral.ai/pricing#api)
- [InWorld](https://inworld.ai/pricing)
- [Async.com](https://async.com/pricing)
- [Cerebras](https://www.cerebras.ai/pricing)
- [DeepInfra](https://deepinfra.com/pricing)
- [Together: Kokoro](https://www.together.ai/models/kokoro-82m)

## Benchmarks

### ASR

#### Voxstral Mini @ High Quality Studio Recording

> Jetzt zeichne ich mit meinem Mikrofon meine Sprache auf und ich kann auch so switch language, if you want to, und das Mikrofon ein bisschen näher dran und schaue, was sich entwickelt und ob die ~~Vertätigung~~ sich verändern kann und ob es in Zukunft vielleicht besser wird mit der Spracherkennung. Man muss auch sagen, jetzt bin ich recht nah dran und spreche jetzt hier rein und jetzt werde ich ein bisschen leiser und gucke, wie sich das entwickelt auf die Sprache.

#### Voxstral Mini @ 7 kbps Opus

> Jetzt zeichne ich mit meinem Mikrofon meine Sprache auf und ~~eigne mir auch so ein Switch ein, das ist für 4 Monate.~~ Und das Mikrofon ein bisschen näher dran und schaue, was sich entwickelt und ob die Qualität sich verändern kann und ob es in Zukunft vielleicht besser wird mit der Spracherkennung. Man muss auch sagen, jetzt bin ich recht nah dran und spreche jetzt hier rein und jetzt werde ich ein bisschen leiser und gucke, ~~was das~~ entwickelt auf die Sprache.
