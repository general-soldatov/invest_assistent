import requests
from bs4 import BeautifulSoup
from typing import List

class InfoPaper:
    def __init__(self):
        self.url_bond_seq = 'https://iss.moex.com/iss/engines/stock/markets/bonds/securities.xml'
        self.price_url = lambda x: f'https://iss.moex.com/iss/engines/stock/markets/bonds/securities.xml?securities={x}'

    @staticmethod
    def response_soup(url) -> BeautifulSoup:
        response = requests.get(url)
        return BeautifulSoup(response.content, 'xml')


    def get_bond(self, isin: str):
        bonds = self.response_soup(self.url_bond_seq).find_all('row')
        for bond in bonds:
            if bond['ISIN'] == isin:
                return {
                    'security_id': bond['SECID'],
                    'name_paper': bond['SHORTNAME'],
                    'nominal': int(bond['LOTVALUE']),
                    'coupon_value': float(bond['COUPONVALUE']),
                    'nkd': float(bond['ACCRUEDINT']),
                    'next_coupon_date': bond['NEXTCOUPON'],
                    'maturity_date': bond['MATDATE'],
                    'coupon_period': int(bond['COUPONPERIOD'])
                }

    def get_bonds_lst(self, bonds_isin: List[str]):
        bonds = self.response_soup(self.url_bond_seq).find_all('row')
        data = []
        for bond in bonds:
            try:
                if bond['ISIN'] in bonds_isin:
                    enroll = float(bond['COUPONVALUE']) * (365 // int(bond['COUPONPERIOD'])) / float(bond['LOTVALUE']) * 100
                    data.append({
                        'security_id': bond['SECID'],
                        'name_paper': str(bond['SHORTNAME']),
                        'nominal': int(bond['LOTVALUE']),
                        'coupon_value': float(bond['COUPONVALUE']),
                        'nkd': float(bond['ACCRUEDINT']),
                        'next_coupon_date': bond['NEXTCOUPON'],
                        'maturity_date': bond['MATDATE'],
                        'coupon_period': int(bond['COUPONPERIOD']),
                        'coupon_enroll': f"{enroll} %"
                    })

                    if len(data) == len(bonds_isin):
                        break
            except KeyError:
                continue
        return data

    def get_price_paper(self, bonds_isin: str = 'RU000A106P63'):
        price_element = self.response_soup(self.price_url(bonds_isin)).findAll('row', {'SECID': bonds_isin})[1]
        data = price_element.get('PREVPRICE', 0) \
                        if price_element.get('PREVPRICE', 0) else price_element.get('OFFER', 0)
        return float(data or 0)
