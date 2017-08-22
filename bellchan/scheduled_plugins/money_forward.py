from bellchan.lib.money_forward import MoneyForward


def notify_budget(bot, schedule, handle_schedule_error):

    @handle_schedule_error()
    def notify():
        money_forward = MoneyForward()
        budget_status = money_forward.get_budget()

        text = '予算報告だよ！\n'
        text += '今月で使った金額\n'
        text += '【サマリー】\n'
        text += f'- *総額*: {budget_status.total_amount}円\n'
        text += f'- *変動費*: {budget_status.variable_amount}円\n'
        text += '【個別品目】\n'
        for variable_record in budget_status.variable_records:
            text += f'- *{variable_record.name}*: {variable_record.amount}円\n'
        text += '\n'

        text += '今月で残り使える金額だよ！\n'
        text += '【サマリー】\n'
        text += f'- *総額*: {budget_status.total_remaining}円\n'
        text += f'- *変動費*: {budget_status.variable_remaining}円\n'
        text += '【個別品目】\n'
        for variable_record in budget_status.variable_records:
            text += f'- *{variable_record.name}*: {variable_record.remaining}円\n'

        bot.push_message(text)

    schedule.every().saturday.at('12:00').do(notify)
