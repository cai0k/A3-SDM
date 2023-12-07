class Relatorio:
    def produtos_mais_vendidos(vendas):
        produtos_vendidos = {}

        for venda in vendas:
            for produto in venda.produtos:
                if produto.codigo in produtos_vendidos:
                    produtos_vendidos[produto.codigo] += 1
                else:
                    produtos_vendidos[produto.codigo] = 1

        produtos_mais_vendidos = sorted(produtos_vendidos.items(), key=lambda x: x[1], reverse=True)

        return produtos_mais_vendidos
    
    @staticmethod
    def produtos_por_cliente(vendas, cliente):
        produtos_cliente = []

        for venda in vendas:
            if venda.cliente == cliente:
                produtos_cliente.extend(venda.produtos)

        return produtos_cliente

    @staticmethod
    def consumo_medio_cliente(vendas, cliente):
        total_produtos = 0
        total_vendas = 0

        for venda in vendas:
            if venda.cliente == cliente:
                total_produtos += len(venda.produtos)
                total_vendas += 1

        if total_vendas == 0:
            return 0

        consumo_medio = total_produtos / total_vendas
        return consumo_medio
    
    def produtos_baixo_estoque(produtos, limite):
        try:
            limite = int(limite)
        except ValueError:
            print("Erro: O limite deve ser um número inteiro.")
            return

        produtos_baixo_estoque = []

        for produto in produtos:
            if produto.estoque < limite:
                produtos_baixo_estoque.append(produto)

        return produtos_baixo_estoque

