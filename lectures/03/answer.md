# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
<br>第１回のapp.askでは「コンテキストの詳細が見つからなかった」と回答したが、第３回のapp.agentでは glossary.jsonの記載を引用して回答した。<br>
- `--trace` で見えたツール呼び出し（ツール名と引数）：
<br>ツール名：search_glossary<br>
引数（１回目）：{'query': 'LoRA'}<br>
引数（２回目）：{'query': 'QLoRA'}<br>
- 1つの質問での LLM 呼び出し回数（`requests`）：２回
<br>
- 追加したツールと、docstring に書いた説明：
<br>追加したツール：make_quiz
<br>
説明：<br>
    """指定した回の用語から1つを選び、
    確認問題と答えを返す。
 
    「第2回の確認問題を出して」のように、
    復習用の問題を求められたときに使う。
    """
<br>

## 宿題
<br>
- 取り組んだレベル：基礎
- やったこと：
<br>
1. app/tool.py の search_glossary の docstring の「用語を1つだけ入れる」を「まとめて入れる」に変えた。
<br>
2. app/agent.py の INSTRUCTIONS から「必ず search_glossary で用語集を確認する」の行を消した。
<br>
- 結果：
<br>
1. ツール make_quiz が呼び出される回数が１回になった。
<br>
2. 変わらず、ツール search_glossary が呼び出された。
<br>

- 気づき・疑問：
<br>
INSTRUCTION から「必ず search_glossary で用語集を確認する」の
行を消しても、search_glossary が呼び出されたのは予想外だった。<br>
どのような仕組みでモデルがツールを呼び出す判断をしているのかが分からなかった。
