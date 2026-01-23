#include <winsock2.h>
#include <windows.h>
#include <ws2tcpip.h>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>

#pragma comment(lib, "ws2_32.lib")

#define ICMP_ECHO 8
#define ICMP_ECHOREPLY 0
#define ICMP_MIN 8 // minimum 8 byte icmp packet (just header)
#define STATUS_FAILED 0xFFFF
#define DEF_PACKET_SIZE 32
#define DEF_PACKET_NUMBER 4
#define MAX_PACKET 1024

// IP header structure
typedef struct iphdr {
    unsigned int h_len : 5;       // header length
    unsigned int version : 4;     // IP version
    unsigned char tos;            // type of service
    unsigned short total_len;     // total length
    unsigned short ident;         // identification
    unsigned short frag_and_flags;// fragmentation flags
    unsigned char ttl;            // time to live
    unsigned char proto;          // protocol
    unsigned short checksum;      // checksum
    unsigned int sourceIP;
    unsigned int destIP;
} IpHeader;

// ICMP header structure
typedef struct icmphdr {
    BYTE i_type;
    BYTE i_code;
    USHORT i_cksum;
    USHORT i_id;
    USHORT i_seq;
    ULONG timestamp;
} IcmpHeader;

// Function prototypes
void fill_icmp_data(char*, int);
USHORT checksum(USHORT*, int);
int decode_resp(char*, int, sockaddr_in*);
void Usage(const char* progname);

int main(int argc, char** argv) {
    WSADATA wsaData;
    SOCKET sockRaw;
    sockaddr_in dest, from;
    int fromlen = sizeof(from);
    char* dest_ip;
    char* icmp_data = nullptr;
    char* recvbuf = nullptr;
    USHORT seq_no = 0;
    int statistic = 0;

    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "WSAStartup failed: " << WSAGetLastError() << std::endl;
        return STATUS_FAILED;
    }

    if (argc < 2) {
        Usage(argv[0]);
    }

    // Create raw socket
    sockRaw = WSASocket(AF_INET, SOCK_RAW, IPPROTO_ICMP, NULL, 0, 0);
    if (sockRaw == INVALID_SOCKET) {
        std::cerr << "WSASocket() failed: " << WSAGetLastError() << std::endl;
        WSACleanup();
        return STATUS_FAILED;
    }

    // Set timeout
    int timeout = 1000;
    setsockopt(sockRaw, SOL_SOCKET, SO_RCVTIMEO, (char*)&timeout, sizeof(timeout));

    // Resolve destination address
    memset(&dest, 0, sizeof(dest));
    dest.sin_family = AF_INET;

    unsigned long addr = inet_addr(argv[1]);
    if (addr == INADDR_NONE) {
        // If not a valid IP address, try to resolve as hostname
        hostent* hp = gethostbyname(argv[1]);
        if (hp) {
            memcpy(&(dest.sin_addr), hp->h_addr, hp->h_length);
        } else {
            std::cerr << "Unable to resolve " << argv[1] << std::endl;
            closesocket(sockRaw);
            WSACleanup();
            return STATUS_FAILED;
        }
    } else {
        dest.sin_addr.s_addr = addr;
    }

    dest_ip = inet_ntoa(dest.sin_addr);

    // Set packet count and size
    int times = (argc > 2) ? atoi(argv[2]) : DEF_PACKET_NUMBER;
    if (times <= 0) times = DEF_PACKET_NUMBER;

    int datasize = (argc > 3) ? atoi(argv[3]) : DEF_PACKET_SIZE;
    if (datasize <= 0) datasize = DEF_PACKET_SIZE;
    if (datasize > MAX_PACKET) {
        std::cerr << "WARNING: data_size is too large! Using default." << std::endl;
        datasize = DEF_PACKET_SIZE;
    }

    std::cout << "The length of ICMP header is " << sizeof(IcmpHeader) << std::endl;

    // Allocate memory
    icmp_data = new char[sizeof(IcmpHeader) + MAX_PACKET];
    recvbuf = new char[sizeof(IcmpHeader) + MAX_PACKET + 20];
    memset(icmp_data, 0, sizeof(IcmpHeader) + MAX_PACKET);
    memset(recvbuf, 0, sizeof(IcmpHeader) + MAX_PACKET + 20);

    fill_icmp_data(icmp_data, datasize);
    datasize += sizeof(IcmpHeader);

    std::cout << "\nPinging " << dest_ip << " with " << datasize << " bytes of data:\n" << std::endl;

    // Send and receive packets
    for (int i = 0; i < times; ++i) {
        ((IcmpHeader*)icmp_data)->i_cksum = 0;
        ((IcmpHeader*)icmp_data)->timestamp = GetTickCount();
        ((IcmpHeader*)icmp_data)->i_seq = seq_no++;
        ((IcmpHeader*)icmp_data)->i_cksum = checksum((USHORT*)icmp_data, datasize);

        // Send packet
        int bwrote = sendto(sockRaw, icmp_data, datasize, 0, (sockaddr*)&dest, sizeof(dest));
        if (bwrote == SOCKET_ERROR) {
            if (WSAGetLastError() == WSAETIMEDOUT) {
                std::cout << "Request timed out." << std::endl;
                continue;
            }
            std::cerr << "sendto failed: " << WSAGetLastError() << std::endl;
            break;
        }

        // Receive response
        int bread = recvfrom(sockRaw, recvbuf, MAX_PACKET + sizeof(IcmpHeader) + 20, 0, (sockaddr*)&from, &fromlen);
        if (bread == SOCKET_ERROR) {
            if (WSAGetLastError() == WSAETIMEDOUT) {
                std::cout << "Request timed out." << std::endl;
            } else {
                std::cerr << "recvfrom failed: " << WSAGetLastError() << std::endl;
            }
        } else {
            if (!decode_resp(recvbuf, bread, &from)) {
                statistic++;
            }
        }

        Sleep(1000);
    }

    // Print statistics
    std::cout << "\nPing statistics for " << dest_ip << ":" << std::endl;
    std::cout << "    Packets: Sent = " << times << ", Received = " << statistic 
              << ", Lost = " << (times - statistic) << " (" 
              << (float)(times - statistic) / times * 100 << "% loss)" << std::endl;

    // Cleanup
    delete[] icmp_data;
    delete[] recvbuf;
    closesocket(sockRaw);
    WSACleanup();

    return 0;
}

