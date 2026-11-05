create table categories (
    id integer generated always as identity primary key,
    name text not null
);

create table priorities (
    id integer generated always as identity primary key,
    code text not null unique,
    name text not null,
);

create table statutes (
    id integer generated always as identity primary key,
    cod text not null unique,
    name text not null

);

create table (
    id integer generated always as identity primary key,
    title text not null,
    description text,
    category_id integer not null references categories(id),
    priority_id integer not null references priorities(id),
    status_id integer not null references statutes(id)
)