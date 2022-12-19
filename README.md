# Employee manager
## This is a simple web application to manage employees work duration.
To run this project do as follows:   
1- Download project or clone it using this command: 
```
git clone https://github.com/javadadabi/manage_employee
```
2- Install virtual environment for Python:    
In Unix or Mac: ```python3 -m pip install --user virtualenv ```   
In Windows: ```py -m pip install --user virtualenv ```   
3- Create a virtualenv using this command:    
In Unix or Mac:```python3 -m venv env```    
In Windows:```py -m venv env```   
4- Activate env :    
In Unix/mac: ```source env/bin/activate```    
IN windows:```.env\Scripts\activate```    
5_a- Extract manage_employee-master and Navigate to project directory while venv is active. for example:
```
cd manage_employee-master
```
5_b- Install requirements using requirements.txt file:    
In Unix/mac: ```python3 -m pip install -r requirements.txt```    
In windows:  ```py -m pip install -r requirements.txt```    
6- Our database engine is postgresql, so it's a time to use psql shell, to run some commands    
In Unix/mac: ```sudo -u postgres psql```      
In windows: search psql in start menu and run sql shell    
7- Run some configuration commands before creating user and database   :
```
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;
SET default_tablespace = '';
SET default_table_access_method = heap;
```
8- Create a user: username:employee_manager password:your_password:
```
CREATE USER employee_manager WITH PASSWORD 'your_password';
```
9- Warning: we want to drop database employee_manager if exist in this step,
so make sure there is no database named employee_manager filled by valuable data, unless, skip this step:
```
--Terminate databse connection before dropping 
SELECT 
    pg_terminate_backend(pid) 
FROM 
    pg_stat_activity 
WHERE 
    -- don't kill my own connection!
    pid <> pg_backend_pid()
    -- don't kill the connections to other databases
    AND 
	datname = 'employee_manager'
    ;

--DROP DATABASE IF EXISTS

DROP DATABASE IF EXISTS employee_manager;
```
10- Create employee_manager database:
```
CREATE DATABASE employee_manager WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';
```
‍‍‍‍‍‍‍11- change employee_manager database owner to employee_manager user:
```
ALTER DATABASE employee_manager OWNER TO employee_manager;
```
12- connect to employee_manager as employee_manager user:
```
\connect employee_manager
```
After that your shell user will appear like this: employee_manager# instead of #postgres  
13- Although there is an easy way to create database schema but in we want to have a deep   
learning issue about database creation using sql commands, so you can do as follows, or skip and jump to step 14:    
13_a- Create auth_group table (note that because we are creating auth_group table inside public schema,   
so we add public. before its name), change its owner to employee_manager, and change id column such that   
increment automatically:
```
CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);
ALTER TABLE public.auth_group OWNER TO employee_manager;
ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
```
We will create other auth tables as follows:
```
CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
ALTER TABLE public.auth_group_permissions OWNER TO employee_manager;
ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    codename character varying(100) NOT NULL,
    content_type_id integer NOT NULL
);
ALTER TABLE public.auth_permission OWNER TO employee_manager;
ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);
ALTER TABLE public.auth_user OWNER TO employee_manager;
CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);
ALTER TABLE public.auth_user_groups OWNER TO employee_manager;
ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);
ALTER TABLE public.auth_user_user_permissions OWNER TO employee_manager;
ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
```
13_b- Create admin tables:
```
CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);
ALTER TABLE public.django_admin_log OWNER TO employee_manager;
ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
```
13_c- Create django_content_type tables:
```
CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
ALTER TABLE public.django_content_type OWNER TO employee_manager;
ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
```
13_d- Create django_migration table:
```
CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);
ALTER TABLE public.django_migrations OWNER TO employee_manager;
ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
```
13_e- Create django_session:
```
CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
ALTER TABLE public.django_session OWNER TO employee_manager;
```
13_f- Create employee_manager tables:
```
CREATE TABLE public.employee_manager_employee (
    employee_number integer NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(100) NOT NULL,
    slug character varying(152) NOT NULL,
    gender character varying(1) NOT NULL,
    hire_date date,
    salary numeric(12,2),
    remark text,
    user_id integer,
    CONSTRAINT employee_manager_employee_employee_number_check CHECK ((employee_number >= 0))
);
ALTER TABLE public.employee_manager_employee OWNER TO employee_manager;
CREATE TABLE public.employee_manager_employee_responsibilities (
    id bigint NOT NULL,
    employee_id integer NOT NULL,
    responsibility_id character varying(150) NOT NULL
);
ALTER TABLE public.employee_manager_employee_responsibilities OWNER TO employee_manager;
ALTER TABLE public.employee_manager_employee_responsibilities ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.employee_manager_employee_responsibilities_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
CREATE TABLE public.employee_manager_responsibility (
    responsibility_name character varying(150) NOT NULL,
    slug character varying(150) NOT NULL,
    rank smallint,
    description text NOT NULL,
    minimum_salary numeric(12,2),
    maximum_salary numeric(12,2),
    CONSTRAINT employee_manager_responsibility_rank_check CHECK ((rank >= 0))
);
ALTER TABLE public.employee_manager_responsibility OWNER TO employee_manager;
CREATE TABLE public.employee_manager_task (
    id bigint NOT NULL,
    task_name character varying(200) NOT NULL,
    slug character varying(200) NOT NULL,
    description text,
    start_time timestamp with time zone NOT NULL,
    expected_duration interval,
    end_time timestamp with time zone,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    done boolean NOT NULL,
    belong_to_work_id bigint NOT NULL,
    employee_id integer NOT NULL
);
ALTER TABLE public.employee_manager_task OWNER TO employee_manager;
ALTER TABLE public.employee_manager_task ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.employee_manager_task_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
CREATE TABLE public.employee_manager_work (
    id bigint NOT NULL,
    work_title character varying(200) NOT NULL,
    slug character varying(200) NOT NULL,
    description text,
    begin_time timestamp with time zone NOT NULL,
    expected_duration interval,
    end_time timestamp with time zone,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    done boolean NOT NULL
);
ALTER TABLE public.employee_manager_work OWNER TO employee_manager;
ALTER TABLE public.employee_manager_work ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.employee_manager_work_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
```
13_g- Add some constraints to created tables.(Note that these constraints make some changes to   
column properties or make relationship between tables):
```
ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);
    
ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);

ALTER TABLE ONLY public.employee_manager_employee_responsibilities
    ADD CONSTRAINT employee_manager_employe_employee_id_responsibili_5bca72bc_uniq UNIQUE (employee_id, responsibility_id);

ALTER TABLE ONLY public.employee_manager_employee
    ADD CONSTRAINT employee_manager_employee_pkey PRIMARY KEY (employee_number);

ALTER TABLE ONLY public.employee_manager_employee_responsibilities
    ADD CONSTRAINT employee_manager_employee_responsibilities_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.employee_manager_employee
    ADD CONSTRAINT employee_manager_employee_user_id_key UNIQUE (user_id);

ALTER TABLE ONLY public.employee_manager_responsibility
    ADD CONSTRAINT employee_manager_responsibility_pkey PRIMARY KEY (responsibility_name);

ALTER TABLE ONLY public.employee_manager_responsibility
    ADD CONSTRAINT employee_manager_responsibility_rank_key UNIQUE (rank);

ALTER TABLE ONLY public.employee_manager_responsibility
    ADD CONSTRAINT employee_manager_responsibility_slug_key UNIQUE (slug);

ALTER TABLE ONLY public.employee_manager_task
    ADD CONSTRAINT employee_manager_task_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.employee_manager_work
    ADD CONSTRAINT employee_manager_work_pkey PRIMARY KEY (id);
```
13_h- It's the time to create some indexes in database:
```
CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);

CREATE INDEX employee_ma_last_na_86746d_idx ON public.employee_manager_employee USING btree (last_name, first_name);

CREATE INDEX employee_ma_task_na_4bf64a_idx ON public.employee_manager_task USING btree (task_name);

CREATE INDEX employee_manager_employe_responsibility_id_e458a546_like ON public.employee_manager_employee_responsibilities USING btree (responsibility_id varchar_pattern_ops);

CREATE INDEX employee_manager_employee__responsibility_id_e458a546 ON public.employee_manager_employee_responsibilities USING btree (responsibility_id);

CREATE INDEX employee_manager_employee_responsibilities_employee_id_3c4304e4 ON public.employee_manager_employee_responsibilities USING btree (employee_id);

CREATE INDEX employee_manager_employee_slug_93ff0efa ON public.employee_manager_employee USING btree (slug);

CREATE INDEX employee_manager_employee_slug_93ff0efa_like ON public.employee_manager_employee USING btree (slug varchar_pattern_ops);

CREATE INDEX employee_manager_respons_responsibility_name_fca94e92_like ON public.employee_manager_responsibility USING btree (responsibility_name varchar_pattern_ops);

CREATE INDEX employee_manager_responsibility_slug_b164143b_like ON public.employee_manager_responsibility USING btree (slug varchar_pattern_ops);

CREATE INDEX employee_manager_task_belong_to_work_id_45f804a5 ON public.employee_manager_task USING btree (belong_to_work_id);

CREATE INDEX employee_manager_task_employee_id_50fcab1e ON public.employee_manager_task USING btree (employee_id);

CREATE INDEX employee_manager_task_slug_e946dd5f ON public.employee_manager_task USING btree (slug);

CREATE INDEX employee_manager_task_slug_e946dd5f_like ON public.employee_manager_task USING btree (slug varchar_pattern_ops);

CREATE INDEX employee_manager_work_slug_15d52161 ON public.employee_manager_work USING btree (slug);

CREATE INDEX employee_manager_work_slug_15d52161_like ON public.employee_manager_work USING btree (slug varchar_pattern_ops);
```
13_i- Create other constraints:
```
ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.employee_manager_employee_responsibilities
    ADD CONSTRAINT employee_manager_emp_employee_id_3c4304e4_fk_employee_ FOREIGN KEY (employee_id) REFERENCES public.employee_manager_employee(employee_number) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.employee_manager_employee_responsibilities
    ADD CONSTRAINT employee_manager_emp_responsibility_id_e458a546_fk_employee_ FOREIGN KEY (responsibility_id) REFERENCES public.employee_manager_responsibility(responsibility_name) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.employee_manager_employee
    ADD CONSTRAINT employee_manager_employee_user_id_8c766728_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.employee_manager_task
    ADD CONSTRAINT employee_manager_tas_belong_to_work_id_45f804a5_fk_employee_ FOREIGN KEY (belong_to_work_id) REFERENCES public.employee_manager_work(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.employee_manager_task
    ADD CONSTRAINT employee_manager_tas_employee_id_50fcab1e_fk_employee_ FOREIGN KEY (employee_id) REFERENCES public.employee_manager_employee(employee_number) DEFERRABLE INITIALLY DEFERRED;
-- Database creation completed
```
14- Database creation completed, now exit psql shel by pressing backslash+q , if needed press ctrl+d to exit    
14_note- If you fill it was boring work, we have prepared a migration script for you to automate execution of this boring tasks.
Just in your activated virtual environment terminal type this:
```
python my_db_migrator.py
```
15- If you skipped step 13 and wand to create database schema using  django migrations do as follows, unless, jump to step 16:     
15_a- Make migrations at first:
```
python manage.py makemigrations
```
15_b- Apply django migration to database: 
```
python manage.py migrate
```
16- Create super user:
```
python manage.py createsuperuser
```
17- Run django server:
```
python manage.py runserver 
```
18- Open your web browser and go to address http://127.0.0.1:8000/   
19- Login to site using superuser and password.    
20- As it's the first time you logged in to the site, go to admin page using admin panel link   
21- Site admin and staff users can add employees(Note that prior to define     
an employee, his/her responsibility and user must be defined. So it is better to let employees _who you want to access    
the site_ to sign up at first). A Work can only defined by staff users. Each work can be done with one or more than    
one task. So you can define a work based on a project period, or monthly rooting works.    
That's it, Enjoy.
