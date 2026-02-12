async def calculate_co_value(data: dict[str, any]) -> str:
    co_value = float(data['co_value'])
    base_value = float(data['base_value'])
    client_value = float(data['client_value'])
    co_cur_after_int = data['co_cur_after_int']

    return f"{(co_value / base_value * client_value):.{co_cur_after_int}f}"

class Pair:
    def __init__(self, pair):
        self.client_value = None
        self.co_after_int = int(pair['CoCurAfterInt'])+2
        self.co_value = float(pair['CoValue'])
        self.co_cur_title = pair['CoCurTitle']
        self.co_cur_name = pair['CoCurName']
        self.client_cur_title = pair['ClientCurTitle']
        self.base_value = float(pair['BaseValue'])

    def calculate_exchange_rate(self):
        self.client_value = float(f"{(self.base_value / 1000):.{self.co_after_int}f}")
        self.co_value = float(f"{(self.co_value / 1000):.{self.co_after_int}f}")

        # format values for example: 1.000 -> 1, 1.123 -> 1.123
        self.client_value = f"{self.client_value:f}".rstrip('0').rstrip('.')
        self.co_value = f"{self.co_value:f}".rstrip('0').rstrip('.')
