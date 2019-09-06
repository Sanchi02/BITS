#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/wait.h>
#include <sys/types.h>


int fd12[2];
int fd23[2];
int fd13[2];
void *myThreadFun1(void *vargp)
{
	int counter =0;
	int timestamp = 0;
	int res;
	//e1
	counter++;
	printf("E1 : %d\n",counter);
	res = write(fd12[1], &counter, 1);
	//e2
	counter++;
	printf("E2 : %d\n",counter);
	//e3
	counter++;
	printf("E3 : %d\n",counter);
	//e4
	res = read(fd13[0], &timestamp, 1);
	if(timestamp>counter)
		counter = timestamp;
	else
		counter++;
	timestamp = 0;
	printf("E4 : %d\n",counter);
	printf("Value of timestamp in P1: %d\n", counter);
	
}

void *myThreadFun2(void *vargp)
{
	int timestamp = 0;
	int counter = 0;
	int res;
	//e5
	res = read(fd12[0], &timestamp, 1);
	if(timestamp>counter)
		counter = timestamp;
	else
		counter++;
	timestamp = 0;
	printf("E5 : %d\n",counter);
	//e6
	counter++;
	printf("E6 : %d\n",counter);
	res = write(fd23[1], &counter, 1);
	printf("Value of timestamp in P2: %d\n", counter);
}

void *myThreadFun3(void *vargp)
{
	int timestamp = 0;
	int counter = 0;
	int res;
	//e7
	counter++;
	printf("E7 : %d\n",counter);
	//e8
	counter++;
	printf("E8 : %d\n",counter);
	res = write(fd13[1], &counter, 1);
	//e9
	counter++;
	printf("E9 : %d\n",counter);
	//e10
	res = read(fd23[0], &timestamp, 1);
	if(timestamp>counter)
		counter = timestamp;
	else
		counter++;
	timestamp = 0;
	printf("E10 : %d\n",counter);
	printf("Value of timestamp in P3: %d\n", counter);

}

int main() {
	
	pipe (fd12);
	pipe (fd23);
	pipe (fd13);
	pthread_t thread_id1;
	pthread_t thread_id2;
	pthread_t thread_id3;
	pthread_create(&thread_id1, NULL, myThreadFun1, NULL);
	pthread_create(&thread_id2, NULL, myThreadFun2, NULL);
	pthread_create(&thread_id3, NULL, myThreadFun3, NULL);
	pthread_join(thread_id1, NULL);
	pthread_join(thread_id2, NULL);
	pthread_join(thread_id3, NULL);	
	exit(0);


}
