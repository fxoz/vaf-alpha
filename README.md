# `vaf-alpha`

## Model Overview

**Quality rankings:** 🔵 excellent/SOTA 🟢 very good 🟡 okay 🟠 bad 🔴 critical

| Task | Provider  | Model                  | Cost                               | E2E Latency | Notes |
| ---- | --------- | ---------------------- | ---------------------------------- | ----------- | ----- |
| ASR  | DeepInfra | 🟢 Voxtral-Mini-3B-2507 | $0.0030/min                        | 🔴 ~2s       |       |
| ASR  | Mistral   | 🟢 voxtral-mini-latest  | $0.001/min + $0.04/M output tokens | 🟠 ~1s       |       |
| TTS  | DeepInfra | 🟢 Kokoro-82M           | 🔵 $0.7440/M characters             | 🔴 ~1.3–1.6s |       |
| LLM  | Cerebras  | 🟡 gpt-oss-120b         | $0.35/M tokens                     | 🟢 ~0.4s     |       |

*Info (especially pricing) may be inaccurate or outdated!*

Pricing links:z

- [Mistral](https://mistral.ai/pricing#api)
- [InWorld](https://inworld.ai/pricing)
- [Cerebras](https://www.cerebras.ai/pricing)
- [DeepInfra](https://deepinfra.com/pricing)

## Benchmarks

### ASR

#### Voxstral Mini @ High Quality Studio Recording

> Jetzt zeichne ich mit meinem Mikrofon meine Sprache auf und ich kann auch so switch language, if you want to, und das Mikrofon ein bisschen näher dran und schaue, was sich entwickelt und ob die ~~Vertätigung~~ sich verändern kann und ob es in Zukunft vielleicht besser wird mit der Spracherkennung. Man muss auch sagen, jetzt bin ich recht nah dran und spreche jetzt hier rein und jetzt werde ich ein bisschen leiser und gucke, wie sich das entwickelt auf die Sprache.

#### Voxstral Mini @ 7 kbps Opus

> Jetzt zeichne ich mit meinem Mikrofon meine Sprache auf und ~~eigne mir auch so ein Switch ein, das ist für 4 Monate.~~ Und das Mikrofon ein bisschen näher dran und schaue, was sich entwickelt und ob die Qualität sich verändern kann und ob es in Zukunft vielleicht besser wird mit der Spracherkennung. Man muss auch sagen, jetzt bin ich recht nah dran und spreche jetzt hier rein und jetzt werde ich ein bisschen leiser und gucke, ~~was das~~ entwickelt auf die Sprache.
