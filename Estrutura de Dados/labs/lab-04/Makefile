all: cliente.o ficha.o
	gcc cliente.o ficha.o -lm -o cliente.bin

cliente.o: cliente.c ficha.h
	gcc -std=c99 -Wall -Werror -c cliente.c

ficha.o: ficha.c ficha.h
	gcc -std=c99 -Wall -Werror -c ficha.c

clean:
	rm *.o
	rm *.bin
