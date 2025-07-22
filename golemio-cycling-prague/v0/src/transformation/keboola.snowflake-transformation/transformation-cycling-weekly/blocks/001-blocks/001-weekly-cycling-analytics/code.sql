CREATE TABLE "cyclists_weekly_summary" AS
SELECT 
    bc."name" as location_name,
    bc."route" as route,
    bc."lat" as latitude,
    bc."lon" as longitude,
    bcd."direction_name" as direction,
    obs."location_id",
    obs."location_direction_id",
    obs."measured_from",
    obs."measured_to",
    obs."observed_cyclists",
    DATE_TRUNC('week', TO_TIMESTAMP(obs."measured_from")) as week_start,
    EXTRACT(YEAR FROM TO_TIMESTAMP(obs."measured_from")) as year,
    EXTRACT(WEEK FROM TO_TIMESTAMP(obs."measured_from")) as week_number,
    CONCAT(EXTRACT(YEAR FROM TO_TIMESTAMP(obs."measured_from")), '-W', LPAD(EXTRACT(WEEK FROM TO_TIMESTAMP(obs."measured_from"))::STRING, 2, '0')) as week_label
FROM "KBC_USE4_1909"."out.c-cyclists-in-prague"."bicycles_observations" obs
JOIN "KBC_USE4_1909"."in.c-cycling_in_prague"."bicycle_counters" bc
    ON obs."location_id" = bc."id"
JOIN "KBC_USE4_1909"."in.c-cycling_in_prague"."bicycle_counters_directions" bcd
    ON obs."location_direction_id" = bcd."direction_id"
ORDER BY week_start, location_name, direction
