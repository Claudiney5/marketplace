SELECT T1.*,
    case when pct_receita <= 0.5 and pct_freq <= 0.5 then 'Baixo Baixo'
        when pct_receita > 0.5 and pct_freq <= 0.5 then 'Alto Valor'
        when pct_receita <= 0.5 and pct_freq > 0.5 then 'Alta Frequência'
        when pct_receita < 0.9 or pct_freq < 0.9 then 'Produtivo'
        else 'Super Produtivo'
    end as SEGMENTO_VALOR_FREQ,

    CASE when qtd_dias_base <= 60 then 'INICIO'
        when qtd_dias_venda >= 300 then 'RETENÇÃO'
        else 'ATIVO'
    end as SEGMENTO_VIDA,

    '{date_end}' as DT_SEGMENT

FROM (

    SELECT T1.*,
       percent_rank() over(order by receita_total asc) as pct_receita,
       percent_rank() over(order by qtd_pedidos asc) as pct_freq

    FROM (

        SELECT T2.seller_id,
                SUM(T2.price) AS receita_total,
                COUNT(DISTINCT T1.order_id) as qtd_pedidos,
                COUNT(T2.product_id) AS qtd_produtos,
                COUNT(DISTINCT T2.product_id) AS qtd_prod_dist,
                MIN(CAST(julianday('{date_end}') - julianday(T1.order_approved_at) AS INT)) AS qtd_dias_venda,
                max(cast(julianday('{date_end}') - julianday(dt_inicio) as int)) as qtd_dias_base

        FROM tb_orders AS T1

        LEFT JOIN tb_order_items AS T2
        ON T1.order_id = T2.order_id

        left join(
            SELECT T2.seller_id, min(date(T1.order_approved_at)) as dt_inicio
            FROM tb_orders AS T1
            left join tb_order_items as T2
            on T1.order_id = T2.order_id
            GROUP BY T2.seller_id
            ) as T3
            on T2.seller_id = T3.seller_id

        WHERE T1.order_approved_at BETWEEN '{date_init}' AND '{date_end}'

        GROUP BY T2.seller_id
    ) as T1

) as T1

where seller_id is not null
