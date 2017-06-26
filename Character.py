from enum import Enum
from FSM import *
from Game import *
import Queue
from Event import *


class Character_State_Enum(Enum):
    
    STAND = 0       # Done
    MOVE = 1        # Done
    MOVE_LEFT = 2   # Done
    MOVE_RIGHT = 3  # Done
    MOVE_UP = 4     # Done
    MOVE_DOWN = 5   # Done
    DEAD = 6            # Undo
    MOVE_TRANSITION = 7     # Done
    DIE_TRANSITION = 8      # Done


class Character_Move_Frame(Enum):
    
    TOTAL_FRAME_NUM = 16
    DIRECTION_FRAME_NUM = 4
    MOVE_DOWN_BEGIN = 0
    MOVE_DOWN_END = 3
    MOVE_LEFT_BEGIN = 4
    MOVE_LEFT_END = 7
    MOVE_RIGHT_BEGIN = 8
    MOVE_RIGHT_END = 11
    MOVE_UP_BEGIN = 12
    MOVE_UP_END = 15
    FRAME_INTERVAL = 200 # 80ms
    MOVE_STEP = 4
    MOVE_ACC_OFFSET = 36


# DEAD state
class Character_State_Dead(FSM_State):
    
    def __init__(self, fsm):
        super(Character_State_Dead, self).__init__(fsm)
        self.sn = Character_State_Enum.DEAD
    
    def enter(self):
        super(Character_State_Dead, self).enter()
        # print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Dead, self).update(et)
    
    def draw(self, et):
        super(Character_State_Dead, self).draw(et)

    def exit(self):
        super(Character_State_Dead, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)


# STAND state
class Character_State_Stand(FSM_State):
    
    def __init__(self, fsm):
        super(Character_State_Stand, self).__init__(fsm)
        self.sn = Character_State_Enum.STAND
    
    def enter(self):
        super(Character_State_Stand, self).enter()
        character = self.fsm.owner
        character.team.lvl_map.get_tile_by_coord(character.pos_x, character.pos_y).occupy = True
        print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Stand, self).update(et)
        if not self.fsm.owner.command_queue.empty():
            self.fsm.owner.direction = self.fsm.owner.command_queue.get()
        if self.fsm.owner.pos_x == self.fsm.owner.moving_target_x and self.fsm.owner.pos_y == self.fsm.owner.moving_target_y:
            self.fsm.owner.send_event(self.fsm.owner.team, Event_Character_Stop_Moving(EventType.CHARACTER_STOP_MOVING))
            self.fsm.owner.moving_target_x = 0
            self.fsm.owner.moving_target_y = 0
    
    def draw(self, et):
        super(Character_State_Stand, self).draw(et)
        self.fsm.owner.sprite_sheet.draw(0, self.fsm.owner.get_pos())

    def exit(self):
        super(Character_State_Stand, self).exit()
        character = self.fsm.owner
        character.team.lvl_map.get_tile_by_coord(character.pos_x, character.pos_y).occupy = False
        print self.fsm.owner.name + " exit state " + str(self.sn)

# MOVE state
class Character_State_Move(FSM_State):
    
    def __init__(self, fsm):
        super(Character_State_Move, self).__init__(fsm)
        self.sn = Character_State_Enum.MOVE
    
    def enter(self):
        super(Character_State_Move, self).enter()
        # print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Move, self).update(et)
        if not self.fsm.owner.command_queue.empty():
            self.fsm.owner.direction = self.fsm.owner.command_queue.get()
    
    def draw(self, et):
        super(Character_State_Move, self).draw(et)
        self.fsm.owner.sprite_sheet.draw(0, self.fsm.owner.get_pos())

    def exit(self):
        super(Character_State_Move, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)

