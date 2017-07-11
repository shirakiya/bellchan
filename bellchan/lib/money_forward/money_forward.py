import os
import requests
from bs4 import BeautifulSoup
from bellchan.exceptions import HTMLTagNotFoundError
from bellchan.lib.money_forward.budget_status import BudgetStatus
from bellchan.lib.money_forward.budget_record import VariableRecord, FixedRecord


class MoneyForward(object):

    URLS = {
        'sign_in_get': 'https://moneyforward.com/users/sign_in',
        'sign_in_post': 'https://moneyforward.com/session',
        'spending_summaries_get': 'https://moneyforward.com/spending_summaries',
    }

    def __init__(self):
        self.user_id = os.environ['MONEY_FORWARD_ID']
        self.user_password = os.environ['MONEY_FORWARD_PASSWORD']

        self.logged_in = False
        self.sess = requests.session()

    def _make_soup(self, response):
        return BeautifulSoup(response.text, 'lxml')

    def login(self):
        res = self.sess.get(self.URLS['sign_in_get'])
        login_page = self._make_soup(res)
        auth_token = login_page.find(attrs={'name': 'authenticity_token'}).get('value')

        self.sess.post(self.URLS['sign_in_post'], data={
            'utf8': '✓',
            'sign_in_session_service[email]': self.user_id,
            'sign_in_session_service[password]': self.user_password,
            'authenticity_token': auth_token,
        })

        self.logged_in = True

    def get_page(self, page_key):
        if not self.logged_in:
            self.login()

        return self._make_soup(self.sess.get(self.URLS[page_key]))

    def get_budget(self):
        budget_page = self.get_page('spending_summaries_get')
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
