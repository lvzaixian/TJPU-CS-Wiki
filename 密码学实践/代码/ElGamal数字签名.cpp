#include<bits/stdc++.h>
using namespace std;
int GetInverse(int a,int mod){
	for(int i=1;i<mod;i++){
		int r=a*i;
		if(r%mod==1) return i;
	}
	return -1;
}
// 快速幂取模 (a^b % mod)
long long fastpow(long long a, long long b, long long mod) {
    long long res = 1;
    while (b > 0) {
        if (b % 2 == 1) res = (res * a) % mod;
        a = (a * a) % mod;
        b /= 2;
    }
    return res;
}
// 检查 g 是否是原根（最暴力方式）
bool is_primitive_root_super_brute(int g, int p) {
    vector<int> residues; // 存储 g^1, g^2, ..., g^{p-1} mod p
    for (int k = 1; k <= p - 1; ++k) {
        int val = fastpow(g, k, p);
        // 如果出现重复，说明不是原根
        if (find(residues.begin(), residues.end(), val) != residues.end()) {
            return false;
        }
        residues.push_back(val);
    }
    // 检查是否覆盖 1~p-1
    for (int i = 1; i <= p - 1; ++i) {
        if (find(residues.begin(), residues.end(), i) == residues.end()) {
            return false;
        }
    }
    return true;
}
// 暴力查找最小的原根
int find_primitive_root_super_brute(int p) {
    if (p == 2) return 1; // 特殊情况
    for (int g = 2; g < p; ++g) {
        if (is_primitive_root_super_brute(g, p)) {
            return g;
        }
    }
    return -1; // 理论上素数总有原根
}
bool sushu(int n) {
    if (n <= 1) return false;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) return false;
    }
    return true;
}
int main(){
	int p,x,m,k;
	int g,y,r,s;
	cout<<"请输入素数p：";cin>>p;
	if(!sushu(p)){
		cout<<"不是素数，请重新输入素数p：";cin>>p;
	}
	g=find_primitive_root_super_brute(p);
	cout<<"求得生成元g为："<<g<<endl<<"请输入私钥x:";
	cin>>x;
	y=fastpow(g,x,p);
	cout<<"计算得公钥y为："<<y<<endl<<"请输入要签名的消息m：";
	cin>>m;
	cout<<"输入随机数k：";cin>>k;
	r=fastpow(g,k,p);
	s=(m-x*r)*GetInverse(k,p-1)%(p-1);
	while(1){
		if(s>0) break;
		s+=p-1;
	}
	cout<<"计算得签名为：r="<<r<<",s="<<s<<endl;
	int left,right;
	left=(fastpow(y,r,p)*fastpow(r,s,p))%p;
	right=fastpow(g,m,p);
	if(left==right){
		cout<<"签名验证结果为Ture，该签名有效！";
	}
	else cout<<"签名验证结果为False，该签名无效！";
	return 0;
}
