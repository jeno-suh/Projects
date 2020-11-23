#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include <sys/types.h>
#include <sys/socket.h>

#include <netinet/in.h>
#include <unistd.h>
#include <pthread.h>

#include "cmd.h"
#include "settings.h"
#include "helper.h"

// Struct and globals for linked list with dummy header to store client data
typedef struct client {
    int fd;
    char name[NAME_LENGTH+1];
    struct client* prev;
    struct client* next;
} client_node_t;

client_node_t *start;
client_node_t *end;
int client_count = 0;

// Prototypes
void *handle_client(void *pt_client);
bool command(char buffer[], client_node_t *client_node, bool *pt_left);
void send_to_others(client_node_t *client_node, char *msg, int msg_size);
bool unique_name(char *new_name);

int main(void) {
    // Create a socket
    int sock;
    check(sock = socket(AF_INET, SOCK_STREAM, 0), "Could not create socket");

    // Define the server address
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(SERVERPORT);
    addr.sin_addr.s_addr = INADDR_ANY;

    // Bind the socket to our specified IP and port
    check(bind(sock, (struct sockaddr *) &addr, sizeof(addr)),
          "Could not bind server to specified IP and port");

    // Listen for connections
    check(listen(sock, SERVER_BACKLOG), "Could not listen for connections");

    // Initialise linked list with dummy header
    client_node_t *dummy_header = malloc(sizeof(client_node_t));
    if (dummy_header != NULL) {
        dummy_header->prev = NULL;
        dummy_header->next = NULL;
        start = dummy_header;
        end = dummy_header;
    }
    else {
        printf("Error: Could not initialise linked list");
        exit(EXIT_FAILURE);
    }

    printf("Server has initialised.\n");

    // Loop for accepting connections
    while(true) {
        // Accept connection
        int client_fd = accept(sock, NULL, NULL);

        if (client_count < MAX_CLIENTS) {
            // Send server not full message
            char not_full_msg[] = "Server is not full";
            check(send(client_fd, not_full_msg, sizeof(not_full_msg), 0),
                  "Could not send server full message");

            // Get name from client
            char name[NAME_LENGTH+1];
            while(true) {
                check(recv(client_fd, name, sizeof(name), 0), 
                      "Could not receive name from client");
                // If empty string received, go to next iteration
                if (strlen(name) == 0) {
                    continue;
                }
                else if (unique_name(name)) {
                    char msg[] = UNIQUE_MSG;
                    check(send(client_fd, msg, sizeof(msg), 0),
                          "Could not send unique message");
                    break;
                }
                // Username not unique
                else {
                    char msg[] = NOT_UNIQUE_MSG;
                    check(send(client_fd, msg, sizeof(msg), 0),
                          "Could not send not unique message");
                }
            }
            
            // Create node and add to linked list
            client_node_t *client_node = malloc(sizeof(client_node_t));
            if (client_node != NULL) {
                client_node->fd = client_fd;
                strcpy(client_node->name, name);
                client_node->prev = end;
                end->next = client_node;
                client_node->next = NULL;
                end = client_node;
                client_count += 1;
            }
            else {
                printf("Error: Could not create client node");
                exit(EXIT_FAILURE);
            }

            // Notify others that new client has joined
            char join_msg[NAME_LENGTH+14];
            sprintf(join_msg, "%s has joined.\n", name);
            fputs(join_msg, stdout);
            send_to_others(client_node, join_msg, sizeof(join_msg));
            
            // Create thread for handling client
            void *pt_client = client_node;
            pthread_t client_thread;
            check_thread(pthread_create(&client_thread, NULL, handle_client, 
                                        pt_client),
                         "Could not create thread for handling client");

            // Send welcome message to client
            char welcome_msg[] = "Welcome to the server!\n";
            check(send(client_fd, welcome_msg, sizeof(welcome_msg), 0),
                  "Could not send welcome message");
        }
        else {
            // Send server full message
            char full_msg[] = FULL_MSG;
            check(send(client_fd, full_msg, sizeof(full_msg), 0),
                  "Could not send server full message");
            close(client_fd);
        }
    }

    close(sock);
}

