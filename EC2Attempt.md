# CrackingHashes

This project demonstrates parallel dictionary searching using Python multiprocessing.
The program was deployed and executed on a free-tier AWS EC2 instance.
This is the first attempt with a free tier EC2 instance, however it took too long because many processes were competing for a small pool of CPU space.

---

## EC2 Instance Configuration

- **OS:** Amazon Linux  
- **Instance type:** t3.micro (Free Tier eligible)  
- **Key pair:** RSA (.pem file)  
- **Network settings:**  
  - Allow SSH  
  - Source: My IP  
  - Port: 22  
- **Storage:** Default root volume  

---

## Bash Setup and Execution Commands

```bash
# Set correct permissions on the SSH key
chmod 400 ec2-module4-key.pem

# Connect to the EC2 instance
ssh -i ec2-module4-key.pem ec2-user@3.141.7.247

# Update system packages
sudo dnf update -y

# Install Python and pip
sudo dnf install python3 python3-pip -y

# Install required Python libraries
pip install nltk
python3
import nltk
nltk.download('words')
import bcrypt
exit()

# Exit EC2 to return to local machine
exit

# Copy program files and input data to EC2
scp -i ec2-module4-key.pem Task2.py shadow.txt result.txt ec2-user@3.141.7.247:~

# Reconnect to EC2
ssh -i ec2-module4-key.pem ec2-user@3.141.7.247

# Run the program in the background so it continues after disconnect
nohup python3 Task2.py > run.log 2>&1 &

# Verify that the program is running
ps aux | grep Task2.py

# Exit the SSH session safely
exit

# Copy result file back to local machine
scp -i ec2-module4-key.pem ec2-user@3.141.7.247:~/result.txt .
```
