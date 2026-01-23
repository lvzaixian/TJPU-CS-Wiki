package ssl_server_test;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.security.KeyStore;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;

import javax.net.ssl.KeyManagerFactory;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLServerSocket;
import javax.net.ssl.TrustManager;
import javax.net.ssl.TrustManagerFactory;
import javax.net.ssl.X509TrustManager;

public class SSLTestServer {
	
	
	
	private static final String SERVER_KEYSTORE = "D:/software/lala/ejbcakclient.jks";
//	private static final String SERVER_KEYSTORE = "F:/ejbca/p12/tmp/ejbcakserver.jks";
	private static final String SERVER_KEYSTORE_PWD = "123456";

	public static void main(String[] args) throws Exception {
		SSLContext ctx = SSLContext.getInstance("SSL");
		//获取SSLContext
		KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");  //生成秘钥的manager
		//加载信任的证书
		TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
		//加载秘钥
		KeyStore ks = KeyStore.getInstance("JKS");
		KeyStore tks = KeyStore.getInstance("JKS");

		ks.load(new FileInputStream(SERVER_KEYSTORE),
				SERVER_KEYSTORE_PWD.toCharArray());
		tks.load(new FileInputStream(SERVER_KEYSTORE),
				SERVER_KEYSTORE_PWD.toCharArray());
		//秘钥初始化
		kmf.init(ks, SERVER_KEYSTORE_PWD.toCharArray());
		tmf.init(tks); 
        //初始化SSLContext
		ctx.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);
		  //获取SSLContext的SocketFactory
		SSLServerSocket serverSocket = (SSLServerSocket) ctx
				.getServerSocketFactory().createServerSocket(7071);
		
		 //是否开启双向验证
		serverSocket.setNeedClientAuth(true);
		
		while (true) {
			try {
				Socket s = serverSocket.accept();
				InputStream input = s.getInputStream();
				OutputStream utput = s.getOutputStream();

				BufferedInputStream bis = new BufferedInputStream(input);
				BufferedOutputStream bos = new BufferedOutputStream(utput);

				byte[] buffer = new byte[20];
				int length = bis.read(buffer);
				
				System.out.println("Receive: "
						+ new String(buffer, 0, length).toString());
				
				

				bos.write("Hello,I am server".getBytes());
				bos.flush();

				s.close();
			} catch (Exception e) {
				e.printStackTrace();
				// System.out.println(e);
			}
		}
	}

	private static class SavingTrustManager implements X509TrustManager {
		private final X509TrustManager tm;
		private X509Certificate[] chain;

		SavingTrustManager(X509TrustManager tm) {
			this.tm = tm;
		}

		public X509Certificate[] getAcceptedIssuers() {
			X509Certificate[] certs=tm.getAcceptedIssuers();
			return certs;
//			 throw new UnsupportedOperationException();
		}

		public void checkClientTrusted(X509Certificate[] chain, String authType)
				throws CertificateException {
			this.chain = chain;
			tm.checkClientTrusted(chain, authType);
		}

		public void checkServerTrusted(X509Certificate[] chain, String authType)
				throws CertificateException {
			this.chain = chain;
			tm.checkServerTrusted(chain, authType);
		}
	}
}