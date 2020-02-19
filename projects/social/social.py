import random
from util import Queue

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        if num_users < avg_friendships:
            print('The number of users must be greater than the average number of friendships.')
            return

        for _ in range(num_users):
            self.add_user(self.random_name())

        # gets all user combinations where user 1 has lower id than user 2
        combos = []
        user_ids = []
        for i in range(1, num_users+1):
            user_ids.append(i)

        for user1 in user_ids:
            for user2 in user_ids[user1 + 1:]:
                combos.append((user1, user2))

        # gets the number of needed connections and makes that many
        needed = num_users*avg_friendships
        connections = random.sample(combos, needed // 2)
        for con in connections:
            self.add_friendship(con[0], con[1])


    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        Q = Queue()
        Q.enqueue([user_id])
        visited = {}

        while Q.size() > 0:
            path = Q.dequeue()
            last_friend = path[-1]

            if last_friend not in visited:
                visited[last_friend] = path

                for friend in self.friendships[last_friend]:
                    # (Make a copy of the path before adding)
                    new_path = path.copy()
                    new_path.append(friend)
                    Q.enqueue(new_path)
        return visited

    def random_name(self):
        # sets the letters to generate the random name from
        letters = 'wretyuioasdhjklzcvbm'

        # randomly decides the length of the name
        length = random.choice(range(4, 8))

        # creates the name
        name = ''
        for _ in range(length):
            name += random.choice(letters)
        return(name)


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
