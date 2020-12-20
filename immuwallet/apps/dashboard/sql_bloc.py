from django.db import connection

from dashboard.models import Estabelecimento, Vacina


class SqlBloc:

    @staticmethod
    def relatorio_vacinas_aplicadas_dia(estabelecimento: Estabelecimento = None, vacina: Vacina = None, step="day"):
        """
        Gera um relatório de quantas vacinas de cada tipo foram aplicadas em cada estabelecimento
        em cada dia.
        """
        filtros = [
            "status = 3"  # 3 = concluido
        ]
        if estabelecimento:
            filtros.append(f"estabelecimento_id = '{estabelecimento.pk}'")
        if vacina:
            filtros.append(f"vacina_id = '{vacina.pk}'")

        where_clauses = " AND ".join(filtros)

        sql = f"""
            SELECT
                date_trunc('{step}',"data") as dia,
                estabelecimento_id as cnes,
                est.nome as estabelecimento,
                vac.nome,
                count(*) as quantidade
            FROM public.dashboard_horamarcada
            JOIN estabelecimento est ON estabelecimento_id = est.cnes
            JOIN dashboard_vacina vac ON vacina_id = vac.codigo
            WHERE {where_clauses}
            GROUP BY
                date_trunc('{step}',"data"),
                estabelecimento_id,
                est.nome,
                vac.nome
            """
        cursor = connection.cursor()

        cursor.execute(sql)

        return SqlBloc.dictfetchall(cursor)

    @staticmethod
    def dictfetchall(cursor):
        """
        Pega os resultados de uma query executada através do cursor (que seria uma lista de tuplas)
        e transforma em uma lista de dicionários, onde a chave é o nome da coluna

        :param cursor:  cursor através do qual a query foi executada
        :return:        lista de dicionários
        """
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
