all: cliente.o floresta.o
	gcc cliente.o floresta.o -lm -o cliente.bin

cliente.o: cliente.c floresta.h
	gcc -std=c99 -Wall -Werror -c cliente.c

floresta.o: floresta.c floresta.h
	gcc -std=c99 -Wall -Werror -c floresta.c

clean:
	rm *.o
	rm *.bin
