SELECT * FROM public.funciones_funcion as ff
inner join funciones_asiento
as fa on ff.sala_id = fa.sala_id inner join reservas_reserva as rr
on ff.id = rr.funcion_id

select * from reservas_reserva

select * from reservas_asientoreservado

select * from funciones_sala

select * from funciones_asiento as fa inner join 
funciones_sala as fs on fa.sala_id = fs.id

select * from funciones_sala as fs inner join
funciones_asiento as fa on fs.id = fa.sala_id
inner join funciones_funcion as ff on fs.id = ff.sala_id

select * from funciones_funcion
