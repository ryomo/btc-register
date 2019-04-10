# btc-register

## これは何？

BitcoinのLightning Networkでの支払いを受け付けるレジアプリです。



## 必要なもの

* LND node
    * v0.5.2-beta or newer
* Raspberry Pi
    * 3b or better
    * [link](https://raspberry-pi.ksyic.com/main/index/pdp.id/435/pdp.open/435)
* Raspberry Pi
    * [link](https://raspberry-pi.ksyic.com/main/index/pdp.id/101/pdp.open/101) 
* (Optional) HDMI Display
* Keyboard




## インストール

1. [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/)をmicro sdカードに焼く。
    
    * [Etcher](https://www.balena.io/etcher/)などの使用を推奨。

2. 公式ディスプレイを上下逆さまで使う場合は、`boot`パーティションの`config.txt`の末尾に`lcd_rotate=2`を記載する。

    * HDMIディスプレイの解像度設定で`config.txt`に記載が必要な場合も、ついでにここでやる。

3. bootパーティションに`btc-register-config`フォルダを作って、そこに`settings.ini`というファイル名で以下の内容のファイルを作成。

    ```
    [app]
    shop_name = {店の名前}
    
    [lnd]
    url = https://{LNDノードのアドレス}:{ポート番号}
    ```
   
    * `{}`は付けない。

4. LNDの`tls.cert`・`invoice.macaroon`を、同じ`btc-register-config`フォルダに入れる。

5. 起動してログイン。デフォルトのユーザー/パスワードは、`pi`/`raspberry`。

6. `sudo raspi-config`を実行して、以下の設定をする。

    * `Change User Password`
    * `Localization Options` > `Change Locale`
        * スペースで選択。
        * `ja_JP.UTF-8`など、UTF-8のを選ぶ。
    * `Localisation Options` > `Change Timezone`
    * `Localisation Options` > `Change Keyboard Layout`
    * Wifiで接続する場合は、`Network Options` > `Wi-fi`
    * 自動ログインする場合は、`Boot Options` > `Desktop / CLI` > `Console Autologin`
    * （開発時のみ）`Interfacing Options` > `SSH`
        * 重大なセキュリティリスクがあるので、わからない場合は絶対に有効にしないこと。
        * 有効にする場合でも、すぐに公開鍵認証を設定し、パスワード認証を無効にすること。また、不特定多数のユーザーがアクセスするネットワークとは分離すること。
    * 終わったら`<Finish>`。再起動するか聞かれたらする。

7. 以下を実行。

    ```bash
    git clone https://github.com/ryomo/btc-register.git
    cd btc-register
    ./install.sh
    ```

8. 30~60分くらい？待つ。

    * 正常に完了したら自動で再起動して、アプリが起動する。
    * アプリ内ではキーボードが使えない（二重入力されるバグがある）ので、アプリが起動した時点でキーボードは外す。



## 注意

* 法定通貨からBitcoinに変換するときに、小数点以下は四捨五入しています。
* 現在、このアプリではテンキーを含むキーボードが使えません。
    * キーは二重で入力されてしまいます。
    * キー入力は、背後で動作しているターミナル画面でも同時に入力されてしまいます。



## Licenses

* このプロジェクトはMITライセンスにより公開します。
* このプロジェクトは他のオープンソースプロジェクトを使用しています。

### Kivy

* Open source UI framework.
* Licensed under the MIT License.
* [[link]](https://github.com/kivy/kivy)

### Open Iconic

* Icons under `assets/open_iconic` directory.
* Licensed under the MIT License.
* [[link]](https://github.com/iconic/open-iconic)
