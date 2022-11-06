import collections
import ast
import itertools

# is_continuous_seq and get_move_type classifies the move
# inspiration from: DouZero https://github.com/kwai/DouZero

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

def select(cards, num):
    return [list(i) for i in itertools.combinations(cards, num)]

class MovesGener(object):
    """
    This is for generating the possible combinations
    """

    def __init__(self, cards_list):
        RealCard2EnvCard = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                    '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12,
                    'K': 13, 'A': 14, '2': 17, 'X': 20, 'D': 30}
        self.cards_list = []
        for i in cards_list:
            if i[-1] == '0':
                self.cards_list.append(RealCard2EnvCard['10'])
            else:
                self.cards_list.append(RealCard2EnvCard[i[-1]])
        self.cards_dict = collections.defaultdict(int)

        for i in self.cards_list:
            self.cards_dict[i] += 1

        self.single_card_moves = []
        self.gen_type_1_single()
        self.pair_moves = []
        self.gen_type_2_pair()
        self.triple_cards_moves = []
        self.gen_type_3_triple()
        self.bomb_moves = []
        self.gen_type_4_bomb()
        self.final_bomb_moves = []
        self.gen_type_5_king_bomb()

    def _gen_serial_moves(self, cards, min_serial, repeat=1, repeat_num=0):
        if repeat_num < min_serial:  # at least repeat_num is min_serial
            repeat_num = 0

        single_cards = sorted(list(set(cards)))
        seq_records = list()
        moves = list()

        start = i = 0
        longest = 1
        while i < len(single_cards):
            if i + 1 < len(single_cards) and single_cards[i + 1] - single_cards[i] == 1:
                longest += 1
                i += 1
            else:
                seq_records.append((start, longest))
                i += 1
                start = i
                longest = 1

        for seq in seq_records:
            if seq[1] < min_serial:
                continue
            start, longest = seq[0], seq[1]
            longest_list = single_cards[start: start + longest]

            if repeat_num == 0:  # No limitation on how many sequences
                steps = min_serial
                while steps <= longest:
                    index = 0
                    while steps + index <= longest:
                        target_moves = sorted(longest_list[index: index + steps] * repeat)
                        moves.append(target_moves)
                        index += 1
                    steps += 1

            else:  # repeat_num > 0
                if longest < repeat_num:
                    continue
                index = 0
                while index + repeat_num <= longest:
                    target_moves = sorted(longest_list[index: index + repeat_num] * repeat)
                    moves.append(target_moves)
                    index += 1

        return moves

    def gen_type_1_single(self):
        self.single_card_moves = []
        for i in set(self.cards_list):
            self.single_card_moves.append([i])
        return self.single_card_moves

    def gen_type_2_pair(self):
        self.pair_moves = []
        for k, v in self.cards_dict.items():
            if v >= 2:
                self.pair_moves.append([k, k])
        return self.pair_moves

    def gen_type_3_triple(self):
        self.triple_cards_moves = []
        for k, v in self.cards_dict.items():
            if v >= 3:
                self.triple_cards_moves.append([k, k, k])
        return self.triple_cards_moves

    def gen_type_4_bomb(self):
        self.bomb_moves = []
        for k, v in self.cards_dict.items():
            if v == 4:
                self.bomb_moves.append([k, k, k, k])
        return self.bomb_moves

    def gen_type_5_king_bomb(self):
        self.final_bomb_moves = []
        if 20 in self.cards_list and 30 in self.cards_list:
            self.final_bomb_moves.append([20, 30])
        return self.final_bomb_moves

    def gen_type_6_3_1(self):
        result = []
        for t in self.single_card_moves:
            for i in self.triple_cards_moves:
                if t[0] != i[0]:
                    result.append(t+i)
        return result

    def gen_type_7_3_2(self):
        result = list()
        for t in self.pair_moves:
            for i in self.triple_cards_moves:
                if t[0] != i[0]:
                    result.append(t+i)
        return result

    def gen_type_8_serial_single(self, repeat_num=0):
        return self._gen_serial_moves(self.cards_list, 5, repeat=1, repeat_num=repeat_num)

    def gen_type_9_serial_pair(self, repeat_num=0):
        single_pairs = list()
        for k, v in self.cards_dict.items():
            if v >= 2:
                single_pairs.append(k)

        return self._gen_serial_moves(single_pairs, 3, repeat=2, repeat_num=repeat_num)

    def gen_type_10_serial_triple(self, repeat_num=0):
        single_triples = list()
        for k, v in self.cards_dict.items():
            if v >= 3:
                single_triples.append(k)

        return self._gen_serial_moves(single_triples, 2, repeat=3, repeat_num=repeat_num)

    def gen_type_11_serial_3_1(self, repeat_num=0):
        serial_3_moves = self.gen_type_10_serial_triple(repeat_num=repeat_num)
        serial_3_1_moves = list()

        for s3 in serial_3_moves:  # s3 is like [3,3,3,4,4,4]
            s3_set = set(s3)
            new_cards = [i for i in self.cards_list if i not in s3_set]

            # Get any s3_len items from cards
            subcards = select(new_cards, len(s3_set))

            for i in subcards:
                serial_3_1_moves.append(s3 + i)

        return list(k for k, _ in itertools.groupby(serial_3_1_moves))

    def gen_type_12_serial_3_2(self, repeat_num=0):
        serial_3_moves = self.gen_type_10_serial_triple(repeat_num=repeat_num)
        serial_3_2_moves = list()
        pair_set = sorted([k for k, v in self.cards_dict.items() if v >= 2])

        for s3 in serial_3_moves:
            s3_set = set(s3)
            pair_candidates = [i for i in pair_set if i not in s3_set]

            # Get any s3_len items from cards
            subcards = select(pair_candidates, len(s3_set))
            for i in subcards:
                serial_3_2_moves.append(sorted(s3 + i * 2))

        return serial_3_2_moves

    def gen_type_13_4_2(self):
        four_cards = list()
        for k, v in self.cards_dict.items():
            if v == 4:
                four_cards.append(k)

        result = list()
        for fc in four_cards:
            cards_list = [k for k in self.cards_list if k != fc]
            subcards = select(cards_list, 2)
            for i in subcards:
                result.append([fc]*4 + i)
        return list(k for k, _ in itertools.groupby(result))

    def gen_type_14_4_22(self):
        four_cards = list()
        for k, v in self.cards_dict.items():
            if v == 4:
                four_cards.append(k)

        result = list()
        for fc in four_cards:
            cards_list = [k for k, v in self.cards_dict.items() if k != fc and v>=2]
            subcards = select(cards_list, 2)
            for i in subcards:
                result.append([fc] * 4 + [i[0], i[0], i[1], i[1]])
        return result

    # generate all possible moves from given cards
    def gen_moves(self):
        moves = []
        moves.extend(self.gen_type_1_single())
        moves.extend(self.gen_type_2_pair())
        moves.extend(self.gen_type_3_triple())
        moves.extend(self.gen_type_4_bomb())
        moves.extend(self.gen_type_5_king_bomb())
        moves.extend(self.gen_type_6_3_1())
        moves.extend(self.gen_type_7_3_2())
        moves.extend(self.gen_type_8_serial_single())
        moves.extend(self.gen_type_9_serial_pair())
        moves.extend(self.gen_type_10_serial_triple())
        moves.extend(self.gen_type_11_serial_3_1())
        moves.extend(self.gen_type_12_serial_3_2())
        moves.extend(self.gen_type_13_4_2())
        moves.extend(self.gen_type_14_4_22())
        return moves