create table device_images (
    id bigint primary key,
    device_id bigint not null,
    image_url varchar(512) not null,
    created_at timestamp not null,
    constraint fk_device_images_device
        foreign key (device_id) references devices (id)
);
