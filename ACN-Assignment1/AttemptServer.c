// server program for udp connection 
#include <stdio.h> 
#include <strings.h> 
#include <sys/types.h> 
#include <arpa/inet.h> 
#include <sys/socket.h> 
#include<netinet/in.h>
#include<unistd.h> 
#include<stdlib.h>
#define PORT 5000 
#define MAXLINE 1000 

typedef struct frame_struct
{
    int seqnum;
    char data[10];
    int packet_size;
    char is_last_packet;
} frame;

void delay(int number_of_seconds) 
{ 
    // Converting time into milli_seconds 
    int milli_seconds = 1000 * number_of_seconds; 
  
    // Stroing start time 
    clock_t start_time = clock(); 
  
    // looping till required time is not acheived 
    while (clock() < start_time + milli_seconds) 
        ; 
} 

// Driver code 
int main() 
{ 
	char buffer[100]; 
	char *message = "Connected to server"; 
	int listenfd, len,ch,dupliFlag=0,ackNum=0;
    frame recievedFrame;
    int closeSocketFlag=0;
	struct sockaddr_in servaddr, cliaddr; 
    FILE * fPtr;
    fPtr = fopen("message.txt", "w");
	bzero(&servaddr, sizeof(servaddr)); 

	//Creating UDP socket 
	listenfd = socket(AF_INET, SOCK_DGRAM, 0);		 
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY); 
	servaddr.sin_port = htons(PORT); 
	servaddr.sin_family = AF_INET; 

	//Binding the server address to socket descriptor 
	bind(listenfd, (struct sockaddr*)&servaddr, sizeof(servaddr)); 
	
	//Recieve connection request from client
	len = sizeof(cliaddr); 
	int n = recvfrom(listenfd, buffer, sizeof(buffer), 
			0, (struct sockaddr*)&cliaddr,&len); 
	buffer[n] = '\0'; 
	puts(buffer); 
		
	//Send response to client 
	sendto(listenfd, message, MAXLINE, 0, 
		(struct sockaddr*)&cliaddr, sizeof(cliaddr)); 

    if(fPtr == NULL)
    {
        perror("File error: ");
        exit(EXIT_FAILURE);
    }

    while(1){
        dupliFlag=0;
        recvfrom(listenfd, &recievedFrame, sizeof(recievedFrame), 0, (struct sockaddr *)NULL, NULL);
        printf("\nThe data recieved from server is:\n");
        puts(recievedFrame.data);

        //Check for inorder delivery. If the expected acknowledge number doesn't match the incoming sequence number,
        //either we have recieved out of order delivery that is a packet was lost in the middle or we have recieved
        //duplicate frame because one of our acknowledgements was lost.
        if(recievedFrame.seqnum==ackNum){
             printf("Recieved inorder delivery %d\n",recievedFrame.seqnum);
             fputs(recievedFrame.data, fPtr);
             if(recievedFrame.is_last_packet=='Y'){
                closeSocketFlag=1;
             }
        }
        else{
            if(recievedFrame.seqnum<ackNum) {
                dupliFlag=1;
                printf("Recieved number : %d\n",recievedFrame.seqnum);
                printf("Duplicate packet recieved.Discarding packet.");
            }
            if(dupliFlag==0)
            {
                printf("Expected packet number not recieved. Discarding packet.\n");
                printf("Recieved number : %d\n",recievedFrame.seqnum);
                continue;
            }
        }

        fflush(stdin);
        printf("\nDo you want to send ack?Answer 0-No 1-Yes\n");
        scanf("%d",&ch);
        if(ch==1)
        {
            //Sending acknowlegdement to client
            sendto(listenfd, &ackNum, MAXLINE, 0, (struct sockaddr*)&cliaddr, sizeof(cliaddr));
            if(dupliFlag==0){
                ackNum++;
            }
        }
        else
        {
            ackNum++;
            continue;
        }
        //Cleanup
        if(closeSocketFlag){
            close(listenfd);
            fclose(fPtr);
            break;
        }
    }
} 