# MOVE_RIGHT state
class Character_State_Move_Right(FSM_State):
    
    def __init__(self, fsm):
        super(Character_State_Move_Right, self).__init__(fsm)
        self.sn = Character_State_Enum.MOVE_RIGHT
        self.frame_num = 0
        self.acc_time = 0
        self.offset = 0
    
    def enter(self):
        super(Character_State_Move_Right, self).enter()
        # print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Move_Right, self).update(et)
        self.acc_time += et
        self.fsm.owner.pos_x += Character_Move_Frame.MOVE_STEP.value
        self.offset += Character_Move_Frame.MOVE_STEP.value
        if self.acc_time > Character_Move_Frame.FRAME_INTERVAL.value:
            self.acc_time > 0
            self.frame_num += 1
        if self.offset >= Character_Move_Frame.MOVE_ACC_OFFSET.value:
            self.offset = 0
            if not self.fsm.owner.command_queue.empty():
                self.fsm.owner.direction = self.fsm.owner.command_queue.get()
        
    def draw(self, et):
        super(Character_State_Move_Right, self).draw(et)
        frame_index = self.frame_num % Character_Move_Frame.DIRECTION_FRAME_NUM.value + Character_Move_Frame.MOVE_RIGHT_BEGIN.value
        self.fsm.owner.sprite_sheet.draw(frame_index, self.fsm.owner.get_pos())
        # print frame_index

    def exit(self):
        super(Character_State_Move_Right, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)

# MOVE_LEFT state, a sub-state of MOVE
class Character_State_Move_Left(FSM_State):
    
    def __init__(self, fsm):
        super(Character_State_Move_Left, self).__init__(fsm)
        self.sn = Character_State_Enum.MOVE_LEFT
        self.frame_num = 0
        self.acc_time = 0
        self.offset = 0
    
    def enter(self):
        super(Character_State_Move_Left, self).enter()
        # print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Move_Left, self).update(et)
        self.acc_time += et
        self.fsm.owner.pos_x -= Character_Move_Frame.MOVE_STEP.value
        self.offset += Character_Move_Frame.MOVE_STEP.value
        if self.acc_time > Character_Move_Frame.FRAME_INTERVAL.value:
            self.acc_time > 0
            self.frame_num += 1
        if self.offset >= Character_Move_Frame.MOVE_ACC_OFFSET.value:
            self.offset = 0
            if not self.fsm.owner.command_queue.empty():
                self.fsm.owner.direction = self.fsm.owner.command_queue.get()
    
    def draw(self, et):
        super(Character_State_Move_Left, self).draw(et)
        frame_index = self.frame_num % Character_Move_Frame.DIRECTION_FRAME_NUM.value + Character_Move_Frame.MOVE_LEFT_BEGIN.value
        self.fsm.owner.sprite_sheet.draw(frame_index, self.fsm.owner.get_pos())

    def exit(self):
        super(Character_State_Move_Left, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)

# MOVE_UP state, a sub-state of MOVE
class Character_State_Move_Up(FSM_State):
    
    def __init__(self, fsm):
        super(Character_State_Move_Up, self).__init__(fsm)
        self.sn = Character_State_Enum.MOVE_UP
        self.frame_num = 0
        self.acc_time = 0
        self.offset = 0
    
    def enter(self):
        super(Character_State_Move_Up, self).enter()
        # print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Move_Up, self).update(et)
        self.acc_time += et
        self.fsm.owner.pos_y -= Character_Move_Frame.MOVE_STEP.value
        self.offset += Character_Move_Frame.MOVE_STEP.value
        if self.acc_time > Character_Move_Frame.FRAME_INTERVAL.value:
            self.acc_time > 0
            self.frame_num += 1
        if self.offset >= Character_Move_Frame.MOVE_ACC_OFFSET.value:
            self.offset = 0
            if not self.fsm.owner.command_queue.empty():
                self.fsm.owner.direction = self.fsm.owner.command_queue.get()
    
    def draw(self, et):
        super(Character_State_Move_Up, self).draw(et)
        frame_index = self.frame_num % Character_Move_Frame.DIRECTION_FRAME_NUM.value + Character_Move_Frame.MOVE_UP_BEGIN.value
        self.fsm.owner.sprite_sheet.draw(frame_index, self.fsm.owner.get_pos())

    def exit(self):
        super(Character_State_Move_Up, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)

