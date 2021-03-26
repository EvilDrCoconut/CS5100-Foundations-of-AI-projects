from pypokerengine.players import BasePokerPlayer
from pypokerengine.engine import action_checker
from pypokerengine.engine import dealer
from pypokerengine.engine import player
from pypokerengine.utils import action_utils
from pypokerengine.engine import table

class MinimaxAgent(BasePokerPlayer):
    def manhattanDistance(xy1, xy2):
        "Returns the Manhattan distance between points xy1 and xy2"
        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
    def getAction(self, gameState):
        depth = self.depth
        num = gameState.getNumAgents()
        def generateSuccessor(playerNum,action):
            return
        def minimax(state, depth, current_depth, ghostNumber):
            current_depth += 1
            if depth * ghostNumber == current_depth or state.isLose() or state.isWin():
                return self.bluff(state), "Stop"
            if current_depth==ghostNumber or current_depth==0:
                v = float('-Inf')
                for action in action_utils.generate_legal_actions(players, player_pos, sb_amount):
                    result, max_move = minimax(table.next_active_player_pos(start_pos), depth, current_depth, ghostNumber)
                    if result > v:
                        v = result
                        move = action
                return v, move
            else:
                current_ghost = current_depth % ghostNumber
                v = float('Inf')
                for action in action_utils.generate_legal_actions.legal_actions(sb_amount):
                    result, min_move = minimax(table.next_active_player_pos(start_pos), depth, current_depth, ghostNumber)
                    if result < v:
                        v = result
                        move = action
                return v, move

        result, action = minimax(gameState, depth, -1, num)
        return result

    class AlphaBetaAgent(BasePokerPlayer):

        def getAction(self, gameState):

            numb = gameState.getNumAgents()
            dep = self.depth
            def alpha_beta(state, depth, alpha, beta, index, n=numb, depth_=dep):
                if depth == depth_ or state.isWin() or state.isLose():
                    return self.evaluationFunction(state), " "

                if index == 0:
                    max_value = -999999.0
                    move_ = " "
                    for action in state.getLegalActions(0):
                        value = alpha_beta(state.generateSuccessor(0, action), depth, alpha, beta, (index + 1) % n)[0]
                        if value > max_value:
                            max_value = value
                            move_ = action
                            if max_value > beta:
                                return max_value, move_
                            if alpha < max_value:
                                alpha = max_value
                    return max_value, move_

                else:
                    min_value = 99999999
                    if index == n - 1:
                        depth += 1
                    for action in state.getLegalActions(index):
                        value = alpha_beta(state.generateSuccessor(index, action), depth, alpha, beta, (index + 1) % n)[
                            0]
                        if value < min_value:
                            min_value = value
                            if min_value < alpha:
                                return min_value, " "
                            if beta > min_value:
                                beta = min_value
                    return min_value, " "

            result = alpha_beta(gameState, 0, -99999999, 99999999, 0)
            return result[1]




