import os
import requests
from bs4 import BeautifulSoup
from bellchan.exceptions import HTMLTagNotFoundError
from bellchan.lib.money_forward.budget_status import BudgetStatus
from bellchan.lib.money_forward.budget_record import VariableRecord, FixedRecord


def notify_budget(schedule, bellchan):

    def login(sess):
        res = sess.get('https://moneyforward.com/users/sign_in')
        login_page = BeautifulSoup(res.text, 'lxml')
        auth_token = login_page.find(attrs={'name': 'authenticity_token'}).get('value')

        sess.post('https://moneyforward.com/session', data={
            'utf8': '✓',
            'sign_in_session_service[email]': os.environ['MONEY_FORWARD_ID'],
            'sign_in_session_service[password]': os.environ['MONEY_FORWARD_PASSWORD'],
            'authenticity_token': auth_token,
        })

        return sess

    def get_budget_page():
        sess = requests.session()
        sess = login(sess)
        res = sess.get('https://moneyforward.com/spending_summaries')
        return BeautifulSoup(res.text, 'lxml')

    def get_budget():
        budget_page = get_budget_page()
        ss_table = budget_page.find('table')
        if not ss_table:
            raise HTMLTagNotFoundError('spending summaries table is not found.')

        VARIABLE_CLASS = 'variable_type'
        FIXED_CLASS = 'fixed_type'

        budget_status = BudgetStatus()
        budget_type = None

        for tr in ss_table.find('tbody').find_all('tr'):
            name = tr.find('th').string
            amount = tr.find('td', class_='amount').find('span').string
            for string in tr.find('td', class_='remaining').strings:
                if string.strip().endswith('円'):
                    remaining = string

            if 'large_category_expense' in tr['class']:
                if budget_type == VARIABLE_CLASS:
                    record = VariableRecord(name, amount, remaining)
                elif budget_type == FIXED_CLASS:
                    record = FixedRecord(name, amount, remaining)
            else:
                if VARIABLE_CLASS in tr['class']:
                    budget_type = VARIABLE_CLASS
                elif FIXED_CLASS in tr['class']:
                    budget_type = FIXED_CLASS
                continue

            budget_status.add(record)

        return budget_status

    def notify():
        budget_status = get_budget()

        text = '今月で使った金額だよ！\n'
        text += '【サマリー】\n'
        text += f'*総額*: {budget_status.total_amount}円\n'
        text += f'*変動費*: {budget_status.variable_amount}円\n'
        text += '【個別品目】\n'
        for variable_record in budget_status.variable_records:
            text += f'*{variable_record.name}*: {variable_record.amount}円\n'
        text += '\n'

        text += '今月で残り使える金額だよ！\n'
        text += '【サマリー】\n'
        text += f'*総額*: {budget_status.total_remaining}円\n'
        text += f'*変動費*: {budget_status.variable_remaining}円\n'
        text += '【個別品目】\n'
        for variable_record in budget_status.variable_records:
            text += f'*{variable_record.name}*: {variable_record.remaining}円\n'

        bellchan.push_message(text)

    schedule.every().monday.at('08:00').do(notify)
