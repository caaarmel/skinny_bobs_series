DROP VIEW results_public;

CREATE VIEW iF NOT EXISTS results_public AS
select distinct
e.tourney_name as tournament,
e.date,
e.roster as total_players,
es.name as event_subtype,
ps.name as pt_structure,
p.full_name,
case when r.position_std = 1 then "1st"
    else r.position
    end as position_orig,
r.position_std,
ifnull(ps.points_awarded,0) as points_awarded,
case 
    when r.position_std > e.roster then e.roster
    else r.position_std
end as case_pts,

et.name as event_type_name,

p.first_name,
p.last_name,
p.alias,

e.id as event_id,
e.event_type_id,
e.event_subtype_id,
ps.id as ps_id,
ps.min_position as ps_min_pos,
ps.max_position as ps_max_pos,
r.source_id,
r.created_at,
r.processed_datetime

from staging_results r 
left outer join players p on r.full_name = p.full_name
left outer join events e on r.tourney = e.tourney_slug and r.date = e.date
left outer join event_types et on e.event_type_id = et.id
left outer join event_subtypes es on e.event_subtype_id = es.id
left outer join point_structures ps
    on e.event_subtype_id = ps.event_subtype_id
    and (e.season_id between ps.season_id_start and ifnull(ps.season_id_end,99))
    and (e.roster between ps.min_players and ifnull(ps.max_players,999) )
    and (r.position_std between ps.min_position and ifnull(ps.max_position,999))
    and (r.position_std between ps.min_position and ifnull(ps.max_players,999))
;