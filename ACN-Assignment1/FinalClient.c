// udp client driver program
#include <stdio.h>
#include <strings.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include <time.h>

#define PORT 5000
#define DELAY 1
#define MAXLINE 1000

typedef struct frame_struct
{
    char is_ack;
    int seqnum;
    char data[30];
    int packet_size;
    char is_last_packet;
} frame;

void delay(int number_of_seconds)
{
    int milli_seconds = 1000 * number_of_seconds;
    clock_t start_time = clock();
    while (clock() < start_time + milli_seconds)
        ;
}
//getFrame function takes data chunk as input and return a frame as output.
frame getframe(char data[], int seqnum1, char last_pkt_flag)
{
    frame sendframe;
    strcpy(sendframe.data, data);
    sendframe.seqnum = seqnum1;
    sendframe.packet_size = strlen(sendframe.data);
    if (last_pkt_flag == 'Y')
    {
        sendframe.is_last_packet = 'Y';
    }
    else
    {
        sendframe.is_last_packet = 'N';
    }
    sendframe.is_ack = 'N';
    return sendframe;
}

int main(int argc, char *argv[])
{
    if (argc < 6)
    {
        printf("Less command line arguments provided than required. Provide five arguments");
        exit(0);
    }
    else if (argc > 6)
    {
        printf("Too many command line arguments than required. Provide five arguments");
        exit(0);
    }
    //Command line arguments are converted to int
    int port = atoi(argv[2]);
    int packet_size = atoi(argv[4]);
    int win_size = atoi(argv[5]);

    char buffer[100];
    char *message = "Connection recieved";
    int sockfd, n, he, ch, recv_size;
    char c, fr[200][30];
    int packet_num, len;
    int count = 0;
    int i = 0;
    int r = 0;
    int seqNum = 0;
    int k = 0;
    int ackNum;
    struct timeval tv;
    struct sockaddr_in servaddr;
    frame arr_win[20], ackFrame;
    frame frames_arr[100];
    tv.tv_sec = 10;

    //Initialization of servaddr
    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_addr.s_addr = inet_addr(argv[1]);
    servaddr.sin_port = htons(port);
    servaddr.sin_family = AF_INET;
    fflush(stdin);

    //Creating datagram socket with UDP protocol
    sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

    //Setting socket options for timeout
    setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, (char *)&tv, sizeof(struct timeval));

    //Connect to server
    if (connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) < 0)
    {
        printf("\n Error : Connect Failed \n");
        exit(0);
    }

    //Sending request to server
    sendto(sockfd, message, MAXLINE, 0, (struct sockaddr *)NULL, sizeof(servaddr));

    //Waiting and recieving response from server
    recv_size = recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr *)NULL, NULL);
    if (recv_size == -1)
    {
        if ((errno == EAGAIN) || (errno == EWOULDBLOCK))
        {
            perror("Timeout has occured.");
            exit(0);
        }
    }
    puts(buffer);
    len = sizeof(servaddr);

    //Reading file
    int fd = open(argv[3], 0, "O_RDWR");
    if (fd == -1)
        perror("\nFile reading error : \n");
    else
    {
        printf("\nFile read successful.\n");
    }

    //Dividing file into equal chunks
    while ((r = read(fd, &c, sizeof(char))) > 0)
    {
        if (count < packet_size - 1)
        {
            fr[i][count++] = c;
        }
        else
        {
            fr[i][count++] = c;
            fr[i][count] = '\0';
            count = 0;
            i++;
        }
    }

    if (fr[i][0])
    {
        fr[i][count] = '\0';
        i++;
    }
    packet_num = i;

    //Converting data chunks of file into frames to be sent to server
    for (i = 0; i < packet_num - 1; i++)
    {
        frames_arr[i] = getframe(fr[i], seqNum, 'N');
        seqNum++;
    }
    frames_arr[i] = getframe(fr[i], seqNum, 'Y');

    k = 0;

    //The loop iterates until all frames are not sent to server
    while (k != packet_num)
    {
        //Frames equal to window size are sent at a time to server
        for (i = 0; i < win_size; i++)
        {
            arr_win[i] = frames_arr[k];
            k++;
            if (k == packet_num)
            {
                i++;
                break;
            }
        }
        //Sending frames to server
        for (he = 0; he < i; he++)
        {
            sendto(sockfd, &arr_win[he], MAXLINE, 0, (struct sockaddr *)&servaddr, sizeof(servaddr));
            printf("----SEND PACKET %d \n", arr_win[he].seqnum);
            delay(DELAY);
        }

        //Waiting for acknowledgement from server
        for (he = 0; he < i; he++)
        {
            recvfrom(sockfd, &ackFrame, sizeof(ackFrame), 0, (struct sockaddr *)&servaddr, &len);
            printf("----RECEIVE ACK %d \n", ackFrame.seqnum);
        }
    }

    //Closing socket descriptor
    printf("----CLOSING CONNECTION \n");
    close(sockfd);
}
