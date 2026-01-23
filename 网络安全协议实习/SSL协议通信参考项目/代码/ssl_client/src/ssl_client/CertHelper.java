package ssl_client;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.nio.charset.CharsetEncoder;
import java.nio.charset.spi.CharsetProvider;
import java.security.KeyStore;
import java.security.MessageDigest;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;

import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLException;
import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;
import javax.net.ssl.TrustManager;
import javax.net.ssl.TrustManagerFactory;
import javax.net.ssl.X509TrustManager;

public class CertHelper {
	public static boolean intallCert(String trustKeyStoreFilePath,
			String trustKeyStorePassword, String targetHost, int targetPort)
			throws Exception {
		char[] passphrase = trustKeyStorePassword.toCharArray();

		File file = new File(trustKeyStoreFilePath);
		if (!file.isFile()) {
			char SEP = File.separatorChar;
			File dir = new File(System.getProperty("java.home") + SEP + "lib"
					+ SEP + "security");
			file = new File(dir, "jssecacerts");
			if (file.isFile() == false) {
				file = new File(dir, "cacerts");
			}
		}
		System.out.println("加载证书库[" + file + "]...");
		InputStream in = new FileInputStream(file);
		KeyStore ks = KeyStore.getInstance(KeyStore.getDefaultType());
		ks.load(in, passphrase);
		in.close();

		SSLContext context = SSLContext.getInstance("TLS");
		TrustManagerFactory tmf = TrustManagerFactory
				.getInstance(TrustManagerFactory.getDefaultAlgorithm());
		tmf.init(ks);
		X509TrustManager defaultTrustManager = (X509TrustManager) tmf
				.getTrustManagers()[0];
		SavingTrustManager tm = new SavingTrustManager(defaultTrustManager);
		context.init(null, new TrustManager[] { tm }, null);
		SSLSocketFactory factory = context.getSocketFactory();

		System.out.println("连接" + targetHost + ":" + targetPort + "...");
		SSLSocket socket = (SSLSocket) factory.createSocket(targetHost,
				targetPort);
		socket.setSoTimeout(10000);
		try {

			socket.startHandshake();
			socket.close();
			// System.out.println("存在可信证书，handshake通信成功.");
			// return true;
		} catch (Exception e) {
			System.out.println("handshake通信失败...");
			System.out.println(e);
		}
		X509Certificate[] chain = tm.chain;
		if (chain == null) {
			System.out.println("不包含服务器证书链，安装失败.");
			return false;
		}
		System.out.println();
		System.out.println(String.format("收到服务器发送的%d个证书.", chain.length));
		System.out.println();
		for (int i = 1; i <= chain.length; i++) {
			System.out.println("安装第" + i + "个数字证书...");
			X509Certificate cert = chain[i - 1];
			String alias = targetHost + "-" + (i);
			ks.setCertificateEntry(alias, cert);
			OutputStream out = new FileOutputStream(trustKeyStoreFilePath);
			ks.store(out, passphrase);
			out.close();
			System.out.println(String.format("成功安装证书[%s]至证书库[%s]", alias,
					trustKeyStoreFilePath));
		}
		return true;
	}

	private static final char[] HEXDIGITS = "0123456789abcdef".toCharArray();

	private static String toHexString(byte[] bytes) {
		StringBuilder sb = new StringBuilder(bytes.length * 3);
		for (int b : bytes) {
			b &= 0xff;
			sb.append(HEXDIGITS[b >> 4]);
			sb.append(HEXDIGITS[b & 15]);
			sb.append(' ');
		}
		return sb.toString();
	}

	private static class SavingTrustManager implements X509TrustManager {
		private final X509TrustManager tm;
		private X509Certificate[] chain;

		SavingTrustManager(X509TrustManager tm) {
			this.tm = tm;
		}

		public X509Certificate[] getAcceptedIssuers() {
			return tm.getAcceptedIssuers();
			// throw new UnsupportedOperationException();
		}

		public void checkClientTrusted(X509Certificate[] chain, String authType)
				throws CertificateException {

			// throw new UnsupportedOperationException();
		}

		public void checkServerTrusted(X509Certificate[] chain, String authType)
				throws CertificateException {
			this.chain = chain;
			tm.checkServerTrusted(chain, authType);
		}
	}
}