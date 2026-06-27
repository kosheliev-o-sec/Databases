
-- Task 1



create or replace function calculate_order_total(p_order_id int)	 --Створюємо функцію, інпут - id замовлення
returns numeric(10,2)	 -- Функція повертає число з двома знаками після коми
language plpgsql 
as $$
declare
total numeric(10,2); 				--Змінна для збереження заг. вартості замовлення
begin 										-- Обчислюємо суму всіх товарів у замовленні

	select coalesce(sum(quantity*price), 0)   -- Замінюємо на 0, якщо sum = null
	into total 	 								-- Зберігаємо результат
	from order_items
	where order_id = p_order_id;  	-- Умова лише для нашого інпут id

	return total;  -- Повертаємо результат
end;
$$;

select calculate_order_total(1);   --Перевірити

--Task 2

create or replace procedure create_order(p_customer_id int) --Створюємо процедуру, інпут - id клієнта
language plpgsql
as $$
begin
	if not exists(				-- Перевіряємо, чи існує клієнт із переданим id
	select *
	from customers
	where customer_id=p_customer_id) 
	then
	raise exception 'Немає клієнта з таким id';  -- Рейзимо помилку, якщо клієнта не існує
end if;

insert into orders( 					 -- Додаємо нове замовлення до таблиці orders
customer_id, order_date, total_amount)

values(p_customer_id, current_timestamp, 0); -- Передаємо значення
end;
$$;

call create_order(5);  -- Викликаємо процедуру
select * from orders;  -- Перевірити


-- Task 3

create or replace procedure add_product_to_order(  --створюємо процедуру
p_order_id int, p_product_id int, p_quantity int)
language plpgsql
as $$
declare 
v_price numeric(10,2); --Збереження ціни та кількості товару
v_in_stock int;
begin
	if p_quantity <= 0    --Перевірка інпуту
	then raise exception 'Неможлива кількість <=0';
end if;

select price, stock_quantity
into v_price, v_in_stock
from products
where product_id = p_product_id;

if v_price is null   
then raise exception 'Такого продукту не існує';

end if;

if v_in_stock < p_quantity --Перевірка на наявність 
then raise exception 'Немає такої кількості. В наявності: %', v_in_stock;
end if;


insert into order_items(   --Додаємо товар у таблицю
order_id, product_id, quantity, price)
values(p_order_id, p_product_id, p_quantity, v_price);

update products p  --Зменшуємо к-сть товару на складі
set stock_quantity = p.stock_quantity - p_quantity
where product_id = p_product_id;

end;
$$;

call add_product_to_order(1, 2, 3); -- Перевірка


---Task 4

create or replace function update_order_total() -- Створюєммо тригерну функцію, яка автоматично оновлює суму замовлення
returns trigger
language plpgsql
as $$
begin
if tg_op = 'DELETE' then  --Змінна що показує яка операція викликала тригер
	update orders
	set total_amount = calculate_order_total(old.order_id)  --Перераховуємо суму для замовлення, використовучи функцію з 1 таски
	where order_id = old.order_id;
else
	update orders
	set total_amount = calculate_order_total(new.order_id)
	where order_id = new.order_id;
end if;

    return null;  -- Для after тригера повертаємо null(результат функції ігнорується)
end;
$$;



create trigger trg_update_order_total  -- Створюємо тригер
after insert or update or delete on order_items -- Він спрацьовує після цих дій для order_items, для кожного рядка окремо
for each row
execute function update_order_total(); -- Викликає функцію



--Task 5


create or replace function order_audit_log()  -- Створюємо тригерну функцію
returns trigger
language plpgsql
as $$
begin

    -- Додаємо запис у таблицю order_log після створення замовлення
    insert into order_log (
        order_id,
        customer_id,
        action, -- Текстовий опис події
        log_date
    )
    values (
        new.order_id,        
        new.customer_id,     
        'order_created',     -- Тип події
        current_timestamp    -- Час(зараз)
    );

    return new;  -- Повертаємо новий рядок
end;
$$;

create trigger trg_order_audit_log 
after insert on orders  -- Тригер спрацює після створення нового  замовлення
for each row
execute function order_audit_log();  -- Виклик тригерної функції



--Testing


insert into customers(full_name, email, balance)
values
('Ivan Petrenko', 'ivan@gmail.com', 222),
('Olena Shevchenko', 'olena@gmail.com', 291);

select * from customers;


insert into products(product_name, price, stock_quantity)
values
('Ice cream', 10, 4000),
('Mouse', 700, 30);

select * from products;



--Створюємо замовлення
call create_order(1);

select * from orders;

--Перевірка ордерів
select * from order_log;


--Додаємо товари
call add_product_to_order(1, 1, 1);
call add_product_to_order(1, 2, 2);

select * from order_items;


--Перевіряємо кількість товару
select * from products;

--Перевіряємо функцію

select calculate_order_total(1);




