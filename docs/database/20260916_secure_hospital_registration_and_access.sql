-- Phase 1.7: Secure hospital registration and hospital-scoped access
-- Applied to Supabase project: DrugReminder

-- Public hospital registration is removed.
drop policy if exists allow_public_hospital_registration on public.hospitals;
drop policy if exists hospital_users_insert_own on public.hospital_users;

-- Authenticated users create a hospital and become its hospital_admin atomically.
create or replace function public.register_hospital_with_owner(
    p_hospital_name text,
    p_hospital_type text,
    p_phone text,
    p_email text,
    p_address text,
    p_owner_manager_name text default null,
    p_information text default null
)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
    new_hospital_id uuid;
    new_membership_id uuid;
    current_user_id uuid := auth.uid();
begin
    if current_user_id is null then
        raise exception 'Authentication required';
    end if;

    if p_hospital_type not in ('private', 'government') then
        raise exception 'Invalid hospital type';
    end if;

    insert into public.hospitals (
        hospital_name,
        hospital_type,
        phone,
        email,
        address,
        owner_manager_name,
        information
    )
    values (
        p_hospital_name,
        p_hospital_type,
        nullif(p_phone, ''),
        nullif(p_email, ''),
        p_address,
        nullif(p_owner_manager_name, ''),
        nullif(p_information, '')
    )
    returning id into new_hospital_id;

    insert into public.hospital_users (user_id, hospital_id, role)
    values (current_user_id, new_hospital_id, 'hospital_admin')
    returning id into new_membership_id;

    return jsonb_build_object(
        'hospital_id', new_hospital_id,
        'membership_id', new_membership_id
    );
end;
$$;

revoke all on function public.register_hospital_with_owner(text, text, text, text, text, text, text) from public;
grant execute on function public.register_hospital_with_owner(text, text, text, text, text, text, text) to authenticated;

-- Hospital members can see only their own memberships.
create policy hospital_users_select_own
on public.hospital_users
for select
to authenticated
using (user_id = auth.uid());

-- Hospital members can read/create branches belonging to their hospital.
create policy hospital_branches_select_member
on public.hospital_branches
for select
to authenticated
using (
    exists (
        select 1
        from public.hospital_users hu
        where hu.hospital_id = hospital_branches.hospital_id
          and hu.user_id = auth.uid()
    )
);

create policy hospital_branches_insert_member
on public.hospital_branches
for insert
to authenticated
with check (
    exists (
        select 1
        from public.hospital_users hu
        where hu.hospital_id = hospital_branches.hospital_id
          and hu.user_id = auth.uid()
    )
);

-- Hospital members can read/create departments only inside their hospital's branches.
create policy departments_select_member
on public.departments
for select
to authenticated
using (
    exists (
        select 1
        from public.hospital_branches hb
        join public.hospital_users hu on hu.hospital_id = hb.hospital_id
        where hb.id = departments.branch_id
          and hu.user_id = auth.uid()
    )
);

create policy departments_insert_member
on public.departments
for insert
to authenticated
with check (
    exists (
        select 1
        from public.hospital_branches hb
        join public.hospital_users hu on hu.hospital_id = hb.hospital_id
        where hb.id = departments.branch_id
          and hu.user_id = auth.uid()
    )
);
