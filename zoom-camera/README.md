# 📷 zoom-camera - ラズパイ用ズームビューア

Raspberry Pi 4 + カメラモジュール用のシンプルなズーム対応ビューアツールです。Tkinter GUIで構成されており、OpenCVを使ってライブ映像を表示、ズームイン・ズームアウトを制御できます。

---

## 🧰 使用技術

- Python 3
- OpenCV
- Tkinter
- Raspberry Pi OS（Bullseye 推奨）

---

## ⚙️ 機能概要

- 📷 Piカメラからの映像をリアルタイムで表示
- ➕ ➖ ズームイン / ズームアウト ボタン
- 🔁 スムーズなフレーム更新（cv2 → Tkinter）
- 🖥️ GUI一体型アプリ

---

## ▶️ 実行方法

1. Python 3 がインストールされていることを確認
2. 必要なライブラリをインストール:

```bash
pip install opencv-python
```

3. スクリプトを実行:
```bash
python camera_zoomer.py
```

---

## 💡 今後のアップデート予定

- [ ] ズームバー（スライダー）で操作可能に
- [ ] 撮影ボタンで画像保存
- [ ] 録画機能の追加
- [ ] カメラ設定（露出・ホワイトバランス）調整

---

## 📸 スクリーンショット

*(ここにGUIの画像を追加予定)*

---

## 🙌 作者

Aziz（Ajizu456）による個人プロジェクト。

> ラズパイを使って、自分だけのツールを開発中。

GitHubスター・フォーク歓迎です！

---

**ありがとう！/ Thanks! / Terima kasih!**

