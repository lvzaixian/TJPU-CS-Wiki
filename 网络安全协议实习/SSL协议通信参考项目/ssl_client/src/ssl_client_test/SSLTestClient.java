package ssl_client_test;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.security.KeyStore;

import javax.net.ssl.KeyManagerFactory;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLHandshakeException;
import javax.net.ssl.SSLServerSocket;
import javax.net.ssl.SSLSocket;
import javax.net.ssl.TrustManagerFactory;

import ssl_client.CertHelper;

public class SSLTestClient {
	
	
	private static final String CLIENT_KEYSTORE = "client_ks.jks";
	//private static final String CLIENT_KEYSTORE = "F:/ejbca/p12/tmp/ejbcakclient.jks";
	
	//D:/software/lala/ejbcakclient.jks
	
	
	private static final String CLIENT_KEYSTORE_PWD = "123456";

	
	
	
	public static void main(String[] args) throws Exception {
		 //获取SSLContext
		SSLContext ctx = SSLContext.getInstance("SSL");
		 //生成秘钥的manager
		KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
		//加载信任的证书
		TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
		
		//加载秘钥
		KeyStore ks = KeyStore.getInstance("JKS");
		KeyStore tks = KeyStore.getInstance("JKS");
		ks.load(new FileInputStream(CLIENT_KEYSTORE),
				CLIENT_KEYSTORE_PWD.toCharArray());
		tks.load(new FileInputStream(CLIENT_KEYSTORE),
				CLIENT_KEYSTORE_PWD.toCharArray());

		 //秘钥初始化
		kmf.init(ks, "123456".toCharArray());
		tmf.init(tks);
		 //初始化SSLContext
		ctx.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);
		
		
		//获取SSLContext的SocketFactory
		SSLSocket sslSocket = (SSLSocket) ctx.getSocketFactory().createSocket(
				"localhost", 7071);
		
		try {
			sslSocket.startHandshake();
		} catch (SSLHandshakeException e) {
			System.out.println("客户端未能安装服务器证书，自动安装服务器证书...");
			boolean result = CertHelper.intallCert(CLIENT_KEYSTORE,
					CLIENT_KEYSTORE_PWD, "localhost", 7071);
			if (result) {
				System.out.println("重新运行即可建立安全连接.");
			} else {
				System.out.println("安装证书失败.");
			}
			System.exit(0);
		} catch (Exception e) {
			System.out.println(e);
			System.exit(0);
		}
	
	
	
		InputStream input = sslSocket.getInputStream();
		OutputStream utput = sslSocket.getOutputStream();

		BufferedInputStream bis = new BufferedInputStream(input);
		BufferedOutputStream bos = new BufferedOutputStream(utput);

		bos.write("Hello,I am client".getBytes());
		bos.flush();

		byte[] buffer = new byte[20];
		int length = bis.read(buffer);
		System.out.println(new String(buffer, 0, length));

		sslSocket.close();
	}

}