from bellchan.lib.money_forward import MoneyForward

from .base import BaseMessageBuilder


class MoneyForwardMessageBuilder(BaseMessageBuilder):

    def create(self):
        money_forward = MoneyForward()
        budget_status = money_forward.get_budget()

        message = '予算報告だよ！\n'
        message += '今月で使った金額\n'
        message += '【サマリー】\n'
        message += f'- *総額*: {budget_status.total_amount}円\n'
        message += f'- *変動費*: {budget_status.variable_amount}円\n'
        message += '【個別品目】\n'
        for variable_record in budget_status.variable_records:
            message += f'- *{variable_record.name}*: {variable_record.amount}円\n'
        message += '\n'

        message += '今月で残り使える金額だよ！\n'
        message += '【サマリー】\n'
        message += f'- *総額*: {budget_status.total_remaining}円\n'
        message += f'- *変動費*: {budget_status.variable_remaining}円\n'
        message += '【個別品目】\n'
        for variable_record in budget_status.variable_records:
            message += f'- *{variable_record.name}*: {variable_record.remaining}円\n'

        return message
