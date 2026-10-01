-- CENTRAL DE APROVAÇÃO V7 — SUPABASE
-- Execute este script no SQL Editor do seu projeto Supabase.

create table if not exists public.user_app_state (
  user_id uuid primary key references auth.users(id) on delete cascade,
  state jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table public.user_app_state enable row level security;

drop policy if exists "Users can read own study state" on public.user_app_state;
create policy "Users can read own study state"
on public.user_app_state
for select
to authenticated
using (auth.uid() = user_id);

drop policy if exists "Users can insert own study state" on public.user_app_state;
create policy "Users can insert own study state"
on public.user_app_state
for insert
to authenticated
with check (auth.uid() = user_id);

drop policy if exists "Users can update own study state" on public.user_app_state;
create policy "Users can update own study state"
on public.user_app_state
for update
to authenticated
using (auth.uid() = user_id)
with check (auth.uid() = user_id);

-- Opcional: garante updated_at automaticamente caso uma atualização
-- seja feita fora da Central.
create or replace function public.set_updated_at()
returns trigger
language plpgsql
security invoker
set search_path = public
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists trg_user_app_state_updated_at on public.user_app_state;
create trigger trg_user_app_state_updated_at
before update on public.user_app_state
for each row execute function public.set_updated_at();
