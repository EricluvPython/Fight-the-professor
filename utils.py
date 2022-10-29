import collections
import ast

# is_continuous_seq and get_move_type classifies the move
# inspiration from: DouZero https://github.com/kwai/DouZero/tree/d731ca2ca507f2a53d6ca19a2acdb0b284046d0c

# check if move is a continuous sequence


def is_continuous_seq(move):
    i = 0
    while i < len(move) - 1:
        if move[i+1] - move[i] != 1:
            return False
        i += 1
    return True

# main function of getting the move type and rank


def get_move_type(move):
    move_size = len(move)
    move_dict = collections.Counter(move)

    if move_size == 0:  # pass
        return {'type': 0}

    if move_size == 1:  # single
        return {'type': 1, 'rank': move[0]}

    if move_size == 2:
        if move[0] == move[1]:  # pair
            return {'type': 2, 'rank': move[0]}
        elif move == [20, 30]:  # Kings
            return {'type': 5}
        else:  # invalid
            return {'type': 15}

    if move_size == 3:
        if len(move_dict) == 1:  # triple
            return {'type': 3, 'rank': move[0]}
        else:  # invalid
            return {'type': 15}

    if move_size == 4:
        if len(move_dict) == 1:  # bomb
            return {'type': 4,  'rank': move[0]}
        elif len(move_dict) == 2:  # 3+1
            if move[0] == move[1] == move[2] or move[1] == move[2] == move[3]:
                return {'type': 6, 'rank': move[1]}
            else:  # invalid
                return {'type': 15}
        else:  # invalid
            return {'type': 15}

    if is_continuous_seq(move):  # solo chain
        return {'type': 8, 'rank': move[0], 'len': len(move)}

    if move_size == 5:
        if len(move_dict) == 2:  # 3+2
            return {'type': 7, 'rank': move[2]}
        else:  # invalid
            return {'type': 15}

    count_dict = collections.defaultdict(int)
    for c, n in move_dict.items():
        count_dict[n] += 1

    if move_size == 6:  # 4+2
        if (len(move_dict) == 2 or len(move_dict) == 3) and count_dict.get(4) == 1 and \
                (count_dict.get(2) == 1 or count_dict.get(1) == 2):
            return {'type': 13, 'rank': move[2]}
    # 4+2*2
    if move_size == 8 and (((len(move_dict) == 3 or len(move_dict) == 2) and
                            (count_dict.get(4) == 1 and count_dict.get(2) == 2)) or count_dict.get(4) == 2):
        return {'type': 14, 'rank': max([c for c, n in move_dict.items() if n == 4])}

    mdkeys = sorted(move_dict.keys())
    if len(move_dict) == count_dict.get(2) and is_continuous_seq(mdkeys):
        # airplane (serial pair)
        return {'type': 9, 'rank': mdkeys[0], 'len': len(mdkeys)}

    if len(move_dict) == count_dict.get(3) and is_continuous_seq(mdkeys):
        # rocket (serial triple)
        return {'type': 10, 'rank': mdkeys[0], 'len': len(mdkeys)}

    # Check Type 11 (serial 3+1) and Type 12 (serial 3+2)
    if count_dict.get(3, 0) >= 2:
        serial_3 = list()
        single = list()
        pair = list()

        for k, v in move_dict.items():
            if v == 3:
                serial_3.append(k)
            elif v == 1:
                single.append(k)
            elif v == 2:
                pair.append(k)
            else:  # no other possibilities
                return {'type': 15}

        serial_3.sort()
        if is_continuous_seq(serial_3):
            if len(serial_3) == len(single)+len(pair)*2:
                # 3+1
                return {'type': 11, 'rank': serial_3[0], 'len': len(serial_3)}
            if len(serial_3) == len(pair) and len(move_dict) == len(serial_3) * 2:
                # 3+2
                return {'type': 12, 'rank': serial_3[0], 'len': len(serial_3)}

        if len(serial_3) == 4:
            if is_continuous_seq(serial_3[1:]):
                return {'type': 11, 'rank': serial_3[1], 'len': len(serial_3) - 1}
            if is_continuous_seq(serial_3[:-1]):
                return {'type': 11, 'rank': serial_3[0], 'len': len(serial_3) - 1}

    return {'type': 15}  # invalid

# helper function for converting remote game data


def convertHelper(s):
    s = ast.literal_eval(s)
    for i in range(len(s)):
        if len(s[i]) > 1:
            if s[i][-1] == '0':
                s[i] = s[i][:-2]+' '+s[i][-2:]
            else:
                s[i] = s[i][:-1]+' '+s[i][-1]
    return s

# another helper function for converting different game data


def anotherConvertHelper(s):
    s = ast.literal_eval(s)
    for i in range(len(s[1])):
        if len(s[1][i]) > 1:
            if s[1][i][-1] == '0':
                s[1][i] = s[1][i][:-2]+' '+s[1][i][-2:]
            else:
                s[1][i] = s[1][i][:-1]+' '+s[1][i][-1]
    return s
