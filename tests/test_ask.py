from types import SimpleNamespace

from app import ask


class FakeChat:
    def __init__(self):
        self.questions = []

    def send_message(self, question):
        self.questions.append(question)
        return SimpleNamespace(
            text=f"回答: {question}",
            usage_metadata=SimpleNamespace(
                prompt_token_count=3,
                candidates_token_count=2,
            ),
        )


class FakeChats:
    def __init__(self, chat):
        self.chat = chat
        self.models = []

    def create(self, model):
        self.models.append(model)
        return self.chat


class FakeClient:
    def __init__(self, chat):
        self.chats = FakeChats(chat)


def test_main_keeps_chat_history_for_follow_up_questions(monkeypatch, capsys):
    chat = FakeChat()
    client = FakeClient(chat)
    monkeypatch.setattr(ask.genai, "Client", lambda api_key: client)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("sys.argv", ["app.ask", "最初の質問"])
    inputs = iter(["続けて質問", "exit"])

    ask.main()

    assert chat.questions == ["最初の質問", "続けて質問"]
    assert client.chats.models == [ask.MODEL]
    output = capsys.readouterr().out
    assert "回答: 最初の質問" in output
    assert "回答: 続けて質問" in output
    assert output.count("[usage]") == 2
