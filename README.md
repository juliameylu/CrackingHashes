# CrackingHashes

For Task 2, given your results, how long would it take to brute force a 
password that uses the format word1:word2 where both words are between 6 
and 10 characters? What about word1:word2:word3? What about 
word1:word2:number where number is between 1 and 5 digits? Make sure to 
sufficiently justify your answers.

If a password took time t seconds to brute force, it would take around t^2 seconds for a password in the format word1:word2. The runtime grows quadratically because the number of possible combinations is squared. Similarly, it would take around t^3 seconds for a password in the format word1:word2:word3 because the number of possible combinations is cubed. It would take around 111,110 * t^2 seconds to brute force a password in the format word1:word2:number where the number is between 1 and 5 digits (including leading zeros) because the number of numeric possibilities is 10 + 100 + 1,000 + 10,000 + 100,000 = 111,110.

Please address the following in your report:
1. What you did and what you observed
For Task 2, I pasted the contents of the shadow.pdf file into a txt file and then parsed it for each user's salt and hash. I then filtered and split the dictionary into chunks for each thread to process to shorten compute time. 

At first, I tried to run the program on an EC2 instance, so that if I stepped away from the computer, the program wouldn't be interupted. However, I discovered that running on the EC2 instance was taking a lot longer because the free tier only provides 1-2 vCPUs which have lower clock speed than my Mac's CPU. I ended up running the program locally on my laptop but included the EC2 setup and commands for future reference. 

4. Please include any explanations of the surprising or interesting observations you made
I observed a clear trend between higher work factors and higher runtime, which matches bcrypt's design. However, it wasn't perfectly consistent. For example, Dwalin's 10 work factor password took around 71 seconds to crack while Bilbo's 8 work factor password took around 190 seconds to crack. This suggests that total time isn't purely based on hash cost, but was also caused by other factors like system noise (I was using my laptop for other tasks) and where the password appears in search order. Dwalin's password was "drossy" which appears in the dictionary before Bilbo's password "welcome."


