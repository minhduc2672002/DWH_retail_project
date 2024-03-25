WITH customer_cte AS (
    SELECT DISTINCT
        {{ dbt_utils.generate_surrogate_key(['CustomerID', 'Country']) }} AS customer_id,
        Country AS country
    FROM {{ source('retail','invoice_cleaned') }}
    WHERE CustomerID IS NOT NULL
)
SELECT
    t.*,
    c.iso
FROM customer_cte t 
LEFT JOIN {{ source('retail','country') }} c ON t.country = c.nicename   
