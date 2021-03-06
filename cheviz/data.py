# AUTOGENERATED! DO NOT EDIT! File to edit: 01_data.ipynb (unless otherwise specified).

__all__ = ['fetch', 'Game', 'fromGame', 'games', 'MoveSequencerResult', 'makeMoveSequencer', 'diffReduce', 'countZeros',
           'makeDiffReduceAnalyzer', 'zerosDiffReduce']

# Cell
from pathlib import Path
import urllib.request
import shutil

def fetch()->dict:
    result = {}
    url_prefix = 'https://pgnchessbook.org/wp-content/uploads/2019/08/'
    data_files = ['WorldChamp_1986_to_2018.pgn', 'Candidates_1953.pgn', 'WijkaanZee2019.pgn', 'Shamkir2019.pgn', 'Baden2019.pgn']

    for file in data_files:
        src = url_prefix + file
        dst = Path().absolute() / 'data' / file
        if not dst.is_file():
            with urllib.request.urlopen(src) as response, open(dst, 'wb') as dst_file:
                shutil.copyfileobj(response, dst_file)

        if dst.is_file():
            result[file] = dst

    return result

# Cell
from typing import NamedTuple
import chess.pgn


class Game(NamedTuple):
    board: chess.Board
    moves: chess.pgn.Mainline
    headers: chess.pgn.Headers


def fromGame(game:chess.pgn.Game)->tuple:
    return Game(game.board(), game.mainline_moves(), game.headers)


def games(pgn_name:str)->tuple:
    with open(pgn_name, 'r') as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break

            yield fromGame(game)

# Cell
from typing import Callable, NamedTuple
import numpy as np
from cheviz import core
import chess.pgn


class MoveSequencerResult(NamedTuple):
    result: list
    board: chess.Board


def makeMoveSequencer(moves_list:list)->Callable:
    # to represent the initial position, we insert an 'empty' move in front:
    board = chess.Board()
    ts = core.makeThreatenedSquares(board=board)

    def moveSequencer(moves_range:range, side:bool, square_filter:Callable)->np.ndarray:
        result = []
        board.reset()

        start = -1 if moves_range.start == - 1 else 0
        stop = min(len(moves_list), moves_range.stop)

        for index in range(start, stop):
            # print("loop", index, start, stop)
            was_our_turn = board.turn == side # check *before* pushing next move
            adjusted_start = moves_range.start if was_our_turn else moves_range.start - 1

            move_to_push = None if index == -1 else moves_list[index]
            if move_to_push is not None:
                # print("empty move", index, was_our_turn, adjusted_start)
                board.push(moves_list[index])

            if index >= adjusted_start and was_our_turn:
                # print("result push", index, was_our_turn, adjusted_start)
                result.append(ts(side, square_filter))

        return MoveSequencerResult(result, board)

    return moveSequencer

# Cell
def diffReduce(data:list):
    while len(data) > 1:
        data = [data[i] - data[i + 1] for i in range(len(data) - 1)]
    data = data.pop() if len(data) == 1 else np.zeros(core.dimension() ** 2)
    return data

# Cell
def countZeros(data:np.ndarray)->int:
    unique, counts = np.unique(data, return_counts=True)
    return dict(zip(unique, counts))[0]

# Cell
def makeDiffReduceAnalyzer(move_list:list, square_filter:Callable)->Callable:
    ms = makeMoveSequencer(moves_list)

    def analyzer(mr:range, side:bool)->np.ndarray:
        return diffReduce(ms(mr, side, square_filter).result)

    return analyzer


def zerosDiffReduce(moves_total:int, move_window_size:int, side:bool, analyzer:Callable)->list:
    result = []
    for i in range(0 if side else 1, moves_total, 2):
        data = analyzer(range(i, i + move_window_size), side)
        result.append(countZeros(data))
    return result