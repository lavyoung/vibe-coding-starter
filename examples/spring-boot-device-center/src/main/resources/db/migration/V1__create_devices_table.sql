create table devices (
    id bigint primary key,
    name varchar(128) not null,
    created_at timestamp not null,
    updated_at timestamp not null
);
