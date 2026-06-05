CREATE OR REPLACE VIEW vw_sales_summary AS
SELECT  e.id            AS event_id,
        e.name          AS event_name,
        d.id            AS drink_id,
        d.name          AS drink_name,
        SUM(s.quantity)                 AS total_qty,
        SUM(s.quantity * d.price_dkk)   AS total_revenue
FROM        sale  s
JOIN        event e ON e.id = s.event_id
JOIN        drink d ON d.id = s.drink_id
GROUP BY    e.id, e.name, d.id, d.name
ORDER BY    e.id, d.name;


CREATE OR REPLACE VIEW vw_shift_fill AS
SELECT  sh.id                                                   AS shift_id,
        sh.event_id,
        sh.role,
        sh.capacity,
        COUNT(*) FILTER (WHERE su.status = 'confirmed')         AS confirmed_count,
        COUNT(*) FILTER (WHERE su.status = 'waitlisted')        AS waitlisted_count,
        GREATEST(sh.capacity
                 - COUNT(*) FILTER (WHERE su.status = 'confirmed'), 0) AS slots_left
FROM        shift sh
LEFT JOIN   shift_signup su ON su.shift_id = sh.id
GROUP BY    sh.id, sh.event_id, sh.role, sh.capacity;
