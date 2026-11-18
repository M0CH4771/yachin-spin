-- ヤチンスピン デイリーランキング（Cloudflare D1）
CREATE TABLE IF NOT EXISTS players (
  id TEXT PRIMARY KEY,            -- 端末ごとのプレイヤーID（画面には出さない）
  name TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  banned INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS runs (
  id TEXT PRIMARY KEY,            -- 1回ごとのID
  player_id TEXT NOT NULL,
  day TEXT NOT NULL,              -- 日本時間の日付 YYYY-MM-DD
  seed INTEGER NOT NULL,          -- サーバーが配った乱数のタネ
  state TEXT NOT NULL,            -- サーバーで確かめ済みのところまでのゲームの状態
  n INTEGER NOT NULL DEFAULT 0,   -- 確かめ済みの操作の数
  over INTEGER NOT NULL DEFAULT 0,-- 1 = 終わった
  rents INTEGER,                  -- 払えた家賃の回数（サーバーで再生して求めた値）
  earned INTEGER,                 -- かせいだコインの合計（同じ回数のときの順位づけ）
  score INTEGER,                  -- rents * 1e12 + earned。家賃を1回払うか、終わるまでは NULL
  build TEXT,                     -- 最終的な構成（手持ちのシンボルの数とお守り）。ランキングで見せる
  started_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS runs_day_score ON runs(day, score DESC);
CREATE INDEX IF NOT EXISTS runs_player_day ON runs(player_id, day);
