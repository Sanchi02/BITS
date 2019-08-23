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
#define MAXLINE 1000

typedef struct frame_struct
{
    int seqnum;
    char data[10];
    int packet_size;
    char is_last_packet;
} frame;

frame getframe(char data[], int seqnum1, char last_pkt_flag)
{
    frame sendframe;
    strcpy(sendframe.data, data);
    sendframe.seqnum = seqnum1;
    sendframe.packet_size = sizeof(sendframe.data) / sizeof(char);
    if (last_pkt_flag == 'Y')
    {
        sendframe.is_last_packet = 'Y';
    }
    else
    {
        sendframe.is_last_packet = 'N';
    }
    return sendframe;
}
// Driver code
int main(int argc, char *argv[])
// int main()
{
    int port = atoi(argv[2]);
    int packet_size = atoi(argv[4]);
    int win_size = atoi(argv[5]);

    char buffer[100];
    char *message = "Connection recieved";
    int sockfd, n, he, ch, recv_size;
    char c, fr[200][10];
    int i, count, r, packet_num, len;
    int seqNum = 0;
    int k = 0;
    int ackNum = 0;
    int resendFlag = 0;
    struct timeval tv;
    tv.tv_sec = 10;
    frame arr_win[20];
    frame frames_arr[20];
    struct sockaddr_in servaddr;

    // clear servaddr
    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_addr.s_addr = inet_addr(argv[1]);
    servaddr.sin_port = htons(port);
    servaddr.sin_family = AF_INET;
    fflush(stdin);

    // create datagram socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, (char *)&tv, sizeof(struct timeval));
    // connect to server
    if (connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) < 0)
    {
        printf("\n Error : Connect Failed \n");
        exit(0);
    }

    // request to send datagram
    // no need to specify server address in sendto
    // connect stores the peers IP and port
    sendto(sockfd, message, MAXLINE, 0, (struct sockaddr *)NULL, sizeof(servaddr));

    // waiting for response
    recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr *)NULL, NULL);
    puts(buffer);
    len = sizeof(servaddr);
    int fd = open(argv[3], 0, "O_RDWR");
    if (fd == -1)
        perror("\nFile reading error : \n");
    else
    {
        printf("\nFile read successful.");
    }

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

    for (i = 0; i < packet_num - 1; i++)
    {
        frames_arr[i] = getframe(fr[i], seqNum, 'N');
        seqNum++;
    }
    frames_arr[i] = getframe(fr[i], seqNum, 'Y');
 
    k = 0;
    while (k != packet_num)
    {
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
        while (1)
        {
            if (resendFlag == 1)
            {
                resendFlag = 0;
            }
            for (he = 0; he < i; he++)
            {
                printf("Data to be sent: \n");
                puts(arr_win[he].data);
                printf("\nDo you want to send this packet? Yes:1 or Skip to next packet:0\n ");
                scanf("%d", &ch);
                if (ch == 1)
                {
                    sendto(sockfd, &arr_win[he], MAXLINE, 0, (struct sockaddr *)&servaddr, sizeof(servaddr));
                }
                else
                {
                    continue;
                }
            }

            for (he = 0; he < i; he++)
            {
                recv_size = recvfrom(sockfd, &ackNum, sizeof(int), 0, (struct sockaddr *)&servaddr, &len);
                if (recv_size == -1)
                {
                    if ((errno == EAGAIN) || (errno == EWOULDBLOCK))
                    {
                        printf("\nTimeout has occured.\n");
                        printf("\nResending data\n");
                        resendFlag = 1;
                        break;
                    }
                }
                printf("Acknowledge number recieved is: %d\n", ackNum);
                fflush(stdin);
            }
            if (resendFlag)
            {
                continue;
            }
            else
            {
                break;
            }
        }
    }

    // close the descriptor
    close(sockfd);
}
