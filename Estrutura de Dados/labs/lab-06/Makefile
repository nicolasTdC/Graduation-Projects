all: cliente.o gerenciador.o
	gcc cliente.o gerenciador.o -o cliente.bin

cliente.o: cliente.c gerenciador.h
	gcc -std=c99 -Wall -Werror -c cliente.c

gerenciador.o: gerenciador.c gerenciador.h
	gcc -std=c99 -Wall -Werror -c gerenciador.c

clean:
	rm -f *.o
	rm -f cliente.bin
