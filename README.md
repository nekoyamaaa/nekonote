# nekonote - NoxPlayer 自動化スクリプト

猫の手も借りたいあなたに。

画像認識によりゲーム画面からステータスを取得してあらかじめ設定したマクロを実行できます。

## 初期設定

配布した ZIP を適当な場所に解凍してください。

この他、Java と ゲームを動かすアプリケーション (NoxPlayer など) が必要です。

### Java

Java (JRE) が正しくインストールされていることを確認してください。コンソールで `java --version` でバージョン名が出ればokです。とりあえず openJDK 13 で確認済みですが oracle版やバージョン 8 でも動くみたいです。

- openJDK <https://jdk.java.net/13/>
- oracle <https://www.oracle.com/technetwork/java/javase/downloads/index.html>

### NoxPlayer

<https://jp.bignox.com/>

キーボードコントロール(仮想キー)のラベルが画面上にあると判定に影響するので、スクリプト動作中は透明度設定を変更して完全に見えなくしてください。


### Windowsの場合

- アプリの位置がずれて検出される場合、画面設定で「拡大縮小とレイアウト」を100%にしてください。
- Noxは "C:\Program Files (x86)\Nox\bin\Nox.exe" にインストールされているものとします。違う場合は設定ファイルを編集してください (後述)。


## 実行

1. Android アプリを起動し、適切な画面(後述)を開いてください。
2. 負荷や誤作動を減らすため関係ないアプリはできれば最小化か終了してください。
3. スクリプトを起動
  - Windows: バッチファイル(nekonote.bat)をダブルクリックまたはコマンドプロンプトで実行してください。
  - mac・Linux: ターミナルを起動して `bash nekonote.sh` を実行してください。
4. 確認画面がポップアップするので、どのような作業をするか選択してください。
5. Nox の範囲指定
  - Windows では Nox の範囲を自動検知します。このときアプリケーションの範囲に赤い枠が一瞬光るので、誤検知や誤動作が起きるときはこの範囲が合っているかを確認してください。
  - Nox以外のアプリケーションを使用している場合や、mac と Linuxでは手動でドラッグして選択する必要があります。
6. 途中で止める場合はコンソール上で Ctrl と C キーを一緒に押してください。 mac でもコマンドキーではなく Control キーを使ってください。

## 設定

基本的にはそのまま使えます。

細かく調整する場合は `data/default.ini` を `nekonote.bat` と同じフォルダに `settings.ini` としてコピーして使ってください。 `default.ini` の上書きはしないでください。

### 一般設定

- `[Nox]`
    - `path`: Nox.exe へのファイルパス。画面範囲の自動検知に使います。デフォルトは Windows のパスになっています。空欄にすると Windows であっても手動での範囲指定に切り替わります。
- `[DEFAULT]`
    - `interval`: ゲーム画面を判定するための最短間隔(秒数)。マクロ側のアルゴリズムによって変動しますので目安程度に考えてください。

### マクロ単位

- `[ゲーム名.マクロ名]`
   - `key_(ボタン名)`: ゲーム画面をクリックする際、マウスの代わりにキーボードショートカットを使う設定です。設定がなかったり、空欄だと通常通りクリックモードになります。ボタン間で設定がかぶってもかまいません。  
     通常キーは小文字で、特殊キーは大文字で書いてください。

#### キーボードショートカットについて

動作としては単純に、決められたキーを押すだけです。キーを押した後の動作は Nox や OS に任せます。  
Nox の仮想キー機能(あるキーを押すと画面上の決まった位置をクリックする)を使って割り当てるのが一番簡単です。設定はネット上の記事を参考にしてください。同じ機能を持ったフリーソフトでも構いません。

1. マクロの説明文などを読んで、必要なボタンの種類を確認します。
2. Nox 上でそのボタンに対して仮想キーを割り当てます。
3. 設定ファイルに割り当てたキーを書き込みます。
4. 設定が終わったら Nox 上で仮想キーを透明にするのを忘れないでください。

以下の特殊キーは大文字で書いてください。

     ENTER, TAB, ESC, BACKSPACE, DELETE, INSERT, SPACE
     HOME, END, LEFT, RIGHT, DOWN, UP, PAGE_DOWN, PAGE_UP
     PRINTSCREEN, PAUSE, CAPS_LOCK, SCROLL_LOCK, NUM_LOCK
     F1 ~ F15

テンキーも特殊キー扱いになります。

     NUM0, NUM1, NUM2, NUM3, NUM4, NUM5, NUM6, NUM7, NUM8, NUM9
     SEPARATOR, ADD, MINUS, MULTIPLY, DIVIDE

## 実行可能な作業内容

TODO

## 注意

- 自動スクリプトを実行中に他の操作はできません。
- アプリのウィンドウが移動したり、他のウィンドウが覆いかぶさると判定に失敗します。
- アプリのウィンドウがPC画面からはみ出していると動作が不安定になることがあります。
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

### マウスカーソルが動かない・クリックしない

下記のようなエラーログが出る場合

    [error] RobotDesktop: checkMousePosition: should be L(1000,500)@S(0)[0,0 1920x1080]
    but after move is L(130,210)@S(0)[0,0 1920x1080]
    Possible cause in case you did not touch the mouse while script was running:
     Mouse actions are blocked generally or by the frontmost application.
     You might try to run the SikuliX stuff as admin.

他のアプリケーションを管理者権限で動かしているとこのような問題が出ます。バッチファイル(スクリプト)も管理者権限で動かしてください。

### 長時間動かしていると画面判定の精度が下がる

画像認識系の限界です。頻発するときは適度に休ませてください。


## その他

ライブラリの SikuliX は動作が確認できたバージョンを同梱しています。<https://raiman.github.io/SikuliX1/downloads.html> からもダウンロードできます。

音素材のクレジット

- notify.wav <http://www.orangefreesounds.com/little-christmas-bell-sound/>
- error.wav <http://www.orangefreesounds.com/error-sound/>
