import random
from typing import Optional, List, Dict

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import clamp


class MyBot(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None
        self.max_capacity = 5  # Kapasitas maksimal diamond

    def get_direction(self, current_x, current_y, dest_x, dest_y):
        if current_x == dest_x and current_y == dest_y:
            return random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        delta_x = clamp(dest_x - current_x, -1, 1)
        delta_y = clamp(dest_y - current_y, -1, 1)
        # Hindari gerakan diagonal: hanya satu arah
        if abs(delta_x) == abs(delta_y):
            if abs(dest_x - current_x) > abs(dest_y - current_y):
                delta_y = 0
            else:
                delta_x = 0
        return (delta_x, delta_y)

    def group_teleports(self, teleports: List[GameObject]) -> Dict[str, List[Position]]:
        pairs = {}
        for tp in teleports:
            pid = tp.properties.pair_id if tp.properties else None
            if pid:
                if pid not in pairs:
                    pairs[pid] = []
                pairs[pid].append(tp.position)
        return pairs

    def find_closest_diamond(self, bot_pos: Position, diamonds: List[GameObject]) -> Position:
        return min(
            diamonds,
            key=lambda d: abs(d.position.x - bot_pos.x) + abs(d.position.y - bot_pos.y)
        ).position

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position
        diamonds = board.diamonds

        # Jika kapasitas penuh, pulang ke base
        if props.diamonds >= self.max_capacity:
            if props.base and (props.base.x != current_position.x or props.base.y != current_position.y):
                self.goal_position = props.base
            else:
                for alt_dx, alt_dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    if board.is_valid_move(current_position, alt_dx, alt_dy):
                        return alt_dx, alt_dy
                return random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

        # Tidak ada diamond di papan
        if not diamonds:
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                if board.is_valid_move(current_position, dx, dy):
                    return dx, dy
            return random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

        # Diamond yang bisa diambil
        if props.diamonds == 4:
            possible_diamonds = [
                d for d in diamonds
                if d.properties
                and getattr(d.properties, "value", 1) == 1
                and (props.diamonds + getattr(d.properties, "value", 1)) <= self.max_capacity
            ]
        else:
            possible_diamonds = [
                d for d in diamonds
                if d.properties
                and (props.diamonds + getattr(d.properties, "value", 1)) <= self.max_capacity
            ]

        # Kalau tidak ada diamond yang sesuai kapasitas, pulang ke base
        if not possible_diamonds:
            if props.base and (props.base.x != current_position.x or props.base.y != current_position.y):
                self.goal_position = props.base
            else:
                for alt_dx, alt_dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    if board.is_valid_move(current_position, alt_dx, alt_dy):
                        return alt_dx, alt_dy
                return random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        else:
            nearest_diamond_pos = self.find_closest_diamond(current_position, possible_diamonds)

            # Gunakan teleport jika menguntungkan
            teleports = [g for g in board.game_objects if g.type == "TeleportGameObject"]
            tp_pairs = self.group_teleports(teleports)

            direct_distance = abs(nearest_diamond_pos.x - current_position.x) + abs(nearest_diamond_pos.y - current_position.y)
            best_path_len = direct_distance
            best_tp_entry = None

            for pair in tp_pairs.values():
                if len(pair) != 2:
                    continue
                a, b = pair
                for entry, exit in [(a, b), (b, a)]:
                    dist_to_entry = abs(current_position.x - entry.x) + abs(current_position.y - entry.y)
                    dist_from_exit = abs(exit.x - nearest_diamond_pos.x) + abs(exit.y - nearest_diamond_pos.y)
                    total_dist = dist_to_entry + dist_from_exit
                    if total_dist < best_path_len:
                        best_path_len = total_dist
                        best_tp_entry = entry

            self.goal_position = best_tp_entry if best_tp_entry else nearest_diamond_pos

        # Jika sudah di posisi tujuan, jangan diam
        if current_position.x == self.goal_position.x and current_position.y == self.goal_position.y:
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                if board.is_valid_move(current_position, dx, dy):
                    return dx, dy
            return random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

        # Bergerak menuju goal
        dx, dy = self.get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )

        if board.is_valid_move(current_position, dx, dy):
            return dx, dy
        else:
            for alt_dx, alt_dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if board.is_valid_move(current_position, alt_dx, alt_dy):
                    return alt_dx, alt_dy
            return random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
