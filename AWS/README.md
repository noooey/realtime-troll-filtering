# AWS

## 💻 EC2 INSTANCE
**REGION**: 아시아 태평양 (서울) ap-northeast-2   
**AMI**: Ubuntu Server 20.04 LTS (HVM), SSD Volume Type   
**INSTANCE TYPE**: m5.2xlarge (패밀리: m5 / 8 vCPU 32 / GiB 메모리)   
**STORAGE**: 100GIB (gp3)

## 🕸️ Elastic IP
탄력적 IP를 사용하여 인스턴스가 종료되더라도 IP가 바뀌지 않게 함   
Elastic IP: *15.164.148.99*

## 🔌 Instance Connection
ANTI-TROLL.pem 400(나만 읽기) 권한 부여 후   
ssh로 인스턴스 원격 접속

```bash
$ chmod 400 ANTI-TROLL.pem
$ ssh -i "ANTI-TROLL.pem" ubuntu@ec2-15-164-148-99.ap-northeast-2.compute.amazonaws.com
```

## 🔧 Configuration
- Install Docker