// Function for thread that deals with clients
void *handle_client(void *pt_client) {
    client_node_t *client_node = pt_client;
    char buffer[BUFFER_SIZE+2];
    bool left = false;
    // Loop to receive messages from client
    while(!left) {
        check(recv(client_node->fd, buffer, sizeof(buffer), 0), 
              "Could not receive data from client");
        // If empty string received, go to next iteration
        if (strlen(buffer) == 0) {
            continue;
        }
        char msg[BUFFER_SIZE+NAME_LENGTH+4];
        bool *pt_left = &left;
        if (!command(buffer, client_node, pt_left)) {
            // Not a command so client sent a message
            char msg[BUFFER_SIZE+NAME_LENGTH+4];
            sprintf(msg, "%s: %s", client_node->name, buffer);
            fputs(msg, stdout);
            send_to_others(client_node, msg, sizeof(msg));
        }
    }
}

// Return whether buffer contains a command.
// If it is a command, execute the relevant procedures.
bool command(char buffer[], client_node_t *client_node, bool *pt_left) {
    // Client is leaving server
    if (strcmp(buffer, QUIT_CMD) == 0) {
        // Notify other nodes
        char msg[NAME_LENGTH+12];
        sprintf(msg, "%s has left.\n", client_node->name);
        fputs(msg, stdout);
        send_to_others(client_node, msg, sizeof(msg));
        // Send goodbye message to client
        char bye_msg[] = "Goodbye!\n";
        check(send(client_node->fd, bye_msg, sizeof(bye_msg), 0), 
              "Could not send data to client");
        // Delete node and free memory
        if (client_node == end) {
            end = client_node->prev;
            end->next = NULL;
        }
        else {
            client_node->prev->next = client_node->next;
            client_node->next->prev = client_node->prev;
        }
        free(client_node);
        // Update variables
        *pt_left = true;
        client_count -= 1;
    }
    // Client wants names of all clients in server
    else if (strcmp(buffer, LIST_CMD) == 0) {
        printf("Sending a list of all members in the server to %s.\n", 
               client_node->name);
        char list[BUFFER_SIZE];
        if (client_count == 1) {
            sprintf(list, "There is 1 member currently in the server:\n");
        }
        else {
            sprintf(list, "There are %i members currently in the server:\n", 
                    client_count);
        }
        client_node_t *node = start;
        while(node->next != NULL) {
            node = node->next;
            char name[NAME_LENGTH+3];
            if (node->next == NULL) {
                // So, at end of list
                sprintf(name, "%s\n", node->name);
            }
            else {
                // So, in start or middle of list
                sprintf(name, "%s, ", node->name);
            }
            strcat(list, name);
        }
        strcat(list, "\0");
        check(send(client_node->fd, list, sizeof(list), 0), 
              "Could not send data to client");
    }
    // Client is changing name
    else if (starts_with(buffer, NAME_CMD)) {
        char *new_name = buffer + strlen(NAME_CMD);
        // Trim '\n' off end
        new_name[strcspn(new_name, "\n")] = '\0';
        // Changing to same name
        if (strcmp(new_name, client_node->name) == 0) {
            char msg[NAME_LENGTH+40];
            sprintf(msg, "%s is already your current username.\n", new_name);
            check(send(client_node->fd, msg, sizeof(msg), 0), 
                  "Could not send data to client");
        }
        // Changing to different name
        else if (alnum(new_name) && 0 < strlen(new_name) && strlen(new_name) 
                 <= NAME_LENGTH && unique_name(new_name)) {
            // Notify client
            char msg1[NAME_LENGTH+40];
            sprintf(msg1, "You have changed your username to %s.\n", new_name);
            check(send(client_node->fd, msg1, sizeof(msg1), 0), 
                  "Could not send data to client");
            // Notify others
            char msg2[2*NAME_LENGTH+35];
            sprintf(msg2, "%s has changed their username to %s.\n", 
                    client_node->name, new_name);
            fputs(msg2, stdout);
            strcpy(client_node->name, new_name);
            send_to_others(client_node, msg2, sizeof(msg2));
        }
        // Username already taken
        else if (!unique_name(new_name)) {
            char msg[] = "Username already taken.\n";
            check(send(client_node->fd, msg, sizeof(msg), 0), 
                  "Could not send data to client");
        }
        // Invalid username given
        else {
            char msg[150];
            sprintf(msg, "Invalid username entered. Username must have at "
                    "least one character, at most %i characters, and must "
                    "contain only alphanumeric characters.\n", NAME_LENGTH);
            check(send(client_node->fd, msg, sizeof(msg), 0), 
                  "Could not send data to client");
        }
    }
    // Client wants to send a private message
    else if (starts_with(buffer, PM_CMD)) {
        // Check if there is a ' ' after PM_CMD
        char *temp = buffer + strlen(PM_CMD);
        char *name;
        if (strchr(temp, ' ') != NULL) {
            char delim[] = " ";
            name = strtok(temp, delim);
        }
        else {
            char msg[] = "Missing parameter/s. Use /help for details on "
                         "correct usage.\n";
            check(send(client_node->fd, msg, sizeof(msg), 0), 
                  "Could not send data to client");
            return starts_with(buffer, "/");
        }
        // Invalid username
        if (!alnum(name) || 0 == strlen(name) || strlen(name) > NAME_LENGTH) {
            char msg[150];
            sprintf(msg, "Invalid username specified. Username must have at "
                    "least one character, at most %i characters, and must "
                    "contain only alphanumeric characters.\n", NAME_LENGTH);
            check(send(client_node->fd, msg, sizeof(msg), 0), 
                  "Could not send data to client");
        }
        // No user with specified username exists
        else if (unique_name(name)) {
            char msg[] = "Specified user not found.\n";
            check(send(client_node->fd, msg, sizeof(msg), 0), 
                  "Could not send data to client");
        }
        // Specified own username
        else if (strcmp(name, client_node->name) == 0) {
            char msg[] = "Cannot send private message to self.\n";
            check(send(client_node->fd, msg, sizeof(msg), 0), 
                  "Could not send data to client");
        }
        // Correct usage
        else {
            // Get the message
            char *msg = buffer + strlen(PM_CMD) + strlen(name) + 1;
            // msg must contain a '\n' so an 'empty' message has len <= 1
            if (strlen(msg) <= 1) {
                char msg1[] = "Cannot send empty message.\n";
                check(send(client_node->fd, msg1, sizeof(msg1), 0), 
                  "Could not send data to client");
            }
            else {
                // Look for node belonging to 'name' and send msg
                client_node_t *node = start;
                while(node->next != NULL) {
                    node = node->next;
                    if (strcmp(node->name, name) == 0) {
                        printf("PM from %s to %s: ", client_node->name, name);
                        fputs(msg, stdout);
                        char pm[NAME_LENGTH+11 + strlen(msg)];
                        sprintf(pm, "PM from %s: ", client_node->name);
                        strcat(pm, msg);
                        check(send(node->fd, pm, sizeof(pm), 0),
                            "Could not send data to client");
                        break;
                    }
                }
                // Notify client of success
                char success[] = "The PM was sent.\n";
                check(send(client_node->fd, success, sizeof(success), 0),
                    "Could not send data to client");
            }
        }
    }
    return starts_with(buffer, "/");
}

// Send msg to all nodes besides client_node
void send_to_others(client_node_t *client_node, char *msg, int msg_size) {
    client_node_t *node = start;
    while(node->next != NULL) {
        node = node->next;
        if (node != client_node) {
            check(send(node->fd, msg, msg_size, 0),
                  "Could not send data to client");
        }
    }
}

// Return whether new_name is unique i.e. no client has already taken that
// as their username
bool unique_name(char *new_name) {
    client_node_t *node = start;
    while(node->next != NULL) {
        node = node->next;
        if (strcmp(new_name, node->name) == 0) {
            return false;
        }
    }
    return true;
}