@ECHO OFF

IF NOT EXIST cliente.c (
    @ECHO Arquivo cliente.c nao encontrado
    PAUSE
    EXIT /B
)
IF NOT EXIST labirinto.c (
    @ECHO Arquivo labirinto.c nao encontrado
    PAUSE
    EXIT /B
)
IF NOT EXIST labirinto.h (
    @ECHO Arquivo labirinto.h nao encontrado
    PAUSE
    EXIT /B
)
IF NOT EXIST Makefile (
    @ECHO Arquivo Makefile nao encontrado
    PAUSE
    EXIT /B
)
IF NOT EXIST TESTES\ (
    @ECHO A subpasta de testes nao existe
    PAUSE
    EXIT /B
)

IF EXIST TESTES\01.txt DEL /F TESTES\01.txt
IF EXIST TESTES\02.txt DEL /F TESTES\02.txt
IF EXIST TESTES\03.txt DEL /F TESTES\03.txt
IF EXIST TESTES\04.txt DEL /F TESTES\04.txt
IF EXIST TESTES\05.txt DEL /F TESTES\05.txt
IF EXIST TESTES\06.txt DEL /F TESTES\06.txt
IF EXIST TESTES\07.txt DEL /F TESTES\07.txt
IF EXIST TESTES\08.txt DEL /F TESTES\08.txt
IF EXIST TESTES\09.txt DEL /F TESTES\09.txt

mingw32-make

cliente.bin < TESTES\01.in >> TESTES\01.txt
cliente.bin < TESTES\02.in >> TESTES\02.txt
cliente.bin < TESTES\03.in >> TESTES\03.txt
cliente.bin < TESTES\04.in >> TESTES\04.txt
cliente.bin < TESTES\05.in >> TESTES\05.txt
cliente.bin < TESTES\06.in >> TESTES\06.txt
cliente.bin < TESTES\07.in >> TESTES\07.txt
cliente.bin < TESTES\08.in >> TESTES\08.txt
cliente.bin < TESTES\09.in >> TESTES\09.txt

IF EXIST TESTES\Resultado.txt DEL /F TESTES\Resultado.txt

FC TESTES\01.txt TESTES\01.out >> TESTES\Resultado.txt
FC TESTES\02.txt TESTES\02.out >> TESTES\Resultado.txt
FC TESTES\03.txt TESTES\03.out >> TESTES\Resultado.txt
FC TESTES\04.txt TESTES\04.out >> TESTES\Resultado.txt
FC TESTES\05.txt TESTES\05.out >> TESTES\Resultado.txt
FC TESTES\06.txt TESTES\06.out >> TESTES\Resultado.txt
FC TESTES\07.txt TESTES\07.out >> TESTES\Resultado.txt
FC TESTES\08.txt TESTES\08.out >> TESTES\Resultado.txt
FC TESTES\09.txt TESTES\09.out >> TESTES\Resultado.txt

@ECHO Os resultados estao disponiveis no arquivo Resultado.txt dentro da pasta TESTES
PAUSE
