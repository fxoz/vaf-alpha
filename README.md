# `vaf-alpha` Voice Assistant

- [x] **Context** of previous question(s)
- [x] **Skills** (e.g. calendar, weather, music, etc.)
  - [ ] **Deep Thinking** (use a better AI for complex questions and tasks)
  - [ ] **Spotify**
  - [ ] **Last.fm**
    - [ ] **Custom algoritm** (e.g. "play something I haven't listened to in a while")
- [ ] **Auto-Retry** (change the model for 429s etc.)
- [ ] **Error Handling** (e.g. if a skill fails, the assistant should be able to handle it gracefully and inform the user)
- [ ] **Hotword** (for 'waking up' the assistant)
- [ ] **Barge-in** (interupting the assistant while it's speaking)
- [ ] **Multi-User-Support** (different users can have different skill storages etc.)
- [ ] **API** (important, but needs time)

## Model Overview

**Ratings:** 🔵 excellent 🟢 very good 🟡 okay 🟠 bad 🔴 critical

End to end latency includes processing time. Ranges can vary significantly based on input length, server load, and other factors.

For TTS: if streaming is supported, latency is measured until the first audio chunk is received. If not, it's measured until the entire audio is received.

| Task | Provider   | Model                  | Cost                                 | E2E Latency  | Notes                              |
| ---- | ---------- | ---------------------- | ------------------------------------ | ------------ | ---------------------------------- |
| ASR  | DeepInfra  | 🟢 Voxtral-Mini-3B-2507 | 🟢 $0.0030/min                        | 🔴 2s         | Too slow                           |
| ASR  | Mistral    | 🟢 voxtral-mini-latest  | 🟢 $0.001/min + $0.04/M output tokens | 🟡 0.45-0.9s  | Needs more quality testing         |
| LLM  | Cerebras   | 🟡 gpt-oss-120b         | 🟢 $0.35/M tokens                     | 🔴 2.5s-3s    | SOTA TPS speeds, but high latency  |
| LLM  | OpenRouter | 🟠 gpt-oss-20b (Groq)   | 🟢 $0.1875/M blended                  | 🟢 0.4-0.7s   | Good latency, but low intelligence |
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


## Development Notes

- I am not using the [Conversation State API](https://developers.openai.com/api/docs/guides/conversation-state) using `previous_response_id`, since OpenAI claims:
  > Even when using `previous_response_id`, **all previous input tokens** for responses in the chain **are billed as input tokens** in the API.

  This makes longer conversations very expensive. Instead, we specify a `RECENT_MESSAGES_LIMIT` in `config.py`, which keeps only the last $N$ messages in the conversation history, plus the system prompt.
