import requests
import json
from config import keys


class APIException(Exception):
    pass

# создание класса ошибок, которые могут быть из-за пользователя
class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base: # Ввод одинаковых значений
            raise APIException(f'\nЯ не перевожу одинаковые валюты "{base}"'
                               f'\nВаше желание нелогично, не так ли?')

        try:
            quote_ticker = keys[quote]
        except KeyError: #Ввод необрабатываемого значения валюты (первое значение)
            raise APIException(f'\nК сожалению мне не знакома валюта "{quote}" :(\n'
                               f'\nЧтобы увидеть валюты, которые я умею конвертировать, '
                               f'введите команду\n/values')

        try:
            base_ticker = keys[base]
        except KeyError: #Второе значение валюты, которое невозможно обработать
            raise APIException(f'\nК сожалению мне не знакома валюта "{base}" :(\n'
                               f'\nЧтобы увидеть валюты, которые я умею конвертировать, '
                               f'введите команду\n/values')

        try:
            amount = float(amount)

            if int(amount) > 0: #Отслеживание введения недопустимого(отрицательного) значения
                amount = int(amount)
            else:
                raise APIException(f'\nКоличество не может быть отрицательным: {amount}\n'
                                   f'\nВводите, пожалуйста, только положительные значения и при '
                                   'необходимости ставьте точку в качестве десятичного разделителя.')

        except ValueError: #Ошибка если введены буквенные а не числовые значения
            raise APIException(f'\nЯ не смог обработать введённое количество: {amount}\n'
                               f'\nПосмотрите ещё раз, что я умею \n/help')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return float(total_base * amount)


class DeclensionByCases():
    def __init__(self, word, num):
        self.word = word
        self.num = num

    # Добавление читабельности текста (окончания валют)
    def incline(self):
        if self.word != 'евро':
            if (2 <= self.num % 10 <= 4 and self.num % 100 not in [12, 13, 14]) or not self.num.is_integer():
                return 'рубля' if self.word == 'рубль' else self.word + 'a'
            if (self.num % 10 == 0 or 5 <= self.num % 10 <= 9 or 11 <= self.num % 100 <= 14) and self.num.is_integer():
                return 'рублей' if self.word == 'рубль' else self.word + 'ов'
        return self.word