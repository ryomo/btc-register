
messages = {
    #
    # main
    #

    # common
    'close_button': '閉じる',
    'clear_button': 'クリア',
    'cancel_button': 'キャンセル',
    'done_button': '完了',

    # main.kv
    'home': 'ホーム',
    'history': '履歴',
    'lnd_history': 'LND履歴',
    'setting': '設定',
    'shutdown': '終了',

    # home_screen.py
    'lnd_unavailable': 'LNDを使用できません。',
    'lnd_not_connected': 'LNDに接続できません。',
    'lnd_not_unlocked': 'LNDがunlockされていません。',
    'payment_amount_zero': '支払額が0です。',
    'payment_not_entered': '金額が入力されていません。',
    'fiat_button': '法定通貨',
    'lightning_payment_button': 'BTC\n(Lihgtning Network)',
    'lnd_invalid_conf': 'LNDの設定が無効です。',
    'lnd_unable_create_invo': 'LNDのinvoiceを作成できませんでした。',

    # home_screen.kv
    'select_payment_method': '支払方法を選択してください。',

    # history_screen.py
    'payment_not_found': '支払データがありません。',
    'payment_detail_id': 'ID',
    'payment_detail_date': '日時',
    'payment_method_fiat': '法定通貨',
    'payment_method_lnd': 'LND',
    'payment_detail_method': '支払方法',
    'payment_detail_total': '合計',
    'payment_detail_paid': '受取額',
    'payment_detail_change': 'お釣り',
    'payment_detail_amount': '金額',
    'payment_detail_btc': 'BTC',

    # history_screen.kv
    'history_list_id': 'ID',
    'history_list_method': '支払方法',
    'history_list_amount': '金額',
    'history_list_btc': 'BTC',
    'history_list_date': '日時',

    # lnd_history_screen.py
    'lnd_invoice_unavailable': 'LNDからinvoiceを読み込めません。',
    'lnd_invoice_not_found': 'invoiceがありません。',

    # lnd_history_screen.kv

    # setting_screen.py
    'readonly_settings': '以下の設定は読込専用です。'
                         '変更するには、`/boot/btc-register-config/config.ini`を編集する必要があります。',
    'save_and_restart': '保存して再起動',
    'language': '言語',
    'price_reference_exchange': '価格を参照する取引所',

    # wait_fiat_screen.py
    'invalid_payment_fiat': '無効な支払です。',
    'amount_not_inputted': '金額が入力されていません。',

    # wait_fiat_screen.kv
    'payment_total': '合計',
    'payment_paid': '受取額',
    'payment_change': 'お釣り',

    # wait_lnd_screen.py
    'invalid_payment_lnd': '無効な支払です。',

    #
    # sub
    #

    # fiat_screen.kv
    'sub_fiat_screen_total': '合計',
    'sub_fiat_screen_paid': 'お受取り',
    'sub_fiat_screen_change': 'お返し',
}
