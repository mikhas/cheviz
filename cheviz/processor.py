# AUTOGENERATED! DO NOT EDIT! File to edit: 04_processor.ipynb (unless otherwise specified).

__all__ = ['Processor']

# Cell
from typing import Callable
import pandas as pd
import numpy as np
import chess.engine
import cheviz.core as cco
import cheviz.data as cda
import cheviz.stockfish as cst

# Cell
class Processor:
    def __init__(self, engine_maker:Callable, game:cda.Game, first_move_by_white=True):
        self.engine_maker = engine_maker
        self.moves = list(game.moves)
        self.first_move_by_white = first_move_by_white
        # FIXME: Fix makeMoveSequencer to indicate that each side needs its own instance,
        # due to how the square filter works (hint: shared board instance).
        self.msw = cda.makeMoveSequencer(self.moves)
        self.msb = cda.makeMoveSequencer(self.moves)
        self.msz = cda.makeMoveSequencer(self.moves)


    def run(self, reduced:Callable, square_filter:Callable, echo:int=1, depth:int=20)->pd.DataFrame:
        engine = self.engine_maker()
        result = pd.DataFrame(columns=['SideThatMoved', 'SideToMove', 'PovScore',
                                       'HalfMoveConfiguration', 'FEN',
                                       'LastWhiteMove', 'LastBlackMove',
                                       'ViewForWhite', 'ViewForBlack',
                                       'Zeros', 'ZerosWithEcho'])

        for curr_move in range(0, len(self.moves)):
            bm_offset = (curr_move + 1) % 2
            adjusted_wm = (curr_move // 2) * 2
            adjusted_bm = curr_move - bm_offset

            side = bool(bm_offset) # white: 1, black: 0, same as in python-chess
            if not self.first_move_by_white:
                adjusted_wm, adjusted_bm = adjusted_bm, adjusted_wm # not tested!

            last_white_move = self.moves[adjusted_wm]
            last_black_move = self.moves[adjusted_bm] if adjusted_bm > -1 else None

            white = self.msw(range(adjusted_wm - (echo * 2) , adjusted_wm + 1), chess.WHITE, square_filter)
            black = self.msb(range(adjusted_bm - (echo * 2), adjusted_bm + 1), chess.BLACK, square_filter)
            zeros_white = reduced(self.msz(range(curr_move, curr_move + 1), chess.WHITE, square_filter).result)
            zeros_black = reduced(self.msz(range(curr_move, curr_move + 1), chess.BLACK, square_filter).result)

            reduced_white = reduced(white.result)
            reduced_black = reduced(black.result)

            # would be nice if engine.analyse could be made to run async/in parallel
            current_board = white.board if side else black.board
            info = engine.analyse(current_board, chess.engine.Limit(depth=depth))

            result.loc[curr_move] = ['White' if side else 'Black',
                                     'Black' if side else 'White',
                                     info['score'], (curr_move, adjusted_wm, adjusted_bm),
                                     current_board.fen(), last_white_move, last_black_move,
                                     reduced_white, reduced_black,
                                     cda.countZeros(np.logical_or(zeros_white, zeros_black)),
                                     cda.countZeros(np.logical_or(reduced_white, reduced_black))]

        engine.quit() # This is important, otherwise we leak opened file objects!
        return result