CREATE TABLE IF NOT EXISTS product_id_tracker
(
    product_id bigint NOT NULL,
    crawled boolean DEFAULT false,
    CONSTRAINT product_id_tracker_pkey PRIMARY KEY (product_id)
)