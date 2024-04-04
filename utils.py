from fastapi import HTTPException


async def check_number(number: str):
    if len(number) != 12 or not number[2:].isdigit():
        raise HTTPException(detail="Неверный формат номера. Пример: +79998887755", status_code=401)
    if number[:2] != "+7":
        raise HTTPException(detail="Неверный формат номера, начните с +7", status_code=401)
    return number


async def check_code(code: int):
    code = str(code)
    if len(code) != 6 or not code.isdigit():
        raise HTTPException(detail="Код должен состоять из 6 цифр", status_code=401)
    return code