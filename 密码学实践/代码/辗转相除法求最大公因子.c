#include <stdio.h>
int TwoNumber(int m,int n){
	int x=m,y=n;
	int r;
	do{
		r=x%y;
		x=y;
		y=r;
	}while(y!=0);
	return x;                                  
}
main()
{
	int a,b,c,d,e;
	printf("输入两个正整数：");
	scanf("%d %d",&a,&b) ;
	int x;
	x=TwoNumber(a,b);
	printf("这两个正整数的最大公因子为：%d\n",x);
	printf("输入三个正整数：");
	scanf("%d %d %d",&c,&d,&e); 
	int y,z;
	y=TwoNumber(c,d);
	z=TwoNumber(y,e);
	printf("这三个正整数的最大公因子为：%d",z);
 } 
