#include<bits/stdc++.h>
using namespace std;
int maxdivisor(int m,int n){
	int x=m,y=n;
	int r;
	do{
		r=x%y;
		x=y;
		y=r;
	}while(y!=0);
	return x;                                  
}
int GetInverse(int a,int mod){
	for(int i=1;i<mod;i++){
		int r=a*i;
		if(r%mod==1) return i;
	}
	return -1;
}
int fastpow(int x,int y,int mod){
	int res=1;
	while(y!=0){
		if(y&1) res=(res*x)%mod;
		x=x*x%mod;
		y>>=1;
	}
	return res;
}
bool sushu(int n) {
    if (n <= 1) return false;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) return false;
    }
    return true;
}
int main(){
	int p,q,e,m;
	int n,fain;
	int d,c;
	int times=2;
	int time=1;
	while(times--){
		cout<<"第"<<time<<"次加解密-----------------------------------------------"<<endl;
		cout<<"输入素数p，q：";
	cin>>p>>q;
	if(!(sushu(p)&sushu(q))){
		cout<<"输入的p,q并不全是素数，请重新输入：";
		cin>>p>>q;
	}
	n=p*q;
	fain=(p-1)*(q-1);
	cout<<"计算得n,φ(n)分别为："<<n<<' '<<fain<<endl;
	cout<<"输入公钥e:";
	cin>>e;
	if(maxdivisor(e,fain)!=1){
		cout<<"输入的公钥e不与φ(n)互素，请重新输入：";
		cin>>e;
	}
	cout<<"输入要加密的消息m："; 
	cin>>m;
	d=GetInverse(e,fain);
	cout<<"计算得私钥d为："<<d<<endl;
	c=fastpow(m,e,n);
	cout<<"计算得密文c为："<<c<<endl;
	m=fastpow(c,d,n);
	cout<<"解密得明文m为："<<m<<endl;
	time++;
	}
	return 0;
} 
