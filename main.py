# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
		print("INFO")

		return {
				"apiversion": "1",
				"author": "team14",  # TODO: Your Battlesnake Username
				"color": "#888888",  # TODO: Choose color
				"head": "default",  # TODO: Choose head
				"tail": "default",  # TODO: Choose tail
		}


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
		print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
		print("GAME OVER\n")

#Distance between two points
def distance_btwn(p, q):
	return abs(p[0] - q[0]) + abs(p[1] - q[1])


def find_closest_food(my_head, food_list):
	closest_food = None
	min_distance = float('inf')  # Initialize with a very large value
	
	for food in food_list:
			food_pos = (food['x'], food['y'])
			head_pos = (my_head['x'], my_head['y'])
			distance = distance_btwn(head_pos, food_pos)
	
			if distance < min_distance:
                    #Sets minimum distance and the position of the closest-food
					min_distance = distance
					closest_food = food_pos
	
	return closest_food
	

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]: 
            is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:
            is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:
            is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:
            is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head["x"] == board_width - 1:
            is_move_safe["right"] = False
    elif my_head["x"] == 0:
            is_move_safe["left"] = False
    if my_head["y"] == board_height - 1:
            is_move_safe["up"] = False
    elif my_head["y"] == 0:
            is_move_safe["down"] = False

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']

    for my_body_part in my_body:
            if(my_head["x"] == my_body_part["x"]-1 and my_head["y"] == my_body_part["y"]):
                    is_move_safe["right"] = False
            if(my_head["x"] == my_body_part["x"]+1 and my_head["y"] == my_body_part["y"]):
                    is_move_safe["left"] = False
            if(my_head["y"] == my_body_part["y"]-1 and my_head["x"] == my_body_part["x"]):
                    is_move_safe["up"] = False
            if(my_head["y"] == my_body_part["y"]+1 and my_head["x"] == my_body_part["x"]):
                    is_move_safe["down"] = False

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponent_snakes = game_state['board']['snakes']

    for snake in opponent_snakes:
            snake_body = snake["body"]
            for snake_body_part in snake_body:
                    if(my_head["x"] == snake_body_part["x"]-1 and my_head["y"] == snake_body_part["y"]):
                            is_move_safe["right"] = False
                    if(my_head["x"] == snake_body_part["x"]+1 and my_head["y"] == snake_body_part["y"]):
                            is_move_safe["left"] = False
                    if(my_head["y"] == snake_body_part["y"]-1 and my_head["x"] == snake_body_part["x"]):
                            is_move_safe["up"] = False
                    if(my_head["y"] == snake_body_part["y"]+1 and my_head["x"] == snake_body_part["x"]):
                            is_move_safe["down"] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
            if isSafe:
                    safe_moves.append(move)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']
    print(my_head, food)
    closest_food = find_closest_food(my_head, food)

    if closest_food is not None:
        direction_to_food = (closest_food[0] - my_head['x'], closest_food[1] - my_head['y'])
        #Statement checks which move is a valid move for the snake to make
        if direction_to_food[0] > 0 and 'right' in safe_moves:
                return {"move": "right"}
        elif direction_to_food[0] < 0 and 'left' in safe_moves:
                return {"move": "left"}
        elif direction_to_food[1] > 0 and 'up' in safe_moves:
                return {"move": "up"}
        elif direction_to_food[1] < 0 and 'down' in safe_moves:
                return {"move": "down"}


    # No valid food found or safe moves toward food, default to a safe move
    if len(safe_moves) > 0:
            # Choose the first safe move available
            return {"move": safe_moves[0]}
    else:
            # No safe moves left, default to moving down to avoid crashing
            print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
            return {"move": "down"}

# Start server when `python main.py` is run
if __name__ == "__main__":
		from server import run_server
		run_server({"info": info, "start": start, "move": move, "end": end})