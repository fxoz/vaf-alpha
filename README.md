# `vaf-alpha` Voice Assistant Framework

The goal for this project is to create a voice assistant that can perform various tasks. In the end, this codebase will probably be wrapped inside of an API, and we will have a separate client (Android, iOS, desktop, etc.) that interacts with the API. For now, however, we will focus on the core functionality of the assistant itself.

Core principles:

- **Modularity & customizability**: Skills are split into easily extensible modules using an uncluttered OOP approach.
- **Speed**: From the start, multiple benchmarks have been conducted to find the fastest models for each task.
- **Cost**: Similarly, cost is a major factor in the choice of models and APIs. The assistant should be affordable to run, even with frequent usage.
- **Intelligence**: Finding a model that's both fast, affordable, and intelligent has been a major challenge. One way to work around this is i.e. the "deep thinking" skill, which uses a slower but more intelligent model for complex questions and tasks, while faster models can be used for simpler queries.
- **Privacy**: In the future, the assistant should be able to run almost entirely locally using self-hosted AI models. At the very least, GDPR-compliant cloud API providers should be used. Self-hostability wasn't a core goal in the beginning, because of 1) costs 2) speed 3) complexity, whereas the first two are likely easier to work with with serverless APIs without cold starts.
- **API**: In the long run, an API will be developed so this assistant can be used by different clients and devices.

## Roadmap

