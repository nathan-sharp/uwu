class MeridianError(Exception):
    """Base error for Meridian."""


class LexError(MeridianError):
    pass


class ParseError(MeridianError):
    pass


class RuntimeErrorM(MeridianError):
    pass