void Usage(const char* progname) {
    std::cerr << "Usage:" << std::endl;
    std::cerr << progname << " <host> [packet_count] [data_size]" << std::endl;
    std::cerr << "data_size can be up to 1KB" << std::endl;
    ExitProcess(STATUS_FAILED);
}

int decode_resp(char* buf, int bytes, sockaddr_in* from) {
    IpHeader* iphdr = (IpHeader*)buf;
    unsigned short iphdrlen = iphdr->h_len * 4;

    if (bytes < iphdrlen + ICMP_MIN) {
        std::cout << "Too few bytes from " << inet_ntoa(from->sin_addr) << std::endl;
        return 1;
    }

    IcmpHeader* icmphdr = (IcmpHeader*)(buf + iphdrlen);
    if (icmphdr->i_type != ICMP_ECHOREPLY) {
        std::cerr << "non-echo type " << icmphdr->i_type << " received" << std::endl;
        return 1;
    }

    if (icmphdr->i_id != (USHORT)GetCurrentProcessId()) {
        std::cerr << "someone else's packet!" << std::endl;
        return 1;
    }

    std::cout << bytes << " bytes from " << inet_ntoa(from->sin_addr) << ":";
    std::cout << " icmp_seq = " << icmphdr->i_seq;
    std::cout << " time: " << GetTickCount() - icmphdr->timestamp << " ms";
    std::cout << std::endl;

    return 0;
}

USHORT checksum(USHORT* buffer, int size) {
    unsigned long cksum = 0;

    while (size > 1) {
        cksum += *buffer++;
        size -= sizeof(USHORT);
    }

    if (size) {
        cksum += *(UCHAR*)buffer;
    }

    cksum = (cksum >> 16) + (cksum & 0xffff);
    cksum += (cksum >> 16);
    return (USHORT)(~cksum);
}

void fill_icmp_data(char* icmp_data, int datasize) {
    IcmpHeader* icmp_hdr = (IcmpHeader*)icmp_data;
    icmp_hdr->i_type = ICMP_ECHO;
    icmp_hdr->i_code = 0;
    icmp_hdr->i_id = (USHORT)GetCurrentProcessId();
    icmp_hdr->i_cksum = 0;
    icmp_hdr->i_seq = 0;

    char* datapart = icmp_data + sizeof(IcmpHeader);
    memset(datapart, 'E', datasize);
}
