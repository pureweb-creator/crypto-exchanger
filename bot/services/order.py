class OrderService():
    @staticmethod
    def calculate_company_value(data: dict[str, any]) -> str:
        co_value = float(data['co_value'])
        base_value = float(data['base_value'])
        client_value = float(data['client_value'])
        co_cur_after_int = data['co_cur_after_int']

        return f"{(co_value / base_value * client_value):.{co_cur_after_int}f}"

    @staticmethod
    def calculate_rate_in_value(pair: dict[str, dict[str, any]]):
        co_after_int = int(pair['CoCurAfterInt'])+2
        base_value = float(pair['BaseValue'])
        client_value = float(f"{(base_value / 1000):.{co_after_int}f}")

        # format values for example: 1.000 -> 1, 1.123 -> 1.123
        return f"{client_value:f}".rstrip('0').rstrip('.')

    @staticmethod
    def calculate_rate_out_value(pair: dict[str, dict[str, any]]):
        co_after_int = int(pair['CoCurAfterInt'])+2
        co_value = float(pair['CoValue'])
        co_value = float(f"{(co_value / 1000):.{co_after_int}f}")

        # format values for example: 1.000 -> 1, 1.123 -> 1.123
        return f"{co_value:f}".rstrip('0').rstrip('.')
