start_list= []
commit_list= []
transactions= {}
Checkpoint= []
Wallet= {}

def undo():
    undo_list= [i for i in start_list if i not in commit_list]
    for transaction_id in list(transactions.keys()):
        if transaction_id in undo_list:
            Wallet[transactions[transaction_id]['wallet']]= transactions[transaction_id]['before']
            del transactions[transaction_id]
    for i in start_list[:]:
        if i in undo_list:
            start_list.remove(i)
    print("Undo:", undo_list)

def redo():
    print("Redo:", start_list)
    for transaction_id in list(transactions.keys()):
        if transaction_id in start_list:
            Wallet[transactions[transaction_id]['wallet']]= transactions[transaction_id]['after']

def check():
    index= start_list.index(Checkpoint[0])
    for i in range(index):
        del start_list[i]
    for key in list(transactions.keys()):
        if key not in start_list:
            del transactions[key]
    index= commit_list.index(Checkpoint[0])
    for i in range(index):
        del commit_list[i]
    undo()
    redo()
    print(Wallet)


### Main function 
with open("input.txt", "r") as file: 
    for line in file: 
        if "START" in line:
            transaction_id= line.replace('<START ', '').replace('>\n', '')
            start_list.append(transaction_id)
        elif "COMMIT" in line:
            transaction_id= line.replace('<COMMIT ', '').replace('>\n', '')
            commit_list.append(transaction_id)
        elif "CKPT" in line:
            if "END" in line:
                check()
                start_list.clear()
                commit_list.clear()
                transactions.clear()
                Wallet.clear()
                Checkpoint.clear()
            else:
                clean_line= line.replace("<CKPT(", "").replace(")>\n", "")
                transaction_id= (clean_line.split(','))
                Checkpoint= [i for i in transaction_id]  
        else:
            clean_transaction= line.replace('<', '').replace('>\n', '').split()
            # print(clean_transaction)
            transaction_id= clean_transaction[0]
            wallet= clean_transaction[1]
            before= int(clean_transaction[2])
            after= int(clean_transaction[3])
            transactions[transaction_id]= {'wallet': wallet, 'before': before, 'after': after}