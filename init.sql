create schema oltp;


create table oltp.user_transactions (
    user_id integer not null,
    amount integer not null,
    created_at timestamp without time zone not null default (current_timestamp at time zone 'utc')
);