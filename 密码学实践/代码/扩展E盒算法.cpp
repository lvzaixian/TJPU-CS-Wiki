#include<bits/stdc++.h>
using namespace std;
int main(){
	int putin[8][4];
	int getout[8][6];
	cout<<"请输入32位比特数据："<<endl;
	for(int i=0;i<8;i++){
		for(int j=0;j<4;j++){
			cin>>putin[i][j];
		}
	}
	for(int i=0;i<8;i++){
		for(int j=0;j<4;j++){
			getout[i][j+1]=putin[i][j];
			getout[i][0]=putin[(i+7)%8][3];
			getout[i][5]=putin[(i+1)%8][0];	
		}
	}
	cout<<"经扩展矩阵E算法得48位比特数据如下："<<endl; 
	for(int i=0;i<8;i++){
		for(int j=0;j<6;j++){
			cout<<getout[i][j]<<' ';
		}
		cout<<endl;
	}
	return 0;
} 
