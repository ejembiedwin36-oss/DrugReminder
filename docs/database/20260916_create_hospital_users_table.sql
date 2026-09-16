-- Phase 1.6: Hospital user ownership
-- Applied to Supabase project: DrugReminder

create table public.hospital_users (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
    hospital_id uuid not null references public.hospitals(id) on delete cascade,
    role text not null check (role in ('hospital_admin', 'doctor', 'nurse', 'pharmacist', 'staff')),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique (user_id, hospital_id)
);

create index hospital_users_user_id_idx
    on public.hospital_users(user_id);

create index hospital_users_hospital_id_idx
    on public.hospital_users(hospital_id);

alter table public.hospital_users enable row level security;

create policy hospital_users_select_own
on public.hospital_users
for select
to authenticated
using (user_id = auth.uid());

create policy hospital_users_insert_own
on public.hospital_users
for insert
to authenticated
with check (user_id = auth.uid());
