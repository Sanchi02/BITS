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
	int counter[3] ={0,0,0};
	int timestamp[3] = {0,0,0};
	int res;
	int i,j=0;
	//e1
	counter[0]++;
	res = write(fd12[1], &counter, sizeof(counter));
	//e2
	counter[0]++;
	//e3
	counter[0]++;
	//e4
	res = read(fd13[0], &timestamp, sizeof(counter));
	for(i=0;i<3;i++){
		if(timestamp[i]>counter[i])
			counter[i] = timestamp[i];
	}
	counter[0]++;
	printf("For P1\n");
	for(j =0; j<3;j++){
		printf("%d",counter[j]);
	}
	printf("\n");
	
}

void *myThreadFun2(void *vargp)
{
	int counter[3] ={0,0,0};
	int timestamp[3] = {0,0,0};
	int res;
int i,j =0;
	//e5
	res = read(fd12[0], &timestamp, sizeof(counter));
	for(i =0;i<3;i++){
		if(timestamp[i]>counter[i])
			counter[i] = timestamp[i];
	}
	counter[1]++;
	//e6
	counter[1]++;
	res = write(fd23[1], &counter, sizeof(counter));
	printf("For P2\n");
	for(j =0; j<3;j++){
		printf("%d",counter[j]);
	}
	printf("\n");
}

void *myThreadFun3(void *vargp)
{
	int counter[3] ={0,0,0};
	int timestamp[3] = {0,0,0};
	int res;
int i,j =0;
	//e7
	counter[2]++;
	//e8
	counter[2]++;
	res = write(fd13[1], &counter, sizeof(counter));
	//e9
	counter[2]++;
	//e10
	res = read(fd23[0], &timestamp, sizeof(counter));
	for(i=0;i<3;i++){
		if(timestamp[i]>counter[i])
			counter[i] = timestamp[i];
	}
	counter[2]++;
	printf("For P3\n");
	for(j =0; j<3;j++){
		printf("%d",counter[j]);
	}
	printf("\n");

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
