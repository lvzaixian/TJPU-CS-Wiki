#include<bits/stdc++.h>
using namespace std;
//换位函数 
void trythis(char a[], int b[], char c[], int x, int y) {
	for (int j = 1; j <= x; j = j + y) {
		for (int i = 2; i <= y; i++)
			a[b[i - 1] + j - 1] = c[b[i] + j - 1];
		a[b[y]+j-1] = c[b[1]+j-1];
	}
}
int main() {
	cout << "请输入明文：" ;
	char message[100];
	scanf("%s", message + 1);
	cout << "请输入加密密钥：";
	char enkey[20];
	//检查密钥是否正确 
	while (1) {
		scanf("%s", enkey + 1);
		if (strlen(message + 1) % strlen(enkey + 1) != 0)
			cout << "密钥有误，请重新输入：";
		else
			break;
	}
	int tem1[20], tem2[20],tema,temb;
	for (int j = 1; j <=strlen(enkey + 1); j++) {
		tem1[j] = enkey[j] - '0';
		tem2[strlen(enkey + 1) + 1 - j] = tem1[j];
	}
	tema = tem2[1];
	for (int j = 2; j <= strlen(enkey + 1); j++) {
		temb = tem2[j];
		tem2[j] = tema;
		tema = temb;
	}
	tem2[1] = tema;
	char message1[100], message2[100];
	int m=strlen(message + 1),n=strlen(enkey + 1);
	trythis(message1, tem1, message, m, n);
	cout << "密文为：" ;
	for (int i = 1; i <= strlen(message + 1); i++)
		cout << message1[i]; cout << endl;
	cout<<"解密密钥为：";
	for (int i = 1; i <= strlen(enkey + 1); i++)
		cout << tem2[i]; cout << endl;
	trythis(message2,tem2,message1,m,n);
	cout << "明文为：" ;
	for (int i = 1; i <= strlen(message + 1); i++)
		cout << message2[i];
	return 0;
}
