# TCP File Storage Python Application

This Python application comprises a server and a client for transmitting and storing files over TCP (Transmission Control Protocol). The application provides basic file storage functionality such as uploading files to the server, downloading files from the server, and listing the available files.

## Usage

1. Start the server:

    ```
    python server.py
    ```

2. Then, launch the client and specify the server's IP address and port:

    ```
    python client.py <server_ip> <port>
    ```

3. Once the client is launched, it will connect to the server, and you can utilize the file storage functionality.

## Commands

- **Sign-in(1) <username=/password=>**: it will allow user to sign-in to the server.
- **Log-in(2) <username=/password=>**: it will allow user to log-in to the server.
- **Download(1) <file_name>**: Uploads a file to the server.
- **Upload(2) <file_number> from the list**: Downloads a file from the server.

*Note: "(1)" if user enters this number, it will allow the user to sign-in. / if user enters this number after log-in, new socket will be open and it will allow the user to download.   
*Note: "(2)" if user enters this number, it will allow the user to log-in. / if user enters this number after log-in, new socket will be open and it will allow the user to upload. 
