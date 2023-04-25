{-# OPTIONS_GHC -Wno-unrecognised-pragmas #-}

{-# HLINT ignore "Avoid lambda using `infix`" #-}
{-# HLINT ignore "Use camelCase" #-}
{-# HLINT ignore "Eta reduce" #-}
{-# HLINT ignore "Avoid lambda" #-}
{-# HLINT ignore "Redundant lambda" #-}
{-# HLINT ignore "Collapse lambdas" #-}
{-# HLINT ignore "Use id" #-}
{-# HLINT ignore "Use const" #-}

-- 1.
scale_nums :: [Integer] -> Integer -> [Integer]
scale_nums nums factor = map (\x -> x * factor) nums

-- >>> scale_nums [1, 4, 9, 10] 3
-- [3,12,27,30]

only_odds :: [[Integer]] -> [[Integer]]
only_odds lists = filter (\x -> all (\y -> mod y 2 == 1) x) lists

-- >>> only_odds [[1, 2, 3], [3, 5], [], [8, 10], [11]]
-- [[3,5],[],[11]]

largest :: String -> String -> String
largest a b =
    if length a >= length b then a else b

largest_in_list :: [String] -> String
largest_in_list strings = foldl largest "" strings

-- >>> largest_in_list ["how", "now", "brown", "cow"]
-- "brown"
-- >>> largest_in_list ["cat", "mat", "bat"]
-- "cat"
-- >>> largest_in_list []
-- ""

-- 2.
count_if :: (a -> Bool) -> [a] -> Int
count_if f a
    | null a = 0
    | f (head a) = 1 + count_if f (tail a)
    | otherwise = count_if f (tail a)

-- >>> count_if (\x -> mod x 2 == 0) [2, 4, 6, 8, 9]
-- 4
-- >>> count_if (\x -> length x > 2) ["a", "ab", "abc"]
-- 1

count_if_with_filter :: (a -> Bool) -> [a] -> Int
count_if_with_filter f a = length (filter f a)

-- >>> count_if_with_filter (\x -> mod x 2 == 0) [2, 4, 6, 8, 9]
-- 4
-- >>> count_if_with_filter (\x -> length x > 2) ["a", "ab", "abc"]
-- 1

count_if_with_fold :: (a -> Bool) -> [a] -> Int
count_if_with_fold f a = foldl (\x y -> if f y then x + 1 else x) 0 a

-- >>> count_if_with_fold (\x -> mod x 2 == 0) [2, 4, 6, 8, 9]
-- 4
-- >>> count_if_with_fold (\x -> length x > 2) ["a", "ab", "abc"]
-- 1

-- foo :: Integer -> Integer -> Integer -> (Integer -> a) -> [a]
-- foo x y z t = map t [x, x + z .. y]

foo :: Integer -> Integer -> Integer -> (Integer -> b) -> [b]
foo =
    \x ->
        ( \y ->
            ( \z ->
                (\t -> map t [x, x + z .. y])
            )
        )

-- >>> foo 2 100 5 (\x -> x + 3)
-- [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]

f a b =
    let c = \a -> a -- (1)
        d = \c -> b -- (2)
     in \e f -> c d e -- (3)

-- >>> f 3 5 7 9
-- 5

-- data InstagramUser = Influencer | Normie

-- lit_collab :: InstagramUser -> InstagramUser -> Bool

-- data InstagramUser = Influencer [String] | Normie

-- -- >>> lit_collab (Influencer ["Google"]) (Normie)
-- -- False
-- lit_collab (Influencer a) (Influencer b) = True
-- lit_collab a b = False

-- is_sponsor :: InstagramUser -> String -> Bool
-- -- >>> is_sponsor (Influencer ["Google", "Instagram", "TikTok"]) "TikTok"
-- -- True
-- -- >>> is_sponsor Normie "Google"
-- -- False
-- is_sponsor Normie sponsor = False
-- is_sponsor (Influencer sponsors) sponsor = sponsor `elem` sponsors

data InstagramUser = Influencer [String] [InstagramUser] | Normie

count_influencers :: InstagramUser -> Integer
-- >>> :t Influencer
-- Influencer :: [String] -> [InstagramUser] -> InstagramUser
count_influencers Normie = 0
count_influencers (Influencer a b) = sum [1 | _ <- b]

data LinkedList = EmptyList | ListNode Integer LinkedList
    deriving (Show)

ll_contains :: LinkedList -> Integer -> Bool
-- >>> ll_contains (ListNode 3 (ListNode 6 EmptyList)) 3
-- True
-- >>> ll_contains (ListNode 3 (ListNode 6 EmptyList)) 4
-- False
ll_contains EmptyList num = False
ll_contains (ListNode a next) num = (a == num) || ll_contains next num

ll_insert :: LinkedList -> Integer -> Integer -> LinkedList
-- >>> ll_insert (ListNode 3 (ListNode 6 EmptyList)) 8 7
-- ListNode 3 (ListNode 6 (ListNode 7 EmptyList))
ll_insert EmptyList index value = ListNode value EmptyList
ll_insert (ListNode head next) index value
    | index <= 0 = ListNode value (ListNode head next)
    | otherwise = ListNode head (ll_insert next (index - 1) value)

longest_run :: [Bool] -> Int
longest_run list =
    checklist list 0 0
  where
    checklist list current maximum
        | null list = maximum
        | head list = checklist (tail list) (current + 1) (max (current + 1) maximum)
        | otherwise = checklist (tail list) 0 maximum

-- >>> longest_run [True, True, False, True, True, True, False, False]
-- 3
-- >>> longest_run [True, True]
-- 2
-- >>> longest_run [False, False, False, False]
-- 0
-- >>> longest_run [False, False, True]
-- 1

data Tree = Empty | Node Integer [Tree]

max_tree_value :: Tree -> Integer
max_tree_value Empty = 0
max_tree_value (Node val trees) = max val (maxlist [max_tree_value x | x <- trees])
  where
    maxlist list
        | null list = 0
        | length list == 1 = head list
        | otherwise = max (head list) (maxlist (tail list))

fibonacci :: Int -> [Int]
fibonacci n
    | n <= 0 = []
    | n == 1 = [1]
    | n == 2 = [1, 1]
    | otherwise = prev ++ [last prev + (last . init) prev]
  where
    prev = fibonacci (n - 1)

-- >>> fibonacci 10
-- [1,1,2,3,5,8,13,21,34,55]
-- >>> fibonacci (-1)
-- []
-- >>> fibonacci 3
-- [1,1,2]

data Event = Travel Integer | Fight Integer | Heal Integer

super_giuseppe :: [Event] -> Integer
super_giuseppe events = propogateEvents events 100
  where
    propogateEvents [] hp
        | hp <= 0 = -1
        | otherwise = hp
    propogateEvents ((Travel n) : xs) hp = propogateEvents xs (travelHandler n hp)
    propogateEvents ((Fight n) : xs) hp = propogateEvents xs (fightHandler n hp)
    propogateEvents ((Heal n) : xs) hp = propogateEvents xs (healHandler n hp)

travelHandler :: Integer -> Integer -> Integer
travelHandler n hp
    | hp <= 0 = -1
    | hp <= 40 = hp
    | otherwise = min 100 (hp + (n `div` 4))

fightHandler :: Integer -> Integer -> Integer
fightHandler n hp
    | hp <= 0 = -1
    | hp <= 40 = hp - (n `div` 2)
    | otherwise = hp - n

healHandler :: Integer -> Integer -> Integer
healHandler n hp
    | hp <= 0 = -1
    | otherwise = min (hp + n) 100

-- >>> super_giuseppe [Heal 20, Fight 20, Travel 40, Fight 60, Travel 80, Heal 30, Fight 40, Fight 20]
-- 10
-- >>> super_giuseppe [Heal 20, Fight 20, Travel 40, Fight 60, Travel 80]
-- 30
-- >>> super_giuseppe [Heal 40, Fight 70, Travel 100, Fight 60, Heal 40]
-- -1
-- >>> super_giuseppe [Fight 100]
-- -1
