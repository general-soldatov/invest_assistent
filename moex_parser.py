import requests
from bs4 import BeautifulSoup
from typing import List

class InfoPaper:
    def __init__(self):
        url = 'https://iss.moex.com/iss/engines/stock/markets/bonds/securities.xml'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'xml')
        self.bonds = soup.find_all('row')

    def get_bond(self, isin: str):
        for bond in self.bonds:
            if bond['ISIN'] == isin:
                return {
                    'security_id': bond['SECID'],
                    'short_name': bond['SHORTNAME'],
                    'nominal': bond['LOTVALUE'],
                    'coupon_value': bond['COUPONVALUE'],
                    'nkd': bond['ACCRUEDINT'],
                    'next_coupon_date': bond['NEXTCOUPON'],
                    'maturity_date': bond['MATDATE'],
                    'coupon_period': bond['COUPONPERIOD']
                }

    def get_bonds_lst(self, bonds_isin: List[str]):
        data = []
        for bond in self.bonds:
            try:
                if bond['ISIN'] in bonds_isin:
                    enroll = round(float(bond['COUPONVALUE']) * (365 // int(bond['COUPONPERIOD'])) / float(bond['LOTVALUE']) * 100, 3)
                    data.append({
                        'security_id': bond['SECID'],
                        'short_name': bond['SHORTNAME'],
                        'nominal': bond['LOTVALUE'],
                        'coupon_value': bond['COUPONVALUE'],
                        'nkd': bond['ACCRUEDINT'],
                        'next_coupon_date': bond['NEXTCOUPON'],
                        'maturity_date': bond['MATDATE'],
                        'coupon_period': bond['COUPONPERIOD'],
                        'coupon_enroll': f"{enroll} %"
                    })

                    if len(data) == len(bonds_isin):
                        break
            except KeyError:
                continue
        return data
