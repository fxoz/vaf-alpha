import os

from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

load_dotenv()

client = Cerebras(
    api_key=os.environ["CEREBRAS_KEY"],
)


def respond(text: str) -> str:
    res = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Answer in a very concise manner. NEVER use markdown, emojis, lists, asterisks, emphasis, code blocks, or ANY kind of formatting! This is extremely important, just write plain text for Text-to-Speech! Unless explicitly asked, respond with a few short sentences at most!",
            },
            {"role": "user", "content": text},
        ],
        model="gpt-oss-120b",
        stream=False,
        max_completion_tokens=1024,
        temperature=0.2,
        top_p=1,
        reasoning_effort="medium",
    )

    # ChatCompletionResponse(id='chatcmpl-be0e66cc-aa0b-4ff1-bf04-6e4858cff65e', choices=[ChatCompletionResponseChoice(finish_reason='stop', index=0, message=ChatCompletionResponseChoiceMessage(role='assistant', content='The deepest point on Earth—Challenger Deep in the Mariana Trench—is over 11\u202fkm (7\u202fmi) below sea level, yet its pressure is only about 1% of the pressure at the core of the planet.', reasoning='We need to answer concisely. Provide an interesting fact about the world. Keep it short.', tool_calls=None), logprobs=None, reasoning_logprobs=None)], created=1774311791, model='gpt-oss-120b', object='chat.completion', system_fingerprint='fp_2d389d34367dd22b92f3', time_info=ChatCompletionResponseTimeInfo(completion_time=0.061507115, prompt_time=0.003011942, queue_time=0.007044776, total_time=0.07758045196533203, created=1774311791.2570376), usage=ChatCompletionResponseUsage(completion_tokens=79, completion_tokens_details=ChatCompletionResponseUsageCompletionTokensDetails(accepted_prediction_tokens=0, rejected_prediction_tokens=0, reasoning_tokens=0), prompt_tokens=88, prompt_tokens_details=ChatCompletionResponseUsagePromptTokensDetails(cached_tokens=0), total_tokens=167), service_tier=None)
    return res.choices[0].message.content.strip()


if __name__ == "__main__":
    respond("Say something interesting about the world.")
