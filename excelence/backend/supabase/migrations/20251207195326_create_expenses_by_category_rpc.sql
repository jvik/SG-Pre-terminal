create or replace function get_expenses_by_category(p_user_id uuid)
returns table (category_name text, total_amount numeric)
language plpgsql
security definer
as $$
begin
  return query
  select
    t.category as category_name,
    sum(t.amount) as total_amount
  from
    transactions t
  where
    t.user_id = p_user_id
    and t.type = 'expense'
  group by
    t.category;
end;
$$;
