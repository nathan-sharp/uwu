class UwuError(Exception):
    """Base error for UWU runtime."""


class LexError(UwuError):
    pass


class ParseError(UwuError):
    pass


class RuntimeErrorM(UwuError):
    pass
