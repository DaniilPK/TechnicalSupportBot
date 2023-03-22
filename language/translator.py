from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator, TranslatorRunner


class Translator:
    t_hub: TranslatorHub

    def __init__(self):
        self.t_hub = TranslatorHub(
            locales_map={
                'en': ('en', 'ru'),
                'ru': ('ru',)
            },
            translators=[
                FluentTranslator(
                    locale='en',
                    translator=FluentBundle.from_files('en-US', filenames=['language/locales/en.ftl'])
                ),
                FluentTranslator(
                    locale='ru',
                    translator=FluentBundle.from_files('ru-RU', filenames=['language/locales/ru.ftl'])
                )
            ],
            root_locale='en'
        )

    def __call__(self, language, *args, **kwargs):
        return LocalizedTranslator(
            translator=self.t_hub.get_translator_by_locale(locale=language)
        )


class LocalizedTranslator:
    translator: TranslatorRunner

    def __init__(self, translator: TranslatorRunner):
        self.translator = translator

    def get(self, key: str, **kwargs) -> str:
        return self.translator.get(key, **kwargs)