- [x] **Context** of previous question(s)
- [x] **Skills** (e.g. calendar, weather, music, etc.)
  - [x] **(Long-Term) Memory**
    - [x] List/write/read
    - [ ] Append
  - [x] **Date and Time**
    - [x] Get Unix timestamp
    - [x] Get local weekday, date and time
  - [x] **Windows API (Media Playback)**
    - [x] Pause/resume
    - [x] Next/previous track
    - [x] Volume: change
  - [x] **OCR**
    - [x] Screenshot
    - [x] Multimodal LLM analysis, with custom prompt support
  - [x] **Spotify**
    - [x] Get currently playing track
    - [x] Search for a track, album, or artist
    - [x] Play a track
    - [x] Next, pause, resume
    - [x] Change volume
    - [ ] Autoplay similar songs
      - Deprecated `reccobeats.com` (which is using Spotify's recommendation system in the backend), because there seems to be something severely broken with it. For example, [Digital Bath by Deftones](https://open.spotify.com/track/2jSJm3Gv6GLxduWLenmjKS?si=c6d9a7de14234ebb) (Alternative Metal) recommends only two(!) metal songs, the rest being Polish hyperpop, Korean as well as Latin pop, German conscious rap and other fully unrelated genres. I've tested this several times, with similarily dissapointing results.
    - [ ] Change device
    - [ ] Play personal playlist
  - [x] **Autonomous Browser Agent** (self-written)
    - Deprecated multimodal LLM OCR for this because of very disappointing results: coordinates can not be estimated reliably whatsoever, neither normalized nor absolute coordinates.
    - [x] High-stealth browser
    - [x] Autonomously open websites and fetch ARIA tree
    - [x] Click buttons, fill out inputs/forms
    - [ ] OCR
  - [ ] **Deep Thinking** (use a better AI for complex questions and tasks)
  - [ ] **Timer & Alarm**
  - [ ] **Calendar**
  - [ ] **Email** (with major focus on privacy!)
  - [ ] **Weather**
  - [ ] **News**
  - [ ] **Finance**
  - [ ] **Last.fm** (for music recommendations based on listening history)
  - [ ] **AlbumOfTheYear (AOTY)** (for high quality music recommendations)
  - [ ] **Custom music algoritm** (requires AOTY and/or Last.fm integration! e.g. "play my favourite Deftones song")
- [ ] **Auto-Retry** (change the model for 429s etc.)
- [ ] **Error Handling** (e.g. if a skill fails, the assistant should be able to handle it gracefully and inform the user)
- [ ] **Hotword** (for 'waking up' the assistant)
- [ ] **Barge-in** (interupting the assistant while it's speaking)
- [ ] **Multi-User-Support** (different users can have different skill storages etc.)
- [ ] **API** (important, but needs time)


## Model Overview

**Ratings:** 🔵 excellent 🟢 very good 🟡 okay 🟠 bad 🔴 critical ❔ untested/unsure

End to end latency includes processing time. Ranges can vary significantly based on input length, server load, and other factors.

For TTS: if streaming is supported, latency is measured until the first audio chunk is received. If not, it's measured until the entire audio is received.

**KWS** = Keyword Spotting (wake word detection), **ASR** = Automatic Speech Recognition, **LLM** = Large Language Model, **OCR** = Optical Character Recognition, **TTS** = Text-to-Speech

<div style="overflow-x: scroll;">

| Task | Provider     | Model                | Cost                               | E2E Latency | Notes                               |
| ---- | ------------ | -------------------- | ---------------------------------- | ----------- | ----------------------------------- |
| KWS  | PicoVoice    | ❔ Porcupine          | ❔ Likely costly commercial license | ❔           | *Only* for businesses AFAIK         |
| KWS  | OpenWakeWord | ❔ -various-          | 🔵 Free (local)                     | 🔵 excellent | ~100-200 MB RAM usage               |
| ASR  | DeepInfra    | 🟢 Voxtral Mini 3B    | 🟢 $0.0030/min                      | 🔴 2s        | Too slow                            |
| ASR  | Mistral      | 🟢 Voxtral Mini       | 🟢 $0.001/min + $0.04/M out tokens  | 🟡 0.45-0.9s | Needs more quality testing          |
| LLM  | Cerebras     | 🟡 GPT OSS 120b       | 🟢 $0.35/M tokens                   | 🔴 2.5s-3s   | SOTA TPS speeds, but high latency   |
| LLM  | OpenRouter   | 🟠 GPT OSS 20b (Groq) | 🟢 $0.1875/M blended                | 🟢 0.4-0.7s  | Good latency, but low intelligence  |
| LLM  | OpenRouter   | 🔴 Qwen 3.5 Flash     | 🟢 $0.0001/prompt approx.           | 🟢 0.4-0.7s  | Good latency, but low intelligence  |
| LLM  | ?            | 🔴 Qwen 3.5 4B        | 🟢 Very cheap                       | ❔(low)      | Not supported by OpenRouter         |
| OCR  | OpenRouter   | 🟢 Gemini 3.1 Flash   | 🟢 $0.00031/img approx.             | 🔴 3-3.8s    | Didn't find a quicker in OpenRouter |
| TTS  | DeepInfra    | 🟢 Kokoro 82M         | 🟢 $0.7440/M chars                  | 🔴 1.5–2.5s  | No mid-sentence language switching  |
| TTS  | SAPI5        | 🟠 Microsoft David    | 🔵 Free (local)                     | 🔵 instant   | Very fast, but robotic voice        |
| TTS  | Async.com    | 🟢 Async Flash 1.0    | 🟠 $0.5/h                           | 🟢 0.6-0.7s  | Streamed response                   |

</div>

*Info (especially pricing) may be inaccurate or outdated!*

Pricing links:

- [Mistral](https://mistral.ai/pricing#api)
- [InWorld](https://inworld.ai/pricing)
- [Async.com](https://async.com/pricing)
- [Cerebras](https://www.cerebras.ai/pricing)
- [DeepInfra](https://deepinfra.com/pricing)
- [Together: Kokoro](https://www.together.ai/models/kokoro-82m)

### Keyword Spotting (KWS)

Find a model with a high step count, low FA/H (false accepts per hour of random noise/speech), high recall on [openwakeword.com/library](https://openwakeword.com/library). I chose "Hey, Nexus" with 100k+ steps, 2.1 FA/H and 92.8% recall:

- [**405 KB ONNX Download**](https://openwakeword.com/api/models/555/download?format=onnx)
- Save as `models/kws/_hey-nexus.onnx`

I gitignored it because of license uncertainties.

## Skills

Skills are external abilities of the AI agent: fetching the current time (`dateandtime`), reading/writing notes (`memory`), etc.

### Developing Skills

Skills are contained in  `src/skills`.

- Use the `Skill` base class to create new skills. 
- `self.get_skill_storage_folder() -> str` provides a dedicated folder for the skill to store files, if needed. 
- Use `_security.validate_name(name: str)` for folders, files etc. to prevent path traversal and other security issues.

The AI needs to know which skills are available and how to call them. Thus, it is crucial to:

- Heavily utilize type hinting in your method signatures whenever possible
- Use docstrings to explain the methods of the skill.
  - The LLM can NOT read the source code or understand the function's logic. Pretend the LLM is of very low intelligence.
  - I've been experimenting with very direct and cautious statements in skill method docstrings like "ONLY run this method/tweak this parameter if the user explicitly asks for it" to avoid lower-intelligence LLMs from mistakenly calling unnecessary tools.
- Use very descriptive names for methods and parameters.

### Testing Skills

To test a skill, you can use the following command:

```bash
uv run python -m src.skills.myskillmodule
```

Getting `ModuleNotFoundError`s? It's a tiny bit hacky, but try:

```bash
$env:PYTHONPATH = "src"
```

...to tell Python where to look for modules, and try again.

### Skill Ambiguity

Especially LLMs with lower intelligence might be unsure which skill to call. For example, "resume the song" can be done using Spotify or the Windows Media Control skill, which is ambiguous in human language. Thus, it is advisable to:

- Disable all but the relevant skills when testing.
- Make the method names and docstrings very descriptive.
- Most importantly, utilize the system prompt to inform the LLM about when to use which skill.

###

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

## Agent Pipeline

Whenever a prompt is received, the agent processes it in the following way:
- Prompt the LLM with recent (`config.RECENT_MESSAGES_LIMIT`) conversation context (including the prompt) and system prompt.
- The LLM can then either answer the question directly, or call a tool (i.e. a skill method) if it needs more information to answer the question.
- Is there any tool call? No, then answer the question directly and quit.
- Yes, then call the tool and get the result.
- Prompt the LLM again, but this time with the tool result included in the context. The LLM can then answer the question using the tool result, or call another tool if needed.

This loop continues either until `config.CONSECUTIVE_TOOL_CALL_LIMIT` is reached or the LLM decides to answer the question without calling another tool.


`agent.py` is useful for testing the agent without tedious voice input, transcription and TTS. It also prints the tool calls etc.

Usage:
```bash
uv run .\src\agent.py your prompt here
```

Example:

```py
PS C:\Users\Felix\Desktop\vaf-alpha> uv run .\src\agent.py play be quiet and drive away by deftones

SpotifySkill__search_anything{'query': 'be quiet and drive away deftones'}
-> {'tracks': [{'id': '4Uiw0Sl9yskBaC6P4DcdVD', 'name': 'Be Quiet and Drive (Far Away)', 'artists': 'Deftones'}, {'id': '2QeutlLcJf2V1cMUUsDFT1', 'name': 'Lotus Flower', 'artists': 'Radiohead'}, {'id': '3RpH7WXnV4fV5p8zo8JV9R', 'name': 
'SEE OR HATE', 'artists': 'MakSmooth'}], 'artists': [{'id': '6Ghvu1VvMGScGpOUJBAHNH', 'name': 'Deftones'}, {'id': '05fG473iIaoy82BF1aGhL8', 'name': 'Slipknot'}, {'id': '3RNrq3jvMZxD9ZyoOZbQOD', 'name': 'Korn'}], 'albums': [{'id': 
'7o4UsmV37Sg5It2Eb7vHzu', 'name': 'Around the Fur', 'artists': 'Deftones'}, {'id': '1GjjBpY2iDwSQs5bykQI5e', 'name': 'Diamond Eyes', 'artists': 'Deftones'}, {'id': '5LEXck3kfixFaA3CqVE7bC', 'name': 'White Pony', 'artists': 'Deftones'}]}
SpotifySkill__play_track_id{'track_id': '4Uiw0Sl9yskBaC6P4DcdVD'}
-> None
"LLM: I found and played 'Be Quiet and Drive (Far Away)' by Deftones."


PS C:\Users\Felix\Desktop\vaf-alpha> uv run .\src\agent.py louder!

WindowsApiSkill__volume_up{}
-> None
"LLM: I have turned up the volume for you."
```