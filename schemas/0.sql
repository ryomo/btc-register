-- payment
create table payment
(
  id integer not null
    constraint payment_pk
    primary key autoincrement,
  method int not null,
  amount int,
  created_at int,
  updated_at int
);

-- payment_fiat
create table payment_fiat
(
  id integer not null
    constraint payment_fiat_pk
      primary key autoincrement,
  payment_id int,
  paid int,
  change int,
  created_at int,
  updated_at int
);

create unique index payment_fiat_payment_id_uindex
  on payment_fiat (payment_id);


-- payment_btc
create table payment_btc
(
  id integer not null
    constraint payment_btc_pk
      primary key autoincrement,
  payment_id int,
  satoshi int,
  created_at int,
  updated_at int
);

create unique index payment_btc_payment_id_uindex
  on payment_btc (payment_id);

