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
        self.slugging = 0 # 長打数

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
            self.slugging += 1
            return "単打"
        elif outcome == "double":
            self.hits += 1
            self.doubles += 1
            self.slugging += 2
            return "二塁打"
        elif outcome == "triple":
            self.hits += 1
            self.triples += 1
            self.slugging += 3
            return "三塁打"
        elif outcome == "homerun":
            self.hits += 1
            self.homeruns += 1
            self.slugging += 4
            return "本塁打"
        elif outcome == "walk":
            self.walks += 1
            return "四死球"
        else:  # "out"
            return "アウト"

    def batting_average(self):
        # 打率 = ヒット数 / 打席数
        return self.hits / self.at_bats if self.at_bats > 0 else 0

    def on_base_percentage(self):
        # 出塁率 = (ヒット数 + 四死球数) / 総打席数
        total_plate_appearances = self.at_bats + self.walks
        return (self.hits + self.walks) / total_plate_appearances if total_plate_appearances > 0 else 0

    def slugging_percentage(self):
        # 長打率＝（ヒット数＋二塁打＊2＋三塁打＊3＋本塁打＊4）/ 総打席数
        total_plate_appearances = self.at_bats + self.walks
        return self.slugging / total_plate_appearances if total_plate_appearances > 0 else 0
    
    def ops(self):
        return self.on_base_percentage() + self.slugging_percentage()
    
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

# 選手のデータを設定
players = [
    Player("岡大海", np.array([67, 28, 2, 7, 57, 259])/420),
    Player("藤岡裕大", np.array([67, 28, 2, 7, 57, 259])/420),
    Player("ポランコ", np.array([67, 28, 2, 7, 57, 259])/420),
    Player("ソト", np.array([67, 28, 2, 7, 57, 259])/420),
    Player("佐藤都志也", np.array([67, 28, 2, 7, 57, 259])/420),
    Player("荻野貴司", np.array([67, 28, 2, 7, 57, 259])/420),
    Player("藤原恭大", np.array([67, 28, 2, 7, 57, 259])/420),
    Player("中村奨吾", np.array([67, 28, 2, 7, 57, 259])/420),
    Player("小川龍成", np.array([67, 28, 2, 7, 57, 259])/420),
]

# 試合をシミュレート
score, game_log = simulate_game(players)
print(f"最終スコア: {score}")

# イニングごとの詳細を表示
print("\n試合の流れ:")
for inning, log in game_log:
    print(f"{inning}回:")
    for event in log:
        print(f"  {event}")

# 各選手の成績を表示
print("\n選手成績:")
for player in players:
    stats = player.detailed_stats()
    print(f"""{player.name} - 打率: {player.batting_average():.3f}, 
          出塁率: {player.on_base_percentage():.3f}, 
          長打率:{player.slugging_percentage():.3f},
          OPS:{player.ops():.3f},
          打点: {player.runs_batted_in}, 
          詳細成績: {stats}""")


# イニングごとの詳細をデータフレームで表示
log_data = {}
for inning, events in game_log:
    for player_name, result in events:
        if player_name not in log_data:
            log_data[player_name] = [""] * 9
        log_data[player_name][inning - 1] = result

game_flow_df = pd.DataFrame.from_dict(log_data, orient="index", columns=[f"{i+1}回" for i in range(9)])
print("\n試合の流れ:")
print(game_flow_df)

# 各選手の成績をデータフレームで表示
player_stats = {
    "名前": [],
    "打率": [],
    "出塁率": [],
    "打点": [],
    "単打": [],
    "二塁打": [],
    "三塁打": [],
    "本塁打": [],
    "打席数": [],
    "四死球": []
}

for player in players:
    stats = player.detailed_stats()
    player_stats["名前"].append(player.name)
    player_stats["打率"].append(player.batting_average())
    player_stats["出塁率"].append(player.on_base_percentage())
    player_stats["打点"].append(player.runs_batted_in)
    player_stats["単打"].append(stats["単打"])
    player_stats["二塁打"].append(stats["二塁打"])
    player_stats["三塁打"].append(stats["三塁打"])
    player_stats["本塁打"].append(stats["本塁打"])
    player_stats["打席数"].append(stats["打席数"])
    player_stats["四死球"].append(stats["四死球"])

player_stats_df = pd.DataFrame(player_stats)
print("\n選手成績:")
print(player_stats_df)
