messages = {
    #
    # main
    #

    # common
    'close_button': 'Close',
    'clear_button': 'Clear',
    'cancel_button': 'Cancel',
    'done_button': 'Done',

    # main.kv
    'home': 'Home',
    'history': 'History',
    'lnd_history': 'LND\nHistory',
    'setting': 'Setting',
    'shutdown': 'Shutdown',

    # home_screen.py
    'lnd_unavailable': 'LND is unavailable.',
    'lnd_not_connected': 'LND is not connected.',
    'lnd_not_unlocked': 'LND is not unlocked.',
    'payment_amount_zero': 'The payment amount is 0.',
    'payment_not_entered': 'The payment amount has not been entered.',
    'fiat_button': 'Fiat',
    'lightning_payment_button': 'BTC\n(Lightning Network)',
    'lnd_invalid_conf': 'LND config is invalid.',
    'lnd_unable_create_invo': 'Unable to create a LND invoice.',

    # home_screen.kv
    'select_payment_method': 'Select payment method.',

    # history_screen.py
    'payment_not_found': 'Payment data not found.',
    'payment_detail_id': 'ID',
    'payment_detail_date': 'Date',
    'payment_method_fiat': 'Fiat',
    'payment_method_lnd': 'LND',
    'payment_detail_method': 'Method',
    'payment_detail_total': 'Total',
    'payment_detail_paid': 'Paid',
    'payment_detail_change': 'Change',
    'payment_detail_amount': 'Amount',
    'payment_detail_btc': 'BTC',

    # history_screen.kv
    'history_list_id': 'ID',
    'history_list_method': 'Method',
    'history_list_amount': 'Amount',
    'history_list_btc': 'BTC',
    'history_list_date': 'Date',

    # lnd_history_screen.py
    'lnd_invoice_unavailable': 'Unable to load invoices from LND.',
    'lnd_invoice_not_found': 'Invoice not found.',

    # lnd_history_screen.kv

    # setting_screen.py
    'readonly_settings': 'The following settings are read only. '
                         'You needs to edit `/boot/btc-register-config/config.ini`.',
    'save_and_restart': 'Save and Restart',
    'language': 'Language',
    'setting_fiat_currency': 'Fiat Currency',
    'price_reference_exchange': 'Price Reference Exchange',

    # wait_fiat_screen.py
    'invalid_payment_fiat': 'Invalid payment.',
    'amount_not_inputted': 'The amount is not inputted.',

    # wait_fiat_screen.kv
    'payment_total': 'Total',
    'payment_paid': 'Paid',
    'payment_change': 'Change',

    # wait_lnd_screen.py
    'invalid_payment_lnd': 'Invalid payment.',

    #
    # sub
    #

    # fiat_screen.kv
    'sub_fiat_screen_total': 'Total',
    'sub_fiat_screen_paid': 'Paid',
    'sub_fiat_screen_change': 'Change',
}
