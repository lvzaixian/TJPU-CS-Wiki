#include<bits/stdc++.h>
using namespace std;
void Ek(char*,char*,char*);
int main(){
	char massage[100]={0},ciphertext[100]={0};
	char key[10]={0};
		cout<<"请输入明文：";
		cin.getline(massage,100);
		cout<<"请输入密钥字：";
		cin.getline(key,10);
		Ek(massage,key,ciphertext);
		cout<<"加密得密文为："<<ciphertext<<endl; 
	char massage1[100]={0},ciphertext1[100]={0};
	char key1[10]={0};
		cout<<"请输入明文：";
		cin.getline(massage1,100);
		cout<<"请输入密钥字：";
		cin.getline(key1,10);
		Ek(massage1,key1,ciphertext1);
		cout<<"加密得密文为："<<ciphertext1;
	return 0;
}
void Ek(char* pre,char* going,char* after){
	int n = strlen(going);
	for(int i = 0;i<strlen(pre);i++){
		int m=going[i%n]-'a';
		int n=pre[i]-'a';
		int encrypted=(n+m)%26;
		after[i]=encrypted+'a';
	}
}
