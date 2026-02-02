from nltk.corpus import words
import nltk
import os
import time
import bcrypt
import multiprocessing

# fiter dictionary for 6-10 letter words
def get_words():
    all_words = words.words()
    filtered = []
    for w in all_words:
        if 6 <= len(w) and len(w) <= 10:
            filtered.append(w)
    return filtered

# split dictionary into chunks
def chunkify(words_list, n_chunks):
    if n_chunks <= 0:
        raise ValueError("n_chunks must be >= 1")
    
    n = len(words_list)
    if n_chunks > n:
        if n > 0:
            n_chunks = n
        else:
            n_chunks = 1

    chunk_size = (n + n_chunks - 1) // n_chunks

    result_chunks = []
    left = 0
    while left < n:
        right = left + chunk_size
        result_chunks.append(words_list[left:right])
        left = right
        
    return result_chunks

def parse_userSaltHash(userSaltHash):
    userSaltHashBytes = userSaltHash.encode('utf-8')
    password_list = userSaltHash.split('$')
    algo = password_list[1]
    workfactor = int(password_list[2])
    salt = password_list[3][:22]
    hash = password_list[3][22:]

    return algo, workfactor, salt, hash, userSaltHashBytes


# get user, algo, wf, salt, hash, and salt+hash in bytes from line
def parse_line(line):
    temp_list = line.split(':')
    user = temp_list[0]
    userSaltHash = temp_list[1]
    # remove newlines so it doesn't mess with the hash
    if userSaltHash[-1] == '\n':
        userSaltHash = userSaltHash[:-1]
    return user, userSaltHash

def parse_file(infile, chunks):
    all_args = []
    for line in infile:
        user, userSaltHash = parse_line(line)
        # group args by user
        arg = []
        for chunk in chunks:
            arg.append((chunk, user, userSaltHash))
        all_args.append(arg)
    return all_args

# bcrypt each word in chunk and check if it equals the user's salt and hash
# imap_unordered takes in a list of args so each arg has to be an iterable
''' # example of arg
arg = (
    [chunk1],
    Bilbo,
    $2b$08$J9FW66ZdPI2nrIMcOxFYI.qx268uZn.ajhymLP/YHaAsfBGP3Fnmq
)
'''
def crack_hash(arg):
    chunk, _, userSaltHash = arg
    for guess in chunk:
        guessBytes = guess.encode('utf-8')
        userSaltHashBytes = userSaltHash.encode('utf-8')
        result = bcrypt.checkpw(guessBytes, userSaltHashBytes)
        if result:
            return guess
    # if password not found
    return None 

def thread_cracking(all_args, n_workers, outfile):
    if n_workers is None:
        n_workers = os.cpu_count() or 4

    '''
    all_args = [
        [ # user_args 1
            (
                [chunk1],
                Bilbo,
                $2b$08$J9FW66ZdPI2nrIMcOxFYI.qx268uZn.ajhymLP/YHaAsfBGP3Fnmq
            ),
            (
                [chunk2],
                Bilbo,
                $2b$08$J9FW66ZdPI2nrIMcOxFYI.qx268uZn.ajhymLP/YHaAsfBGP3Fnmq
            ), ...
        ],
        [ # user_args 2
            (
                [chunk1],
                Gandalf,
                $2b$08$J9FW66ZdPI2nrIMcOxFYI.q2PW6mqALUl2/uFvV9OFNPmHGNPa6YC
            ), ...
        ]
    ]
    '''
    for user_args in all_args:
        start = time.time()
        found = None
        with multiprocessing.Pool(processes=n_workers) as pool:
            # imap_unordered takes in a list of args which are tuples
            for result in pool.imap_unordered(crack_hash, user_args):
                if result is not None:
                    found = result
                    pool.terminate()
                    pool.join()
                    break
            elapsed = time.time() - start

            # unpack
            _, user, userSaltHash = user_args[0]

            algo, workfactor, salt, hash, _ = parse_userSaltHash(userSaltHash)

            # write to outfile
            outfile.write('User: ' + user + '\n')
            outfile.write('Algo: ' + algo + '\n')
            outfile.write('Workfactor: ' + str(workfactor) + '\n')
            outfile.write('Salt: ' + salt + '\n')
            outfile.write('Hash: ' + hash + '\n')
            if found is not None:
                outfile.write('Password: ' + found + '\n')
            else:
                outfile.write('Password not found')
            outfile.write('Time taken: ' + str(elapsed) + ' s\n\n')

def main():
    n = 12
    filtered_words = get_words()
    result_chunks = chunkify(filtered_words, n)
    with open("shadow.txt", "r") as infile, open("result.txt", "w") as outfile:
        all_args = parse_file(infile, result_chunks)
        thread_cracking(all_args, n, outfile)

    

if __name__ == "__main__":
    main()