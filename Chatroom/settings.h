#define SERVERPORT 9002
#define SERVER_BACKLOG 5
#define MAX_CLIENTS 10 // MAX_CLIENTS must be an int
#define NAME_LENGTH 10

// BUFFER_SIZE must hbe greater than 50 + MAX_CLIENTS * (NAME_LENGTH+2);
// otherwise, the list command will not operate correctly
#define MAX(a, b) ((a) > (b) ? (a) : (b)) 
#define BUFFER_SIZE MAX(250, 50 + MAX_CLIENTS * (NAME_LENGTH+2))