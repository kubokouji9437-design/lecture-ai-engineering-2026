"""第1回: 素のLLMと会話するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 講座に固有の質問から会話を始める

ツールは持たないが、同じチャットセッションで会話履歴を保つ。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai.chats import Chat
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(chat: Chat, question: str) -> str:
    response = chat.send_message(question)

    usage = response.usage_metadata
    input_tokens = usage.prompt_token_count if usage is not None else None
    output_tokens = usage.candidates_token_count if usage is not None else None
    print(
        f"[usage] input={input_tokens if input_tokens is not None else '不明'} "
        f"output={output_tokens if output_tokens is not None else '不明'}"
    )

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMと会話する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    try:
        client = genai.Client(api_key=get_api_key())
        chat = client.chats.create(model=MODEL)
        question = args.question

        while True:
            print(f"[質問] {question}\n")
            print(ask(chat, question))
            try:
                while True:
                    question = input("\n次の質問（終了するには exit）: ").strip()
                    if question.lower() in {"exit", "quit", "q", "終了"}:
                        return
                    if question:
                        break
                    print("質問を入力してください。")
            except EOFError:
                print()
                break
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
