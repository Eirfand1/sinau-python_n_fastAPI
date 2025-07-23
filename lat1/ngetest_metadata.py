from typing import Annotated

def say_hello(name: Annotated[str, "ini merupakan metadata"]) -> str:
    return f"Hello {name}"

print(say_hello("Sutaryo"))