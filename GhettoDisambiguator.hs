#!/usr/bin/env runhaskell
import PGF
import System.Environment
import Control.Applicative
import Data.Maybe
import Data.List

main = do
    args <- getArgs
    if length args == 2 then do
        [p, l] <- getArgs
        pgf <- readPGF p
        loop $ fromMaybe (\x -> x :: String) $ (parseString pgf) <$> (readLanguage l)
        else do
            [p, l, s] <- getArgs
            pgf <- readPGF p 
            putStrLn $ fromMaybe "" $ (parseString pgf) <$> (readLanguage l) <*> pure s

getWord :: Bool -> String -> String
getWord _ ('^':xs)   = getWord True xs
getWord _ ('/':xs)   = ' ' : getWord False xs
getWord False (x:xs) = getWord False xs
getWord True (x:xs)  = x : getWord True xs
getWord _ "" = ""

parseSentence :: String -> [String]
parseSentence = words . getWord False

loop :: (String -> String) -> IO ()
loop parse = do
    s <- getLine
    if s == "quit" then putStrLn "bye" else do
        putStrLn $ parse s
        loop parse

getMorph :: PGF -> Language -> String -> [(Lemma, Analysis)]
getMorph p l s = lookupMorpho (buildMorpho p l) s

getMorph2 :: Morpho -> String -> [(Lemma, Analysis)]
getMorph2 m s = lookupMorpho m s

initStream :: PGF -> Language -> String -> String -> String
initStream p l  orig s
    | length morph > 0  = "^" ++ s ++ buildStream p l morph orig
    | otherwise         = "^" ++ s ++ "/*" ++ s ++ "$ "
    where morph = getMorph p l s

initStream2 :: PGF -> Language -> Morpho -> String -> String -> [(Lemma, Analysis)] -> [Tree] -> String
initStream2 p l m orig s la tl
    | length la > 0  = "^" ++ s ++ buildStream2 p l la orig tl
    | otherwise         = "^" ++ s ++ "/*" ++ s ++ "$ "
    --where morph = getMorph2 m s

buildStream :: PGF -> Language -> [(Lemma, Analysis)] -> String -> String
buildStream _ _ [] _ = "$ "
buildStream p ln ((l, a):xs) s
    | isValid p ln s l = "/" ++ show l ++ buildTags (words a) ++ buildStream p ln xs s
    | otherwise = buildStream p ln xs s
    where t = startCat p

buildStream2 :: PGF -> Language -> [(Lemma, Analysis)] -> String -> [Tree] -> String
buildStream2 _ _ [] _ _ = "$ "
buildStream2 p ln ((l, a):xs) s tl
    | isValid2 l tl = "/" ++ show l ++ buildTags (words a) ++ buildStream2 p ln xs s tl
    | otherwise = buildStream2 p ln xs s tl
    where t = startCat p

isValid :: PGF -> Language -> String -> Lemma -> Bool
isValid p ln s l = isInfixOf (show l) . show $ (head $ filter (\x -> not $ isInfixOf "LStr" (show x)) (parse p ln t s))
    where t = startCat p

isValid2 :: Lemma -> [Tree] -> Bool
isValid2 l tl = isInfixOf (show l) . show $ (head $ filter (\x -> not $ isInfixOf "LStr" (show x)) tl)

buildTags :: [String] -> String
buildTags [] = ""
buildTags (x:xs) = "<" ++ x ++ ">" ++ buildTags xs 

parseString :: PGF -> Language -> String -> String
parseString p l s = foldl (\acc x -> acc ++ x) "" (map (initStream p l (getWord False s)) (parseSentence s))

