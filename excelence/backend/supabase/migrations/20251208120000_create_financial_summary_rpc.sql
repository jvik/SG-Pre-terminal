-- Create function to calculate financial summary
create or replace function get_user_financial_summary(p_user_id uuid)
returns table (total_income numeric, total_expenses numeric, net_balance numeric)
language plpgsql
security definer
as $$
begin
  return query
  select
    coalesce(sum(case when t.type = 'income' then t.amount else 0 end), 0) as total_income,
    coalesce(sum(case when t.type = 'expense' then t.amount else 0 end), 0) as total_expenses,
    coalesce(
      sum(case when t.type = 'income' then t.amount else 0 end) -
      sum(case when t.type = 'expense' then t.amount else 0 end),
      0
    ) as net_balance
  from
    transactions t
  where
    t.user_id = p_user_id;
end;
$$;