# MOVE_DOWN state, a sub-state of MOVE
class Character_State_Move_Down(FSM_State):
    
    def __init__(self, fsm):
        super(Character_State_Move_Down, self).__init__(fsm)
        self.sn = Character_State_Enum.MOVE_DOWN
        self.frame_num = 0
        self.acc_time = 0
        self.offset = 0
    
    def enter(self):
        super(Character_State_Move_Down, self).enter()
        # print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Move_Down, self).update(et)
        self.acc_time += et
        self.fsm.owner.pos_y += Character_Move_Frame.MOVE_STEP.value
        self.offset += Character_Move_Frame.MOVE_STEP.value
        if self.acc_time > Character_Move_Frame.FRAME_INTERVAL.value:
            self.acc_time > 0
            self.frame_num += 1
        if self.offset >= Character_Move_Frame.MOVE_ACC_OFFSET.value:
            self.offset = 0
            if not self.fsm.owner.command_queue.empty():
                self.fsm.owner.direction = self.fsm.owner.command_queue.get()
    
    def draw(self, et):
        super(Character_State_Move_Down, self).draw(et)
        frame_index = self.frame_num % Character_Move_Frame.DIRECTION_FRAME_NUM.value + Character_Move_Frame.MOVE_DOWN_BEGIN.value
        self.fsm.owner.sprite_sheet.draw(frame_index, self.fsm.owner.get_pos())

    def exit(self):
        super(Character_State_Move_Down, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)

# state transition
class Character_State_Move_Transition(FSM_Transition):
    
    def __init__(self, from_state, to_state, direction, fsm):
        super(Character_State_Move_Transition, self).__init__(from_state, to_state, fsm)
        self.trans_n = Character_State_Enum.MOVE_TRANSITION
        self.direction = direction

    def check_transition(self):
        super(Character_State_Move_Transition, self).check_transition()
        if self.fsm.owner.direction == self.direction:
            return True
        return False

class Character_State_StandToMove_transition(FSM_Transition):
    
    def __init__(self, from_state, to_state, direction, fsm):
        super(Character_State_StandToMove_transition, self).__init__(from_state, to_state, fsm)
        self.trans_n = Character_State_Enum.MOVE_TRANSITION
        self.direction = direction

    def check_transition(self):
        super(Character_State_StandToMove_transition, self).check_transition()
        if self.fsm.owner.direction == self.direction:
            return True
        return False

class Character_State_Die_Transition(FSM_Transition):
    
    def __init__(self, from_state, to_state, fsm):
        super(Character_State_Die_Transition, self).__init__(from_state, to_state, fsm)
        self.trans_n = Character_State_Enum.DIE_TRANSITION

    def check_transition(self):
        super(Character_State_Die_Transition, self).check_transition()
        if self.fsm.owner.hp <= 0:
            return True
        return False


# character class
class Character(EventObject):

    def __init__(self, cn, sprite_sheet, team):
        super(Character, self).__init__()
        self.name = cn
        self.sprite = None # character picture
        self.fsm = FSM_Machine(self)
        self.sprite_sheet = sprite_sheet
        self.team = team
        self.selected = False
        team.add_character(self)

        # property for test
        self.moving_target_x = 360
        self.moving_target_y = 324
        self.pos_x = 288
        self.pos_y = 288

        self.lvl = 1            # level
        self.exp = 0            # experience
        self.ap = 15            # action point, for moving, attacking and spelling
        self.hp = 1             # health point
        self.mp = 1             # magic point
        self.agility = 1        # agility
        self.strength = 1       # strength
        self.intelligence = 1   # intelligence
        self.defense = 1        # defense
        self.resistance = 1     # resistance
        self.attack = 1
        self.attack_range = 1   # physical attack range, will be not shown at character plane

        self.direction = Character_State_Enum.STAND
        self.command_queue = Queue.Queue()
        # control for test
