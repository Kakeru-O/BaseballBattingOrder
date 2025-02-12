import numpy as np
import pandas as pd

class Player:
    def __init__(self, name, probabilities):
        self.name = name
        self.probabilities = np.array(probabilities)  # [単打, 二塁打, 三塁打, 本塁打, 四死球, アウト]
        self.hits = 0  # ヒット数
        self.at_bats = 0  # 打数
        self.walks = 0  # 四死球数
        self.daseki = 0 # 打席数
        self.runs_batted_in = 0  # 打点
        self.singles = 0  # 単打数
        self.doubles = 0  # 二塁打数
        self.triples = 0  # 三塁打数
        self.homeruns = 0  # 本塁打数
        self.sllugging = 0 # 長打数

    def simulate_at_bat(self):
        # ランダムに結果を決定
        outcome = np.random.choice([
            "single", "double", "triple", "homerun", "walk", "out"
        ], p=self.probabilities)
        
        self.daseki += 1
        # 打数の更新 (四死球は除く)
        if outcome != "walk":
            self.at_bats += 1

        if outcome == "single":
            self.hits += 1
            self.singles += 1
            self.sllugging += 1
            return "単打"
        elif outcome == "double":
            self.hits += 1
            self.doubles += 1
            self.sllugging += 2
            return "二塁打"
        elif outcome == "triple":
            self.hits += 1
            self.triples += 1
            self.sllugging += 3
            return "三塁打"
        elif outcome == "homerun":
            self.hits += 1
            self.homeruns += 1
            self.sllugging += 4
            return "本塁打"
        elif outcome == "walk":
            self.walks += 1
            return "四死球"
        else:  # "out"
            return "アウト"

    def batting_average(self):
        # 打率 = ヒット数 / 打数
        return self.hits / self.at_bats if self.at_bats > 0 else 0.

    def on_base_percentage(self):
        # 出塁率 = (ヒット数 + 四死球数) / 総打席数
        return (self.hits + self.walks) / self.daseki if self.daseki > 0 else 0.

    def sllugging_percentage(self):
        # 長打率＝（ヒット数＋二塁打＊2＋三塁打＊3＋本塁打＊4）/ 打数
        return self.sllugging / self.at_bats if self.at_bats > 0 else 0.
    
    def ops(self):
        return self.on_base_percentage() + self.sllugging_percentage()
    
    def detailed_stats(self):
        # 詳細成績を返す
        return {
            "安打":self.hits,
            "単打": self.singles,
            "二塁打": self.doubles,
            "三塁打": self.triples,
            "本塁打": self.homeruns,
            "打数": self.at_bats,
            "打席数":self.daseki,
            "四死球": self.walks
        }


def simulate_game_1(players):
    lineup = players[:]
    score = 0
    game_log = []  # 試合の流れを記録

    for inning in range(8):  # 9回までシミュレーション
        outs = 0
        bases = np.zeros(3, dtype=int)  # 塁の状態を保持 [一塁, 二塁, 三塁]
        inning_log = []

        while outs < 3:
            player = lineup.pop(0)  # 打者を順番に取り出す
            result = player.simulate_at_bat()

            if result == "アウト":
                outs += 1
            else:
                advance = {"単打": 1, "二塁打": 2, "三塁打": 3, "本塁打": 4, "四死球": 1}[result]
                runs = 0

                # 満塁時の四死球処理
                if result == "四死球" and all(bases):  # 全ての塁が埋まっている場合
                    runs += 1  # 三塁ランナーがホームイン
                    bases[2] = bases[1]  # 2塁ランナーが3塁へ
                    bases[1] = bases[0]  # 1塁ランナーが2塁へ
                    bases[0] = 1  # 打者が1塁へ
                else:
                    # ランナー進塁と得点の計算
                    # 3塁ランナーの処理
                    if bases[2] == 1:
                        if result in ["単打", "二塁打", "三塁打", "本塁打"]:
                            runs += 1
                            bases[2] = 0

                    # 2塁ランナーの処理
                    if bases[1] == 1:
                        if advance >= 2:
                            runs += 1
                            bases[1] = 0
                        #elif advance == 1:
                        else:
                            bases[2] = 1
                            bases[1] = 0

                    # 1塁ランナーの処理
                    if bases[0] == 1:
                        if advance >= 3:
                            runs += 1
                            bases[0] = 0
                        elif advance == 2:
                            bases[2] = 1
                            bases[0] = 0
                        elif advance == 1:
                            bases[1] = 1
                            bases[0] = 0

                    # 打者の処理
                    if advance < 4:
                        bases[advance - 1] = 1
                    else:  # 本塁打
                        runs += 1


                # スコアを更新し打点を記録
                score += runs
                player.runs_batted_in += runs

                # 打点も記録する
                if runs>0:
                    result = result+str(runs)
                
            inning_log.append((player.name, result))

            lineup.append(player)  # 打者を打順の最後に戻す

        game_log.append((inning + 1, inning_log))

    return score, game_log


def simulate_game(players):
    lineup = players[:]
    score = 0

    for inning in range(8):  # 9回までシミュレーション
        outs = 0
        bases = np.zeros(3, dtype=int)  # 塁の状態を保持 [一塁, 二塁, 三塁]

        while outs < 3:
            player = lineup.pop(0)  # 打者を順番に取り出す
            result = player.simulate_at_bat()

            if result == "アウト":
                outs += 1
            else:
                advance = {"単打": 1, "二塁打": 2, "三塁打": 3, "本塁打": 4, "四死球": 1}[result]
                runs = 0

                # 満塁時の四死球処理
                if result == "四死球" and all(bases):  # 全ての塁が埋まっている場合
                    runs += 1  # 三塁ランナーがホームイン
                    bases[2] = bases[1]  # 2塁ランナーが3塁へ
                    bases[1] = bases[0]  # 1塁ランナーが2塁へ
                    bases[0] = 1  # 打者が1塁へ
                else:
                    # ランナー進塁と得点の計算
                    # 3塁ランナーの処理
                    if bases[2] == 1:
                        if result in ["単打", "二塁打", "三塁打", "本塁打"]:
                            runs += 1
                            bases[2] = 0

                    # 2塁ランナーの処理
                    if bases[1] == 1:
                        if advance >= 2:
                            runs += 1
                            bases[1] = 0
                        #elif advance == 1:
                        else:
                            bases[2] = 1
                            bases[1] = 0

                    # 1塁ランナーの処理
                    if bases[0] == 1:
                        if advance >= 3:
                            runs += 1
                            bases[0] = 0
                        elif advance == 2:
                            bases[2] = 1
                            bases[0] = 0
                        elif advance == 1:
                            bases[1] = 1
                            bases[0] = 0

                    # 打者の処理
                    if advance < 4:
                        bases[advance - 1] = 1
                    else:  # 本塁打
                        runs += 1

                # スコアを更新し打点を記録
                score += runs
                player.runs_batted_in += runs

            lineup.append(player)  # 打者を打順の最後に戻す

    return score
