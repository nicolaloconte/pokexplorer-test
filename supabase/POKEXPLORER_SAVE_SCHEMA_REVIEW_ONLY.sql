-- REVIEW ONLY. Do not execute without explicit deployment authorization.
-- Requires Supabase Auth Discord provider configured out-of-band and tested.
create table if not exists public.pokexplorer_saves (
  user_id uuid primary key references auth.users(id) on delete cascade,
  revision bigint not null default 1 check (revision >= 1),
  run jsonb not null,
  updated_at timestamptz not null default now()
);
alter table public.pokexplorer_saves enable row level security;
revoke all on public.pokexplorer_saves from anon, authenticated;
grant select, insert, update, delete on public.pokexplorer_saves to authenticated;
create policy "pokex select own" on public.pokexplorer_saves for select to authenticated
  using ((select auth.uid()) = user_id);
create policy "pokex insert own" on public.pokexplorer_saves for insert to authenticated
  with check ((select auth.uid()) = user_id);
create policy "pokex update own" on public.pokexplorer_saves for update to authenticated
  using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "pokex delete own" on public.pokexplorer_saves for delete to authenticated
  using ((select auth.uid()) = user_id);
-- Before deploying, add adversarial RLS tests for two authenticated users
-- and anon (SELECT/INSERT/UPDATE/DELETE), as well as conflict/aborted requests.
