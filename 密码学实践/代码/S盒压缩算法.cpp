#include<bits/stdc++.h>
using namespace std;
int convert2_10(int n, int* a) {
    int number = 0;
    for (int i = 0; i < n; i++) {
        number = number * 2 + a[i]; // 逐位累加
    }
    return number;
}
void convert10_2(int n,int* b){
	for(int i=3;i>=0;i--){
		b[i]=n%2;
		n=n/2;
	}
}
int main(){
	int s[4][16]={
		{12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11}, 
        {10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8}, 
        {9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6},
        {4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13}
	};
	cout<<"S盒如下："<<endl;
	for(int i=0;i<4;i++){
		for(int j=0;j<16;j++){
			cout<<s[i][j]<<' ';
		}
		cout<<endl;
	}
	int input[6]={0},output[4]={0};
	int length_output=4;
	for(int k=0;k<2;k++){
	cout<<"请输入要进行压缩的6比特数据:";
	for(int i=0;i<6;i++){
		cin>>input[i];
	}
	cout<<endl;
	int midnum1[2]={0},midnum2[4]={0};
	midnum1[0]=input[0];
	midnum1[1]=input[5];
	for(int i=0;i<4;i++){
		midnum2[i]=input[i+1];
	}
	int num1=0,num2=0;
	num1=convert2_10(2,midnum1);
	num2=convert2_10(4,midnum2);
	int num3=s[num1][num2];
	convert10_2(num3,output) ;
	cout<<"压缩结果为："; 
	for(int i=0;i<length_output;i++){
		cout<<output[i]<<' ';
	}
	cout<<endl;
		}
	return 0;
}
