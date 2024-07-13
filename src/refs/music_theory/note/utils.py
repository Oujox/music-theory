
import functools

def ensure_abc_method(cls):
    """
    デコレートされた関数が指定されたABCクラスのメソッドであることを確認するデコレータ。
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not isinstance(args[0], cls):
                raise TypeError(f"The method '{func.__name__}' must be called on an instance of {cls.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator