import investpy

def get_profile(stock , country):
    com_profile = investpy.get_stock_company_profile(stock=stock, country=country, language='english')
    profile = com_profile['desc']
    return profile