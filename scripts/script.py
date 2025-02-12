import pandas as pd

FILE_PATH = '/mnt/data/Meganium_Sales_data.xlsx'
SHEETS = ['Meganium_Sales_Data_-_Etsy', 'Meganium_Sales_Data_-_AliExpres', 'Meganium_Sales_Data_-_Shopee']

def load_data(file_path, sheets):
    """ Carrega os dados de todas as abas especificadas. """
    return {sheet: pd.read_excel(file_path, sheet_name=sheet) for sheet in sheets}

data = load_data(FILE_PATH, SHEETS)

def total_sales_by_platform(data):
    """ Calcula o volume total de vendas (quantidade e valor) por plataforma. """
    result = {}
    for platform, df in data.items():
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        df['total_price'] = pd.to_numeric(df['total_price'], errors='coerce')
        total_quantity = df['quantity'].sum()
        total_value = df['total_price'].sum()
        result[platform] = {'total_quantity': total_quantity, 'total_value': total_value}
    return result

def top_selling_products(data, top_n=5):
    """ Retorna os produtos mais vendidos por plataforma. """
    result = {}
    for platform, df in data.items():
        top_products = (df.groupby('product_sold')['quantity'].sum()
                          .sort_values(ascending=False).head(top_n))
        result[platform] = top_products
    return result

def average_price_by_product(data):
    """ Calcula o preço médio por produto em cada plataforma. """
    result = {}
    for platform, df in data.items():
        df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
        avg_price = df.groupby('product_sold')['unit_price'].mean().sort_values(ascending=False)
        result[platform] = avg_price
    return result

if __name__ == '__main__':
    total_sales = total_sales_by_platform(data)
    top_products = top_selling_products(data)
    avg_prices = average_price_by_product(data)

    print("\n=== Total de Vendas por Plataforma ===")
    for platform, values in total_sales.items():
        print(f"{platform}: Quantidade = {values['total_quantity']}, Valor Total = {values['total_value']}")

    print("\n=== Produtos Mais Vendidos ===")
    for platform, products in top_products.items():
        print(f"{platform}:")
        print(products)

    print("\n=== Preço Médio por Produto ===")
    for platform, prices in avg_prices.items():
        print(f"{platform}:")
        print(prices)
