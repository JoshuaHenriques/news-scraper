create extension if not exists "uuid-ossp";


create table if not exists publisher (
	created_at 			timestamp 		default current_timestamp,    
	updated_at 			timestamp 		default current_timestamp,
    id     				uuid       		not null primary key default uuid_generate_v4(),
    tld   				varchar(255)    not null unique,
    license         	varchar(255)    default 'none'
);

create table if not exists expert (
	created_at 			timestamp 		default current_timestamp,    
	updated_at 			timestamp 		default current_timestamp,
    first_name			varchar(50),    
    last_name			varchar(50),    
    phone				varchar(10),    
	email				varchar(50),	
    id					uuid			not null primary key default uuid_generate_v4()
);


create table if not exists article (
	created_at 			timestamp       default current_timestamp,    
	updated_at 			timestamp       default current_timestamp,
    id      			uuid       		not null primary key default uuid_generate_v4(),
    title	      		varchar(255)    default 'Title not found',
    url			        varchar(255)	not null unique,
    publisher_id       	uuid            not null references publisher(id),
    date    	        varchar(20)     default 'Date not found',
    content    			text     		not null,
    expert        	    varchar(255)    -- Expert should be replaced with the expert field
);


-- is this table necessary?
create table if not exists scraper_profile (
	created_at 			timestamp 		default current_timestamp,    
	updated_at 			timestamp 		default current_timestamp,
    id					uuid       		not null primary key default uuid_generate_v4(),
    status              varchar(255)    default 'initial',
    publisher_id		uuid            not null unique references publisher(id)
);

create table if not exists scraper_queries_log (
	created_at 				timestamp 		default current_timestamp,    
	updated_at 				timestamp 		default current_timestamp,
    id              		uuid     		not null primary key default uuid_generate_v4(),
    user_email              varchar(50)     not null,
    endpoint_accessed       varchar(50)     not null,
    query_data              text			not null
);