#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <limits.h>

#define PORT 80
#define BUFFER_SIZE 1024
#define DEFAULT_FILE "index.html"

void send_response(int client_sock, const char *status, const char *content_type, const char *content, size_t content_length) {
    char header[BUFFER_SIZE];
    snprintf(header, sizeof(header),
             "HTTP/1.1 %s\r\n"
             "Content-Type: %s\r\n"
             "Content-Length: %zu\r\n"
             "\r\n",
             status, content_type, content_length);
    send(client_sock, header, strlen(header), 0);
    send(client_sock, content, content_length, 0);
}

void handle_client(int client_sock) {
    char buffer[BUFFER_SIZE];
    ssize_t bytes_read = read(client_sock, buffer, sizeof(buffer) - 1);
    if (bytes_read < 0) {
        perror("Failed to read from client");
        close(client_sock);
        return;
    }
    buffer[bytes_read] = '\0';


    char method[BUFFER_SIZE], path[BUFFER_SIZE], protocol[BUFFER_SIZE];
    sscanf(buffer, "%s %s %s", method, path, protocol);


    printf("Received request: %s %s %s\n", method, path, protocol);


    if (strstr(path, "..") != NULL) {
        const char *bad_request = "Bad Request";
        send_response(client_sock, "400 Bad Request", "text/html", bad_request, strlen(bad_request));
        close(client_sock);
        return;
    }


    if (strcmp(path, "/") == 0) {
        strcpy(path, DEFAULT_FILE);
    }


    char full_path[PATH_MAX];
    if (path[0] == '/') {
        snprintf(full_path, sizeof(full_path), "%s", path);
    } else {
        snprintf(full_path, sizeof(full_path), "./%s", path);
    }


    printf("Final path to serve: %s\n", full_path);


    int file_fd = open(full_path, O_RDONLY);
    if (file_fd < 0) {

        perror("Failed to open requested file");
        const char *not_found = "404 Not Found";
        const char *not_found_message = "<html><body><h1>404 Not Found</h1></body></html>";
        send_response(client_sock, not_found, "text/html", not_found_message, strlen(not_found_message));
    } else {

        struct stat file_stat;
        fstat(file_fd, &file_stat);
        char *file_content = malloc(file_stat.st_size);
        read(file_fd, file_content, file_stat.st_size);
        send_response(client_sock, "200 OK", "text/html", file_content, file_stat.st_size);
        free(file_content);
        close(file_fd);
    }

    close(client_sock);
}

int main() {
    int server_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (server_sock < 0) {
        perror("Failed to create socket");
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    if (bind(server_sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Failed to bind socket");
        close(server_sock);
        exit(EXIT_FAILURE);
    }

    if (listen(server_sock, 10) < 0) {
        perror("Failed to listen on socket");
        close(server_sock);
        exit(EXIT_FAILURE);
    }

    printf("Server listening on port %d\n", PORT);

    while (1) {
        struct sockaddr_in client_addr;
        socklen_t client_addr_len = sizeof(client_addr);
        int client_sock = accept(server_sock, (struct sockaddr *)&client_addr, &client_addr_len);
        if (client_sock < 0) {
            perror("Failed to accept connection");
            continue;
        }

        handle_client(client_sock);
    }

    close(server_sock);
    return 0;
}
