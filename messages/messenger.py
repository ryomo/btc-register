# TODO: i18n


class Messenger:

    def __init__(self, lang='en'):
        self.lang = lang

    def info(self, text):
        return text

    def warning(self, text):
        return '[color=ffff33]WARNING:[/color] {}'.format(text)

    def error(self, text):
        return '[b][color=ff3333]ERROR:[/color] {}[/b]'.format(text)
