# 体重管理 PWA アプリ

毎日の体重と摂取カロリーを記録し、目標達成をサポートする PWA(Progressive Web App)です。
スマホのホーム画面に追加するとネイティブアプリのように使えます。

## 主な機能

### 体重・食事管理
- 毎日の体重・体脂肪率の記録
- 食事ごとのカロリー記録(複数登録可)
- 1週間単位のカロリー収支管理(残り摂取可能カロリーを自動算出)
- 目標体重 / 体脂肪率 / 目標日 / 1日のカロリー目標の設定
- 体重・カロリー・体脂肪率の推移を線グラフで可視化(7/30/90日)
- 目標達成度を円形プログレスリングで表示

### その他
- ダークモード対応(ヘッダー右上ボタン or システム設定に追従)
- データのエクスポート / インポート(JSON)
- 全データの一括削除
- 完全オフライン対応(Service Worker)
- ホーム画面追加でネイティブアプリ風に動作

## ファイル構成

```
体重管理/
├── index.html          メインのHTML
├── styles.css          スタイル(モバイル最適化)
├── app.js              アプリロジック(localStorage / Chart.js)
├── manifest.json       PWA マニフェスト
├── sw.js               Service Worker(オフライン対応)
├── icons/              アプリアイコン
│   ├── icon.svg
│   ├── icon-192.png
│   ├── icon-512.png
│   └── icon-maskable.png
└── README.md
```

## 使い方(ローカル動作)

PWA を正しく動作させるには、HTTP サーバー経由でアクセスする必要があります(`file://` ではダメ)。

### 方法1: Python(最も簡単)

```powershell
cd "C:\Users\hiu\Desktop\記録\体重管理"
python -m http.server 8080
```

ブラウザで `http://localhost:8080` を開く。

### 方法2: Node.js

```powershell
cd "C:\Users\hiu\Desktop\記録\体重管理"
npx --yes http-server -p 8080 -c-1
```

### 方法3: PowerShell ワンライナー

`start.ps1` または下記コマンド

```powershell
cd "C:\Users\hiu\Desktop\記録\体重管理"; npx --yes http-server -p 8080 -c-1
```

## スマホで開く方法

### 同一Wi-Fi 経由で見る

1. PC で上記の方法でサーバーを立てる
2. PC の IP を確認する(`ipconfig` で `IPv4 Address`)
3. スマホで `http://<PCのIP>:8080` を開く
   - 例: `http://192.168.1.10:8080`
4. ホーム画面に追加:
   - **iOS Safari**: 共有ボタン → 「ホーム画面に追加」
   - **Android Chrome**: メニュー → 「ホーム画面に追加」

> Service Worker は `localhost` または HTTPS でのみ動作します。LAN の IP では Service Worker が動かない場合がありますが、アプリ自体は動作します。

### インターネット公開(おすすめ)

無料でホスティングできます:

- **Vercel**: フォルダごとドラッグ&ドロップで公開可能
- **Netlify**: 同上
- **GitHub Pages**: リポジトリにプッシュして Pages を有効化
- **Cloudflare Pages**: GitHub 連携で自動デプロイ

公開すれば HTTPS なので Service Worker が動作し、完全な PWA として使えます。

## データについて

- データはブラウザの `localStorage` に保存され、その端末・ブラウザにのみ残ります
- 「設定」→「エクスポート」で JSON ファイルとして書き出し、別の端末でインポート可能
- 「全データを削除」で初期化できます

## 操作のコツ

- **初回起動時**: 「設定」タブで身長・開始体重・目標体重・1日のカロリー目標を入力
- **毎日の記録**: 「記録」タブで日付を選び、体重を保存 / 食事を追加
- **クイック追加**: ホーム画面の「体重を記録」「食事を記録」ボタンですぐ入力画面へ
- **グラフ**: 「グラフ」タブで 7/30/90 日を切り替えて推移を確認

## 技術

- 純粋な HTML / CSS / JavaScript(フレームワーク不使用)
- グラフ描画: [Chart.js](https://www.chartjs.org/) 4.x
- データ保存: `localStorage`
- PWA: Service Worker(Cache-first / Network-first 自動切替)
