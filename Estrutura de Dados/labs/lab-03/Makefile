all: cliente.o labirinto.o
	gcc cliente.o labirinto.o -lm -o cliente.bin

cliente.o: cliente.c labirinto.h
	gcc -std=c99 -Wall -Werror -c cliente.c

labirinto.o: labirinto.c labirinto.h
	gcc -std=c99 -Wall -Werror -c labirinto.c

clean:
	rm *.o
	rm *.bin
