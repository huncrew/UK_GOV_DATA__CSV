import sqlite3

conn = sqlite3.connect('uk-energy.sqlite')
cur = conn.cursor()

def retrieve_data():
    amount_list = []
    cur.execute('SELECT amount_id, title_id, quarter_id, amount FROM Amount')
    for row in cur:
        amount_list.append(row)
        print(row)
    
    return amount_list

def sum_amounts(retrieved_data_list):
    title_id = 1
    count = 0
    for row_data in retrieved_data_list:
        if title_id == row_data[1]:
            print(f'This should print {count} times')
            count += 1;
    print(count)


def main():
    retrieved_data_list = retrieve_data()
    sum_amounts(retrieved_data_list)

if __name__ == "__main__":
    main()


# cur.execute('SELECT id, guid,sender_id,subject_id,sent_at FROM Messages')
# messages = dict()
# for message_row in cur :
#     messages[message_row[0]] = (message_row[1],message_row[2],message_row[3],message_row[4])


# sendorgs = dict()
# for (message_id, message) in list(messages.items()):
#     sender = message[1]
#     pieces = senders[sender].split("@")
#     if len(pieces) != 2 : continue
#     dns = pieces[1]
#     sendorgs[dns] = sendorgs.get(dns,0) + 1

# # pick the top schools
# orgs = sorted(sendorgs, key=sendorgs.get, reverse=True)
# orgs = orgs[:10]
# print("Top 10 Organizations")
# print(orgs)

# counts = dict()
# months = list()
# # cur.execute('SELECT id, guid,sender_id,subject_id,sent_at FROM Messages')
# for (message_id, message) in list(messages.items()):
#     sender = message[1]
#     pieces = senders[sender].split("@")
#     if len(pieces) != 2 : continue
#     dns = pieces[1]
#     if dns not in orgs : continue
#     month = message[3][:4]
#     print(message)
#     if month not in months : months.append(month)
#     key = (month, dns)
#     counts[key] = counts.get(key,0) + 1


# months.sort()
# # print counts
# # print months

# fhand = open('gline.js','w')
# fhand.write("gline = [ ['Month'")
# for org in orgs:
#     fhand.write(",'"+org+"'")
# fhand.write("]")

# for month in months:
#     fhand.write(",\n['"+month+"'")
#     for org in orgs:
#         key = (month, org)
#         val = counts.get(key,0)
#         fhand.write(","+str(val))
#     fhand.write("]");

# fhand.write("\n];\n")
# fhand.close()

# print("Output written to gline.js")
# print("Open gline.htm to visualize the data")
