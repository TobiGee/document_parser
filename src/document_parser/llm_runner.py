from openai import OpenAI


class LLMRunner:
    def __init__(self, model="openai") -> None:
        if model == "llava":
            self._OPEN_AI_CLIENT = OpenAI(
                base_url="http://localhost:8000/v1", api_key="sk-1234"
            )
        elif model == "openai":
            self._OPEN_AI_CLIENT = OpenAI()

    def run(self, request: str):
        completion = self._OPEN_AI_CLIENT.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": request}],
        )
        return completion.choices[0].message.content


if __name__ == "__main__":
    runner = LLMRunner()
    print(runner.run("Plase tell me why im the best"))
