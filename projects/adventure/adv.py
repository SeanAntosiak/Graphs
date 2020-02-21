from room import Room
from player import Player
from world import World
from queue import SimpleQueue as Q
import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
#world.print_rooms()


# defines a function to add next rooms
def add_next_rooms(player, player_graph):
    current = player.current_room.id
    player_graph[current] = {}
    for next in player.current_room.get_exits():
        player_graph[current][next] = '?'


# creates a function to inverse direction
def inv_dir(dir):
    if dir == 'n':
        return('s')
    if dir == 'e':
        return('w')
    if dir == 's':
        return('n')
    if dir == 'w':
        return('e')


# creates a function to find a room from another that you have already been to
def find_room(player_graph, start, end):
    q = Q()
    q.put([start])
    visited = set()
    while q.qsize() > 0:
        path = q.get()
        last_room = path[-1]
        if last_room == end:
            return(path)
        if last_room not in visited:
            visited.add(last_room)
            for next in player_graph[last_room]:
                if player_graph[last_room][next] != '?':
                    new_path = path.copy()
                    new_path.append(player_graph[last_room][next])
                    q.put(new_path)


# gets directions to follow a path
def get_directions(player_graph, path):
    directions = []
    for i in range(len(path)-1):
        dirs = player_graph[path[i]]
        for dir in dirs:
            if player_graph[path[i]][dir] == path[i+1]:
                directions.append(dir)
    return(directions)


# sets up blank path graph and player
player = Player(world.starting_room)
player_graph = {}
traversal_path = []

# adds start room to graph
add_next_rooms(player, player_graph)

while len(player_graph) < 500:
    current_room = player.current_room.id
    possible_next = player_graph[current_room]

    # starts looking for a '?'
    searching = 1
    next_direction = None
    while searching == 1:
        for next in possible_next:
            if possible_next[next] == '?':
                next_direction = next
                searching = 0
                break

        if searching != 0:
            searching = 2

    # look for a room that has a ? if none were found in current room
    if searching == 2:
        # finds the room and sets it to go_to
        go_to = 0
        for room in player_graph:
            for dir in player_graph[room]:
                if player_graph[room][dir] == '?':
                    go_to = room
                    break

        # finds a path to the room
        path = find_room(player_graph, current_room, go_to)

        # finds the directions to follow that path
        dirs = get_directions(player_graph, path)


        # moves the player to the room with a new path
        for dir in dirs:
            player.travel(dir)

        # updates the traversal with the path
        traversal_path += dirs


    else:
        # updates traversal path
        traversal_path.append(next_direction)

        # sets last room to use to update the next room
        last_room = current_room

        # travels the player and updates the current room
        player.travel(next_direction)
        current_room = player.current_room.id

        # adds next rooms exits to the graph
        if current_room not in player_graph:
            add_next_rooms(player, player_graph)

        # updates directions from past and current room
        player_graph[last_room][next_direction] = current_room
        player_graph[current_room][inv_dir(next_direction)] = last_room

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
