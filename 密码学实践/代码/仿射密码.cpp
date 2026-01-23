#include<bits/stdc++.h>
using namespace std;
int MaxDivisor(int , int );
int GetInverse(int , int );
void Ek(char* ,char* ,int  ,int );
void Dk(char* ,char* ,int  ,int );
int main() {
	char massage[10]={0}, ciphertext[10]={0},massage1[10]={0};
	cout<< "请输入明文：";
	cin.getline(massage,10);
	cout<< "请输入密钥："<<endl;
	int a,b;
	cout<< "a=";
	cin>>a; 
	cout<< "b=";
	cin>>b; 
	while(MaxDivisor(a,26)!=1|| b < 0 || b >= 26){
		cout << "密钥有误，a不与26互素，请重新输入密钥 "<<endl;
		cout<< "a=";
		cin>>a; 
		cout<< "b=";
		cin>>b; 
	};
	Ek(ciphertext,massage,a,b);
	cout<< "加密得密文："<<ciphertext<<endl; 
	int ani=GetInverse(a,26);
	cout<< "求得a的逆元为："<<ani<<endl;
	Dk(ciphertext,massage1,ani,b);
	cout<< "解密得密文："<<massage1<<endl; 
	return 0;
}
void Ek(char ciphertext[] ,char massage[] ,int x ,int y){
	int n = strlen(massage);
	for(int i=0;i<n;i++){
		int m = massage[i] - 'a';  // 转换为0-25
        int encrypted = (m * x + y) % 26;
        if (encrypted < 0) encrypted += 26;  // 处理负数情况
        ciphertext[i] = encrypted + 'a';  // 转换回字符
	}
}
void Dk(char ciphertext[] ,char massage1[] ,int x ,int y){
	int n = strlen(ciphertext);
	for(int i=0;i<n;i++){
		int m = ciphertext[i] - 'a';  // 转换为0-25
        int decoded = ((m-y)*x) % 26;
        if (decoded < 0) decoded += 26;  // 处理负数情况
        massage1[i] = decoded + 'a';  // 转换回字符
	}
}
int GetInverse(int m, int n) {
	int x = m, y = n;
	int inv, r;
	for (inv = 2; inv < y; inv++) {
		r = (inv * x) % n;
		if (r == 1 && MaxDivisor(inv, y) == 1 && inv * x > n)
			break;
	}
	return inv;
}
int MaxDivisor(int m, int n) {
	int x = m, y = n;
	int r;
	do {
		r = x % y;
		x = y;
		y = r;
	} while (y != 0);
	return x;
}

