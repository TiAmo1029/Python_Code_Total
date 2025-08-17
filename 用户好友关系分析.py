friend_a = {"Tom","tony","mary"}
friend_b = {"Peter","Java","tony"}
common_friend = friend_a & friend_b
all_friends = friend_a.union(friend_b)
print("他们的共同好友是"+ str(common_friend)+ ",他们的全部好友是" + str(all_friends))
exclusive_friend = friend_a ^ friend_b
print(exclusive_friend)
