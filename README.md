# nekonote - NoxPlayer 自動化スクリプト

猫の手も借りたいあなたに。

## 初期設定

配布した ZIP を適当な場所に解凍してください。

この他、Java と NoxPlayer が必要です。

### Java

Java (JRE) が正しくインストールされていることを確認してください。コンソールで `java --version` でバージョン名が出ればokです。とりあえず openJDK 13 で確認済みですが oracle版やバージョン 8 でも動くみたいです。

- openJDK <https://jdk.java.net/13/>
- oracle <https://www.oracle.com/technetwork/java/javase/downloads/index.html>

### NoxPlayer

<https://jp.bignox.com/>

キーボードコントロール(仮想キー)のラベルが画面上にあると判定に影響するので、スクリプト動作中は透明度を下げてください。


### Windowsの場合

- 画面設定で「拡大縮小とレイアウト」を100%にしてください。そうでない場合 Nox の位置がずれて検出されます。
- Noxは "C:\Program Files (x86)\Nox\bin\Nox.exe" にインストールされているものとします。違う場合は設定ファイルを編集してください (後述)。


## 実行

1. NoxPlayer と Android アプリを起動し、適切な画面(後述)を開いてください。
2. 負荷や誤作動を減らすため関係ないアプリはできれば最小化か終了してください。
3. スクリプトを起動
  - Windows: バッチファイル(nekonote.bat)をダブルクリックまたはコマンドプロンプトで実行してください。
  - mac・Linux: ターミナルを起動して `bash nekonote.sh` を実行してください。
4. 確認画面がポップアップするので、どのような作業をするか選択してください。
5. Nox の範囲指定
  - Windows では Nox の範囲を自動検知します。このときアプリケーションの範囲に赤い枠が一瞬光るので、誤検知や誤動作が起きるときはこの範囲が合っているかを確認してください。
  - mac と Linuxでは手動でドラッグして選択する必要があります。
6. 途中で止める場合はコンソール上で Ctrl と C キーを一緒に押してください。 mac でもコマンドキーではなく Control キーを使ってください。

## 設定

`data/default.ini` を `nekonote.bat` と同じフォルダに `settings.ini` としてコピーして使ってください。 `default.ini` の上書きはしないでください。

### 一般設定

- `[Nox]`
    - `path`: Nox.exe へのファイルパス。画面範囲の自動検知に使います。デフォルトは Windows のパスになっています。空欄にすると Windows であっても手動での範囲指定に切り替わります。
- `[DEFAULT]`
    - `interval`: ゲーム画面を判定するための最短間隔(秒数)。マクロ側のアルゴリズムによって変動しますので目安程度に考えてください。

## 実行可能な作業内容

TODO

## 注意

- 自動スクリプトを実行中に他の操作はできません。
- Noxのウィンドウが移動したり、他のウィンドウが覆いかぶさると判定に失敗します。
- Noxのウィンドウの一部がPC画面からはみ出していると動作が不安定になることがあります。
- マルチモニターでは検証していません。


## 既知の不具合

### 現在の画面の検知に失敗する (ログに Current screen: unknown しか出ない)

Nox の範囲指定を手動で行った場合:

Nox の範囲指定をやり直してください。範囲指定は画像検索の範囲だけでなく Nox の画面サイズから縮尺を割り出して調整する役目もあります。
たとえばディスプレイ全体を囲ってしまうと縮尺が食い違って判定できなくなります。

Windows で Nox の範囲を自動検知させている場合:

最初に表示される赤い枠が Nox のアプリに一致していることを確認してください。
特に前述の「拡大縮小とレイアウト」の設定を確認してください。
どうしても自動検知がうまく行かない場合は設定ファイルの Nox セクションの path を空欄にしてください。自動検知がオフになります。


### 長時間動かしていると画面判定の精度が下がる

画像認識系の限界です。頻発するときは適度に休ませてください。


## その他

ライブラリの SikuliX は動作が確認できたバージョンを同梱しています。<https://raiman.github.io/SikuliX1/downloads.html> からもダウンロードできます。

音素材のクレジット

- notify.wav <http://www.orangefreesounds.com/little-christmas-bell-sound/>
- error.wav <http://www.orangefreesounds.com/error-sound/>
