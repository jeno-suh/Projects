server: server.c helper.c
	gcc -o server server.c helper.c -I. -lpthread
client: client.c helper.c
	gcc -o client client.c helper.c -I. -lpthread
test: test.c
	gcc -o test test.c -I. -lpthread