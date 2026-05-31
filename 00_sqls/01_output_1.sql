/*
課題1：【データクレンジング＆エラーハンドリング】（SQL / Polars）
〜本業の名寄せ・ラベリング業務のスピードを爆上げする修行〜

ビジネス背景：
データサイエンスチームから「クラスタリングのモデルにデータを投入したいが、欠損値や異常値が含まれているため、BIやAIが誤作動を起こさないよう、データエンジニアリング側で綺麗なデータに整形してほしい」と依頼された。

タスク：
ビジネスロジックに基づく欠損値補正：
MINIMUM_PAYMENTS（最低支払い金額）の欠損値を、単なる「0」や全体の平均値で埋めるのではなく、「その会員の BALANCE（残高）の10%」または「同じ TENURE（保有期間）の会員の平均値」で動的に補正するロジックを実装せよ。

異常値の検知とラベリング：
クレジットカード限度額（CREDIT_LIMIT）に対して、残高（BALANCE）が超えている（＝オーバートップしている）異常な会員を検知し、is_over_limit フラグ（1または0）を立てよ。

文字列の正規化（名寄せへの応用）：
CUST_ID の前後に不要なスペースや改行コードが含まれていると仮定し（実務の汚いデータを想定）、これらを綺麗にトリム（除去）した一意のIDを生成せよ。

Intermediate（中級）として意識すべき裏側の動き：

これをPolarsの LazyFrame（遅延評価）を使い、メモリを極限まで節約したベクトル演算（when().then().otherwise()）で、一撃かつ高速に処理するコードが書けるか。
*/

-- ===========================
-- 1. ビジネスロジックに基づく欠損値補正：
-- MINIMUM_PAYMENTS（最低支払い金額）の欠損値を、単なる「0」や全体の平均値で埋めるのではなく、
-- 「その会員の BALANCE（残高）の10%」または「同じ TENURE（保有期間）の会員の平均値」で動的に補正するロジックを実装せよ。
-- ===========================
-- ---------------------------
-- base skelton (UK : CUST_ID)
-- ---------------------------
WITH 
base AS (
    SELECT 
        cust_id 
        , balance 
        , balance_frequency
        , purchases 
        , oneoff_purchases
        , installments_purchases
        , cash_advance
        , purchases_frequency
        , oneoffpurchasesfrequency
        , purchasesinstallmentsfrequency
        , cashadvancefrequency
        , cashadvancetrx
        , purchases_trx
        , credit_limit
        , payments
        , minimum_payments
        , prcfullpayment
        , tenure
    FROM RAW 
)
-- ---------------------------
-- TENURの平均値を算出
-- ---------------------------
, tmp_avg_tenur AS (
    SELECT 
        tenure 
        , AVG(minimum_payments) AS avg_minimum_payments
    FROM base 
    WHERE 
        minimum_payments IS NOT NULL 
    GROUP BY 
        tenure 
)
-- ---------------------------
-- 異常値の検知とラベリング： => baseに直接カラム追加, CTE不要
-- クレジットカード限度額（CREDIT_LIMIT）に対して、残高（BALANCE）が超えている（＝オーバートップしている）異常な会員を検知し、is_over_limit フラグ（1または0）を立てよ。
-- ---------------------------

-- ---------------------------
-- 文字列の正規化（名寄せへの応用）：Pythonタスク
-- CUST_ID の前後に不要なスペースや改行コードが含まれていると仮定し（実務の汚いデータを想定）、
-- これらを綺麗にトリム（除去）した一意のIDを生成せよ。
-- データの揺らぎイメージ => Pythonで対応する
    -- C10001 と c10001 が混在
    -- Ｃ１０００１（全角）と C10001（半角）
    -- " C10001 "（前後にスペース）、"C10001\n"（改行コードの巻き込み）
    -- 区切り文字の有無: C-10001、C_10001、C 10001
    -- 本来 001001 なのに 1001 になる
    -- 00000000、99999999、unknown、test_user
    -- "NULL" や "NaN" という「文字列」
    -- C10001_DELETED（退会済）、C10001_DUP（重複）、C10001_01（2回目の登録）
-- ---------------------------
, fix_name AS (
    SELECT 
        cust_id 
    FROM base 
)
-- ---------------------------
-- 欠損値の補完とフラグ付与
-- ---------------------------
, mrt_result AS (
    SELECT 
        cust_id 
        , balance 
        , balance_frequency
        , purchases 
        , oneoff_purchases
        , installments_purchases
        , cash_advance
        , purchases_frequency
        , oneoffpurchasesfrequency
        , purchasesinstallmentsfrequency
        , cashadvancefrequency
        , cashadvancetrx
        , purchases_trx
        , credit_limit
        , payments
        , CASE 
            WHEN minimum_payments IS NULL 
                THEN avg_minimum_payments 
            ELSE minimum_payments 
          END AS minimum_payments
        , prcfullpayment
        , tenure
        , CASE WHEN credit_limit >= balance THEN 1 ELSE 0 END AS is_over_limit
    FROM base 
    LEFT JOIN tmp_avg_tenur 
        USING(tenure)
)
SELECT * FROM mrt_result
;
-- ===========================
-- 確認用クエリ Start
-- ===========================
 SELECT 
    *
 FROM RAW 
 WHERE 
    MINIMUM_PAYMENTS IS NULL 
 ;
 
SELECT 'RAW' AS dsname, COUNT(1) AS cnt FROM RAW 
UNION ALL 
SELECT 'CALC' AS dsname, COUNT(CUST_ID) AS cnt FROM RAW 
;

SELECT * FROM RAW LIMIT 10
;

-- Calculate the ratio of installments_purchase / purchases
SELECT 
    CUST_ID 
    , PURCHASES / INSTALLMENTS_PURCHASES
FROM RAW 
;