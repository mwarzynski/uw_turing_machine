start 0 accept 0 S
start 1 gof1 0 R
start 2 gof2 0 R

gof1 1 checkr 0 R
gof1 1 gof1 1 R
gof1 2 gof1 2 R

gof2 2 checkr 0 R
gof2 1 gof2 1 R
gof2 2 gof2 2 R

checkr 1 gob0 1 L
checkr 2 gob0 2 L

gob0 0 gob0 0 L
gob0 1 gob0x 1 S
gob0 2 gob0x 2 S

gob0x 1 gob0x 1 L
gob0x 2 gob0x 2 L
gob0x 0 start_check_if_ended 0 R


start_check_if_ended 1 scier 1 R
start_check_if_ended 2 scier 2 R

scier 0 scier_true 0 L
scier 1 scier_false 1 L
scier 2 scier_false 2 L

scier_true 1 go1e 0 R
scier_true 2 go2e 0 R
scier_false 1 go1 0 R
scier_false 2 go2 0 R

go1 1 go1 1 R
go1 2 go1 2 R
go1 0 go10 0 R
go10 0 go10 0 R
go10 1 checkr 0 R

go2 1 go2 1 R
go2 2 go2 2 R
go2 0 go20 0 R
go20 0 go20 0 R
go20 2 checkr 0 R

go1e 1 go1e 1 R
go1e 2 go1e 2 R
go1e 0 go10e 0 R
go10e 0 go10e 0 R
go10e 1 checkre 0 R

go2e 1 go2e 1 R
go2e 2 go2e 2 R
go2e 0 go20e 0 R
go20e 0 go20e 0 R
go20e 2 checkre 0 R

checkre 0 accept 0 S
