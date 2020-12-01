#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

#include <sys/types.h>
#include <sys/socket.h>

#include <netinet/in.h>
#include <unistd.h>
#include <pthread.h>

#include "cmd.h"
#include "settings.h"
#include "helper.h"

char name[NAME_LENGTH+2];
bool quit;

// Prototypes
void *receive_data(void *pt_sock);
void *send_data(void *pt_sock);
void command(char *send_buffer, int sock);

int main(void) {
    // Initialise globals
    name[0] = '\0';
    quit = false;

    // Create a socket
    int sock;
    check(sock = socket(AF_INET, SOCK_STREAM, 0), "Could not create socket");

    // Specify an address for the server
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(SERVERPORT);
    addr.sin_addr.s_addr = INADDR_ANY;

    // Connect to server
    check(connect(sock, (struct sockaddr *) &addr, sizeof(addr)),
          "Could not connect to server");
    
    // Check if server is full
    char buffer[BUFFER_SIZE];
    check(recv(sock, buffer, sizeof(buffer), 0),
              "Could not receive data from server");
    if (strcmp(buffer, FULL_MSG) == 0) {
        printf("%s", buffer);
        close(sock);
        return 0;
    }

    // Get username and send information to server
    while(true) {
        printf("Enter username: ");
        if (fgets(name, NAME_LENGTH+2, stdin) != NULL) {
            // Check if valid username
            if (strchr(name, '\n') != NULL && name[0] != '\n' && 
                !(name[strcspn(name, "\n")] = '\0') && alnum(name)) {
                // Send to server to check if it is unique
                check(send(sock, name, sizeof(name), 0),
                      "Could not send username to server");
                char buffer[MAX(strlen(UNIQUE_MSG), strlen(NOT_UNIQUE_MSG))+1];
                check(recv(sock, buffer, sizeof(buffer), 0),
                      "Could not receive data from server");
                // Break out of loop if username is unique
                if (strcmp(buffer, UNIQUE_MSG) == 0) {
                    break;
                }
                else {
                    fputs("Username already taken.\n", stdout);
                }
            }
            // Invalid username
            else {
                printf("Username must have at least one character, at most "
                       "%i characters, and must contain only alphanumeric "
                       "characters.\n", NAME_LENGTH);
                // Clear input buffer if at least one character entered
                if (name[0] != '\n') {
                    int c;
                    while ((c = getchar()) != '\n');
                }
            }
        }
        else {
            printf("Error: Could not get username from user");
            exit(EXIT_FAILURE);
        }
    }

    // Receive welcome message from server
    check(recv(sock, buffer, sizeof(buffer), 0),
              "Could not receive data from server");
    printf("%s", buffer);

    // Thread to handle receiving data from server
    void *pt_sock = &sock;
    pthread_t receive_thread;
    check_thread(pthread_create(&receive_thread, NULL, receive_data, pt_sock),
                 "Could not create receive thread");

    // Thread to handle sending data to server
    pthread_t send_thread;
    check_thread(pthread_create(&send_thread, NULL, send_data, pt_sock),
                 "Could not create send thread");

    // Wait for QUIT_CMD
    while(!quit);

    // Wait for threads to finish up
    pthread_join(receive_thread, NULL);
    pthread_join(send_thread, NULL);

    close(sock);
    return 0;
}

// Function for thread that receives data from server
void *receive_data(void *pt_sock) {
    char recv_buffer[BUFFER_SIZE+NAME_LENGTH+12];
    int sock = *((int *) pt_sock);
    while(!quit) {
        check(recv(sock, recv_buffer, sizeof(recv_buffer), 0),
              "Could not receive data from server");
        // Clear current line
        printf("\33[2K\r");
        printf("%s", recv_buffer);
        // Check if name has been changed
        if (starts_with(recv_buffer, "You have changed your username to ")){
            char *new_name = recv_buffer + 34;
            // Trim ".\n" off end
            new_name[strcspn(new_name, ".\n")] = '\0';
            strcpy(name, new_name);
        }
        if (!quit) {
            printf("%s: ", name);
        }
        fflush(stdout);
    }
}

// Function for thread that sends data to server
void *send_data(void *pt_sock) {
    int sock = *((int *) pt_sock);
    char send_buffer[BUFFER_SIZE+2];
    while(!quit) {
        printf("%s: ", name);
        fflush(stdout);
        if (fgets(send_buffer, sizeof(send_buffer), stdin) != NULL) {
            // Check if message has appropriate length
            if (strchr(send_buffer, '\n') != NULL && send_buffer[0] != '\n') {
                check(send(sock, send_buffer, sizeof(send_buffer), 0),
                      "Could not send data to server");
                command(send_buffer, sock);
            }
            else {
                printf("Message must have at least one character and at most "
                       "%i characters. Please try again.\n", BUFFER_SIZE);
                // Clear input buffer if at least one character entered
                if (send_buffer[0] != '\n') {
                    int c;
                    while ((c = getchar()) != '\n');
                }
            }
        }
        else {
            printf("Error: Could not get data from stdin");
            exit(EXIT_FAILURE);
        }
    }
}

// Check if send_buffer is a command and if it is, execute the command
void command(char *send_buffer, int sock) {
    // Commands (valid or invalid) must start with '/'
    if (!starts_with(send_buffer, "/")) {
        return;
    }
    // Help command
    if (strcmp(send_buffer, HELP_CMD) == 0) {
        printf("Valid commands are:\n"
               "- /help                   Show a list of all valid commands\n"
               "- /quit                   Leave the server\n"
               "- /list                   Show a list of all members in the "
               "server\n"
               "- /name <new name>        Change username to <new name>\n"
               "- /pm <user> <message>    Send private <message> to <user>\n");
    }
    // Command to leave server
    else if (strcmp(send_buffer, QUIT_CMD) == 0) {
        quit = true;
    }
    // Command to list names of all members in server
    else if (strcmp(send_buffer, LIST_CMD) == 0) {
        ;
    }
    // Command to change name
    else if (starts_with(send_buffer, NAME_CMD)) {
        ;
    }
    // Command to pm
    else if (starts_with(send_buffer, PM_CMD)) {
        ;
    }
    // Invalid command
    else {
        fputs("Invalid command entered. Use /help for a list of valid "
              "commands.\n", stdout);
    }
}