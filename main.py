import platform
import aiohttp
import asyncio
from datetime import datetime, timedelta
import sys

class CurrencyApi:
    URL = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
    CURRENCIES = ['USD', 'EUR']

    async def get_currency_rates(self, days):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        rates = []
        async with aiohttp.ClientSession() as session:
            for i in range((end_date - start_date).days):
                current_date = (start_date + timedelta(days=i)).strftime("%d.%m.%Y")
                async with session.get(f'{self.URL}{current_date}') as response:
                    if response.status == 200:
                        data = await response.json()
                        exchange_rates = data.get('exchangeRate', [])
                        for rate in exchange_rates:
                            if rate.get('currency') in self.CURRENCIES:
                                rates.append({
                                    'currency': rate.get('currency'),
                                    'saleRate': rate.get('saleRate'),
                                    'purchaseRate': rate.get('purchaseRate'),
                                    'date': current_date
                                })
                    else:
                        print(f"Error retrieving currency rates for {current_date}")
        return rates

async def main():
    api = CurrencyApi()
    rates = await api.get_currency_rates(days=int(com[1]))
    for rate in rates:
        print(f"{rate.get('date')}: {rate.get('currency')}, Sale: {rate.get('saleRate')}, Purchase: {rate.get('purchaseRate')}")

if __name__ == '__main__':
    com = sys.argv
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    if int(com[1]) <= 10:
        asyncio.run(main())
    else:
        print('The date should be less or equal to 10 days')