#        self.command_queue.put(Character_State_Enum.MOVE_DOWN)
#        self.command_queue.put(Character_State_Enum.MOVE_DOWN)
#        self.command_queue.put(Character_State_Enum.MOVE_DOWN)
#        self.command_queue.put(Character_State_Enum.MOVE_RIGHT)
#        self.command_queue.put(Character_State_Enum.MOVE_RIGHT)
#        self.command_queue.put(Character_State_Enum.MOVE_RIGHT)
#        self.command_queue.put(Character_State_Enum.MOVE_UP)
#        self.command_queue.put(Character_State_Enum.MOVE_LEFT)
#        self.command_queue.put(Character_State_Enum.MOVE_UP)
#        self.command_queue.put(Character_State_Enum.STAND)

        # add states
        self.fsm.add_state(Character_State_Stand(self.fsm))
        self.fsm.add_state(Character_State_Move_Down(self.fsm))
        self.fsm.add_state(Character_State_Move_Left(self.fsm))
        self.fsm.add_state(Character_State_Move_Right(self.fsm))
        self.fsm.add_state(Character_State_Move_Up(self.fsm))

        # add transitions
        '''
                        |---> move right -->|    
                        |---> move left  -->|   
                stand --|---> die           |--->stand
                        |---> move down  -->|
                        |---> move left  -->|
        '''
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_LEFT, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_RIGHT,Character_State_Enum.MOVE_RIGHT, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_UP,Character_State_Enum.MOVE_UP, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_DOWN, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_LEFT, Character_State_Enum.STAND, Character_State_Enum.STAND, self.fsm))

        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_RIGHT, Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_LEFT, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_RIGHT, Character_State_Enum.MOVE_RIGHT,Character_State_Enum.MOVE_RIGHT, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_RIGHT, Character_State_Enum.MOVE_UP,Character_State_Enum.MOVE_UP, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_RIGHT, Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_DOWN, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_RIGHT, Character_State_Enum.STAND, Character_State_Enum.STAND, self.fsm))

        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_LEFT, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_RIGHT,Character_State_Enum.MOVE_RIGHT, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_UP,Character_State_Enum.MOVE_UP, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_DOWN, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_DOWN, Character_State_Enum.STAND, Character_State_Enum.STAND, self.fsm))

        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_UP, Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_LEFT, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_UP, Character_State_Enum.MOVE_RIGHT,Character_State_Enum.MOVE_RIGHT, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_UP, Character_State_Enum.MOVE_UP,Character_State_Enum.MOVE_UP, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_UP, Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_DOWN, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_UP, Character_State_Enum.STAND, Character_State_Enum.STAND, self.fsm))

        self.fsm.add_transition(Character_State_StandToMove_transition(Character_State_Enum.STAND, Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_LEFT, self.fsm))
        self.fsm.add_transition(Character_State_StandToMove_transition(Character_State_Enum.STAND, Character_State_Enum.MOVE_RIGHT,Character_State_Enum.MOVE_RIGHT, self.fsm))
        self.fsm.add_transition(Character_State_StandToMove_transition(Character_State_Enum.STAND, Character_State_Enum.MOVE_UP,Character_State_Enum.MOVE_UP, self.fsm))
        self.fsm.add_transition(Character_State_StandToMove_transition(Character_State_Enum.STAND, Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_DOWN, self.fsm))

        self.fsm.add_transition(Character_State_Die_Transition(Character_State_Enum.STAND, Character_State_Enum.DEAD, self.fsm))

        self.fsm.owner = self

        self.fsm.change_to_state(Character_State_Enum.STAND)
#        self.fsm.cur_state = self.fsm.states[Character_State_Enum.STAND]

        # event handler

    def set_picture(self, pic_path):
        self.sprite = pygame.image.load(pic_path).convert_alpha()

    def update(self, et):
        self.process_evt_queue()
        self.fsm.update(et)

    def draw(self, et):
        self.fsm.draw(et)

    def get_pos(self):
        return self.pos_x, self.pos_y

    def set_moving_target(self, x, y):
        self.moving_target_x = x
        self.moving_target_y = y