import numpy as np
import pandas as pd

class Player:
    def __init__(self, name, probabilities):
        self.name = name
        self.probabilities = np.array(probabilities)  # [単打, 二塁打, 三塁打, 本塁打, 四死球, アウト]
        self.hits = 0  # ヒット数
        self.at_bats = 0  # 打席数
        self.walks = 0  # 四死球数
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

        # 打席数の更新 (四死球は除く)
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
        return self.hits / self.at_bats if self.at_bats > 0 else 0

    def on_base_percentage(self):
        # 出塁率 = (ヒット数 + 四死球数) / 総打席数
        total_plate_appearances = self.at_bats + self.walks
        return (self.hits + self.walks) / total_plate_appearances if total_plate_appearances > 0 else 0

    def sllugging_percentage(self):
        # 長打率＝（ヒット数＋二塁打＊2＋三塁打＊3＋本塁打＊4）/ 打数
        return self.sllugging / self.at_bats if self.at_bats > 0 else 0
    
    def ops(self):
        return self.on_base_percentage() + self.sllugging_percentage()
    
    def detailed_stats(self):
        # 詳細成績を返す
        return {
            "単打": self.singles,
            "二塁打": self.doubles,
            "三塁打": self.triples,
            "本塁打": self.homeruns,
            "打席数": self.at_bats,
            "四死球": self.walks
        }


def simulate_game(players):
    lineup = players[:]
    score = 0
    game_log = []  # 試合の流れを記録

    for inning in range(9):  # 9回までシミュレーション
        outs = 0
        bases = np.zeros(3, dtype=int)  # 塁の状態を保持 [一塁, 二塁, 三塁]
        inning_log = []

        while outs < 3:
            player = lineup.pop(0)  # 打者を順番に取り出す
            result = player.simulate_at_bat()
            inning_log.append((player.name, result))

            if result == "アウト":
                outs += 1
            else:
                advance = {"単打": 1, "二塁打": 2, "三塁打": 3, "本塁打": 4, "四死球": 0}[result]
                runs = 0

                # ランナーを進塁させる
                for i in range(2, -1, -1):
                    if bases[i] == 1:
                        if i + advance >= 3:  # ホームイン
                            runs += 1
                            bases[i] = 0
                        else:
                            bases[i + advance] = 1
                            bases[i] = 0

                # 打者の進塁を処理
                if advance < 4:
                    bases[advance - 1] = 1
                else:  # 本塁打
                    runs += 1

                # スコアを更新し打点を記録
                score += runs
                player.runs_batted_in += runs

            lineup.append(player)  # 打者を打順の最後に戻す

        game_log.append((inning + 1, inning_log))

    return score, game_log

