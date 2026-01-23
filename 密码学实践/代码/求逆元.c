#include <stdio.h>
int GetInverse(int m,int n){
	int x=m,y=n;
	int inv,r;
	for(inv=2;inv<y;inv++){
		r=(inv*x)%n;
		if(r==1&&MaxDivisor(inv,y)==1&&inv*x>n)
		break;
	}  
	return inv;    
}
int MaxDivisor(int m,int n){
	int x=m,y=n;
	int r;
	do{
		r=x%y;
		x=y;
		y=r;
	}while(y!=0);
	return x;                                  
}
int main()
{
	int a,n;
	printf("请输入整数a：");
	scanf("%d",&a);
	printf("请输入模数n：");
	scanf("%d",&n);
	if(MaxDivisor(a,n)!=1){
			printf("a,n不互素，请重新输入！\n");
	printf("输入整数a：");
	scanf("%d",&a);
	printf("输入模数n：");
	scanf("%d",&n);
	}
	printf("计算得逆元b=%d",GetInverse(a,n));
	
}
