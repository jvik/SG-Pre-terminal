-- Fix the get_expenses_by_category function to join with categories table
-- Drop the old function first
drop function if exists get_expenses_by_category(uuid);

-- Recreate with correct return type
create or replace function get_expenses_by_category(p_user_id uuid)
returns table (category_name varchar, total_amount numeric)
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
