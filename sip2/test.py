from enum import Enum, EnumMeta


class DefaultEnumMeta(EnumMeta):
    default = object()

    def __call__(cls, value=default, *args, **kwargs):
        print('toto')
        if value is DefaultEnumMeta.default:
            # Assume the first enum is default
            return next(iter(cls))
        return super().__call__(value, *args, **kwargs)


class SelfcheckLanguage(Enum, metaclass=DefaultEnumMeta):
    """Enum class to list all available language."""

    __metaclass__ = DefaultEnumMeta

    # SIP2 supported Language
    UNKNOWN = '000'
    ENGLISH = '001'
    FRENCH = '002'
    GERMAN = '003'
    ITALIAN = '004'
    DUTCH = '005'
    SWEDISH = '006'
    FINNISH = '007'
    SPANISH = '008'
    DANISH = '009'
    PORTUGUESE = '010'
    CANADIAN_FRENCH = '011'
    NORWEGIAN = '012'
    HEBREW = '013'
    JAPANESE = '014'
    RUSSIAN = '015'
    ARABIC = '016'
    POLISH = '017'
    GREEK = '018'
    CHINESE = '019'
    KOREAN = '020'
    NORTH_AMERICAN_SPANISH = '021'
    TAMIL = '022'
    MALAY = '023'
    UNITED_KINGDOM = '024'
    ICELANDIC = '025'
    BELGIAN = '026'
    TAIWANESE = '027'

    # ISO 639-2 common Language mapping
    und = UNKNOWN
    eng = ENGLISH
    fre = FRENCH
    ger = GERMAN
    ita = ITALIAN
    dut = DUTCH
    swe = SWEDISH
    fin = FINNISH
    spa = SPANISH
    dan = DANISH
    por = PORTUGUESE
    nor = NORWEGIAN
    heb = HEBREW
    jpn = JAPANESE
    rus = RUSSIAN
    pol = POLISH
    gre = GREEK
    chi = CHINESE
    kor = KOREAN
    tam = TAMIL
    may = MALAY
    ice = ICELANDIC


def get_language_code(language):
    """Get mapped selfcheck language.

    :param language: ISO 639-2 common language
    :returns SIP2 mapped language code
    """

    # if SelfcheckLanguage[language] in SelfcheckLanguage:

    try:
        return SelfcheckLanguage[language].value
    except KeyError:
        return SelfcheckLanguage.UNKNOWN.value


if __name__ == "__main__":
    print(get_language_code('und'))
    print(get_language_code('spa'))
    print(get_language_code('aaa'))
