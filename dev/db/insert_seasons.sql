delete from seasons;

insert into seasons(name, year, start_date, end_date)
values
('2022 Calendar Year', 2022, '2022-01-01', '2022-13-31')
, ('2023 Calendar Year', 2023, '2023-01-01', '2023-12-31')
,('2024 Calendar Year', 2024, '2024-01-01', '2024-12-31')
,('2025 Skinny Bob''s Series', 2025, '2025-01-01', '2025-12-31');

select * from seasons;