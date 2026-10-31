# 第2回 解答

## 演習

- 使ったモデル・設定（`result.json` の `config` から）：

  "config": {
    "base_model": "Qwen/Qwen3.5-0.8B",
    "revision": "2fc06364715b967f1860aea9cf38778875588b17",
    "seed": 42,
    "num_train_epochs": 20,
    "warmup_steps": 6,
    "lr": 0.0002,
    "lora_r": 16,
    "lora_alpha": 32,
    "max_seq_len": 512,
    "max_new_tokens": 96,
    "gen": {
      "do_sample": false
    }
  },

- 自分で学習を実行したか（`executed_training_myself`）：いいえ
（実行できた範囲：　）
"executed_training_myself": false
→　学習時にソースコードを変えずに実行したので「false＝いいえ」としました。

- 学習前：`format_rate` =　0.09523809523809523 / `content_rate` =　0.0
- 学習後：`format_rate` =　1.0 / `content_rate` =　0.8571428571428571
- 退行した質問：なし

- 学習後に残った失敗と、その型（根拠なしの質問に断定した / 根拠ありの質問に確認要求で逃げた / 形式の崩れ）：

No. 6：PDF 以外でも出せますか：根拠ありの質問に「記載がありません」と逃げた
No.15：成績はいつ出ますか： 根拠なしの質問にFAQ の別項目を当てて断定

- 知識を問う質問（セクション 6）の結果（学習前の分類 → 学習後の分類）と気づいたこと：
No.0：format_error → asserted
No.1：format_error → needs_review
No.2：format_error → needs_review
No.3：format_error → asserted

学習後は形式のエラーは無くなった。

- 学習で変わったこと・変わらなかったこと：

変わったこと：
　学習後は、必ず needs_review を返すようになった。 
　既知の内容に対して、学習前は answer に含まれる後しか返さないケースもあったが、学習後は期待する回答を返すようになった。

変わらなかったこと：
　学習後も、FAQにない架空の質問に対して、reviewの必要を正しく判断できなかった。

## 宿題

- 取り組んだレベル：基礎
- 変えた設定やデータ：
lora_r を 8 に変更
（lora_r = 8  // 16 -> 8）

- 結果（比較表や数字）：

＜変更前：lora_r = 16＞

format_rate: 1.0,
content_rate: 0.8571428571428571
最終ロス: 0.013894
学習時間: 59 秒

＜変更後：lora_r = 8＞

format_rate: 1.0
content_rate: 0.9047619047619048
最終ロス: 0.013275
学習時間: 221 秒

ランクを下げても回答の精度は落ちなかったが、学習の収束に時間がかかった。

- ファインチューニングが向く場面・向かない場面についての考察：

向く場面は、出力のフォーマットを守らせたいような時には向き、、
向かない場面は、未知の情報に関する推論をさせようとしても、事前学習モデル以上には性能は向上しないので、向かない。
