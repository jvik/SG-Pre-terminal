create or replace function get_expenses_by_category(p_user_id uuid)
returns table (category_name text, total_amount numeric)
language plpgsql
security definer
as $$
begin
  return query
  select
    c.name as category_name,
    sum(t.amount) as total_amount
  from
    transactions t
  join
    categories c on t.category_id = c.id
  where
    t.user_id = p_user_id
    and t.type = 'expense'
  group by
    c.name
  order by
    total_amount desc;
end;
$$;
