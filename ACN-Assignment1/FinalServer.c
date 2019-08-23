// server program for udp connection
#include <stdio.h>
#include <strings.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>
#define PORT 5000
#define MAXLINE 1000
#define DELAY 1

typedef struct frame_struct
{
    char is_ack;
    int seqnum;
    char data[30];
    int packet_size;
    char is_last_packet;
} frame;

//getAckFrame take acknowledgement number as input and returns acknowledgement frame
frame getAckFrame(int ackNum){
    frame ackFrame;
    ackFrame.is_ack='Y';
    ackFrame.seqnum=ackNum;
    ackFrame.is_last_packet='N';
    ackFrame.packet_size = sizeof(int);
    return ackFrame;
}

void delay(int number_of_seconds) 
{ 
    int milli_seconds = 1000 * number_of_seconds; 
    clock_t start_time = clock(); 
    while (clock() < start_time + milli_seconds) 
        ; 
} 

int main()
{
    char buffer[100];
    char *message = "Connected to server";
    int listenfd, len, ch, dupliFlag = 0;
    int ackNumT = 0;
    frame recievedFrame,ackFrame;
    int closeSocketFlag = 0;
    struct sockaddr_in servaddr, cliaddr;
    FILE *fPtr;

    fPtr = fopen("message.txt", "w");
    bzero(&servaddr, sizeof(servaddr));

    //Creating UDP socket
    listenfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(PORT);
    servaddr.sin_family = AF_INET;

    //Binding the server address to socket descriptor
    bind(listenfd, (struct sockaddr *)&servaddr, sizeof(servaddr));

    //Recieve connection request from client
    len = sizeof(cliaddr);
    int n = recvfrom(listenfd, buffer, sizeof(buffer),
                     0, (struct sockaddr *)&cliaddr, &len);
    buffer[n] = '\0';
    puts(buffer);

    //Send response to client
    sendto(listenfd, message, MAXLINE, 0,
           (struct sockaddr *)&cliaddr, sizeof(cliaddr));

    if (fPtr == NULL)
    {
        perror("File error: ");
        exit(EXIT_FAILURE);
    }
    
    //The server keeps listening until the client transmits frame with is_last_frame flag equal to Y
    while (1)
    {   
        //Frames recived from client
        recvfrom(listenfd, &recievedFrame, sizeof(recievedFrame), 0, (struct sockaddr *)NULL, NULL);
        printf("---- RECEIVE PACKET %d length %d LAST PKT %c \n", recievedFrame.seqnum, recievedFrame.packet_size, recievedFrame.is_last_packet);
        
        //The data from frame is written into the file
        fputs(recievedFrame.data, fPtr);

        if (recievedFrame.is_last_packet == 'Y')
        {
            closeSocketFlag = 1;
        }

        fflush(stdin);
        //Sending acknowlegdement to client
        delay(DELAY);
        
        ackFrame = getAckFrame(ackNumT);
        //Send acknowledgement to client
        sendto(listenfd, &ackFrame, sizeof(ackFrame), 0, (struct sockaddr *)&cliaddr, sizeof(cliaddr));
        printf("---- SEND ACK %d \n", ackFrame.seqnum);
        ackNumT++;
        

        //Cleanup
        if (closeSocketFlag)
        {
            printf("----CLOSING CONNECTION \n");
            close(listenfd);
            fclose(fPtr);
            break;
        }
    }
}
